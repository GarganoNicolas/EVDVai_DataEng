#!/bin/bash

docker pull apache/superset

docker run -d -p 8888:8088 \
  --name superset \
  -e "SUPERSET_SECRET_KEY=edvai12345" \
  apache/superset

docker cp edvai_logo.png superset:/app/superset/static/assets/images/edvai_logo.png

docker cp superset_config.py superset:/app/superset/superset_config.py

docker cp config.py superset:/app/superset/config.py

docker exec -it superset superset fab create-admin \
              --username edvai \
              --firstname Edvai \
              --lastname Admin \
              --email admin@superset.com \
              --password edvai12345

docker exec -it superset superset db upgrade

docker exec -it superset superset init



# Si queremos guardar nuestra imagen de docker configurada

# docker stop superset
# docker commit superset apache/superset1
