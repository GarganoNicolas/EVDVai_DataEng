#!/bin/bash

# Crear Variables de entorno. La KEY y el PROJECT

export SUPERSET_KEY=$(openssl rand -hex 32)
export PROJECT_ID=$(gcloud info --format='value(config.project)')


# Traemos la imagen de Docker de Superset en DockerHub
docker pull apache/superset

# La corremos
docker run -d -p 8080:8088 -e "SUPERSET_SECRET_KEY=SUPERSET_KEY" --name superset apache/superset


# Si necesitamos cambiar la config tenemos estas dos opciones
# IMPORTANTE traer el archivo a la carpeta donde estamos haciendo el RUN

# docker cp config.py superset:/app/superset/config.py

# docker cp superset_config.py superset:/app/superset/superset_config.py
# docker exec -it superset export SUPERSET_CONFIG_PATH=/app/superset/superset_config.py


# Podemos agregarle dependencias
# docker exec -it superset pip install sqlalchemy-redshift
# docker exec -it superset pip install google-cloud-bigquery
# docker exec -it superset pip install pyodbc


# Creamos el usuario
docker exec -it superset superset fab create-admin \
              --username admin \
              --firstname Superset \
              --lastname Admin \
              --email admin@admin.com \
              --password admin

# Actualizamos la db (Creo)
docker exec -it superset superset db upgrade

# Iniciamos
docker exec -it superset superset init

# Si no se trabo el script es porque todo esta bien

# Se detiene el contenedor
docker stop superset

# Se crea una nueva imagen con nuestra config de usuario Admin, dependencias, archivo config.py
docker commit superset apache/superset1

# Se taguea a artifact registory
docker tag apache/superset1 gcr.io/PROJECT_ID/superset:v2

# Le damos permiso a Docker para push a artifact registory
gcloud auth configure-docker

# Hacemos el push
docker push gcr.io/PROJECT_ID/superset:v2

# Habilitamos a Cloud Run
gcloud services enable run.googleapis.com

# Y Cloud Run define...
gcloud run deploy superset \
  --image gcr.io/PROJECT_ID/superset:v2 \
  --platform=managed \
  --region=us-central1 \
  --port=8088 \
  --allow-unauthenticated \
  --set-env-vars SUPERSET_SECRET_KEY=SUPERSET_KEY

# Gol !

# Todavia me falta que la DB corra fuera del Cloud Run para no arranque de cero cada vez que lo usas