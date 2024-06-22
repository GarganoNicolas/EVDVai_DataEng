#!/bin/bash

docker pull apache/superset

docker run -d -p 8080:8088 -e "SUPERSET_SECRET_KEY=$SUPERSET_KEY" --name superset apache/superset

# docker exec -it superset pip install sqlalchemy-redshift
# docker exec -it superset pip install google-cloud-bigquery
# docker exec -it superset pip install pyodbc

docker exec -it superset superset fab create-admin \
              --username admin \
              --firstname Superset \
              --lastname Admin \
              --email admin@admin.com \
              --password admin


docker exec -it superset superset db upgrade


# docker cp superset:/app/superset_home/superset.db ./superset.db
# gsutil mb gs://supersetdb
# gsutil cp superset.db gs://supersetdb
# docker cp config.py superset:/app/superset/config.py


docker exec -it superset superset init

docker stop superset

docker commit superset apache/superset1

docker tag apache/superset1 gcr.io/$PROJECT_ID/superset:v2

gcloud auth configure-docker

docker push gcr.io/$PROJECT_ID/superset:v2

gcloud services enable run.googleapis.com

gcloud run deploy superset \
  --image gcr.io/$PROJECT_ID/superset:v2 \
  --platform=managed \
  --region=us-central1 \
  --port=8088 \
  --allow-unauthenticated \
  --set-env-vars SUPERSET_SECRET_KEY=$SUPERSET_KEY \
  --min-instances=1


