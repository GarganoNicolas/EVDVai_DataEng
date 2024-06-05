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

docker cp superset:/app/superset_home/superset.db ./superset.db

gsutil mb gs://supersetdb
gsutil cp superset.db gs://supersetdb

python3 dbPathCreator.py

docker cp config.py superset:/app/superset/config.py

# O podemos crear el archivo superset_config.py para modificar solo aquello que queremos
# docker cp superset_config.py superset:/app/superset/superset_config.py
# docker exec -it superset export SUPERSET_CONFIG_PATH=/app/superset/superset_config.py


# Iniciamos
docker exec -it superset superset init

# Si no se trabo el script es porque todo esta bien

# Se detiene el contenedor
docker stop superset

# Se crea una nueva imagen con nuestra config de usuario Admin, dependencias, archivo config.py
docker commit superset apache/superset1

# Se taguea a artifact registory
docker tag apache/superset1 gcr.io/$PROJECT_ID/superset:v2

# Le damos permiso a Docker para push a artifact registory
gcloud auth configure-docker

# Hacemos el push
docker push gcr.io/PROJECT_ID/superset:v2

# Habilitamos a Cloud Run
gcloud services enable run.googleapis.com

# Y Cloud Run define...
gcloud run deploy superset \
  --image gcr.io/$PROJECT_ID/superset:v2 \
  --platform=managed \
  --region=us-central1 \
  --port=8088 \
  --allow-unauthenticated \
  --set-env-vars SUPERSET_SECRET_KEY=$SUPERSET_KEY YOUR_ACCESS_KEY_ID=$YOUR_ACCESS_KEY_ID YOUR_SECRET_KEY=$YOUR_ACCESS_KEY_ID

# Gol !

