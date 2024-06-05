#!/bin/bash

# Permisos
# TU USUARIO
# Artifact Registry Administrator
# Artifact Registry Create-on-Push Writer
# Storage Admin
# COMPUTE SERVICE ACCOUNT
# Storage Admin

# Crear Variables de entorno. La KEY y el PROJECT

# export SUPERSET_KEY=$(openssl rand -hex 32)
# export YOUR_ACCESS_KEY_ID=$(openssl rand -hex 32)
# export YOUR_ACCESS_KEY_ID=$(openssl rand -hex 32)
# export PROJECT_ID=$(gcloud info --format='value(config.project)')



# Traemos la imagen de Docker de Superset en DockerHub
docker pull apache/superset

# La corremos
docker run -d -p 8080:8088 -e "SUPERSET_SECRET_KEY=$SUPERSET_KEY" --name superset apache/superset


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

# Traemos el superset.db
docker cp superset:/app/superset_home/superset.db ./superset.db

# Creamos un bucket para el superset.db donde se guarda la metadata
# Check if the bucket exists
if ! gsutil ls -b gs://supersetdb >/dev/null 2>&1; then
    # If the bucket does not exist, create it
    gsutil mb gs://supersetdb
else
    echo "Bucket 'superset' already exists. Skipping bucket creation."
fi

# Copiamos el file a gs. NO sobreescribimos podemos perder toda nuestra metadata
if gsutil ls gs://supersetdb/superset.db >/dev/null 2>&1; then
    echo "File 'superset.db' already exists in the bucket 'supersetdb'. Skipping copy operation."
else
    gsutil cp superset.db gs://supersetdb
fi

# Necesitamos cambiar la config 
# IMPORTANTE traer el archivo a la carpeta donde estamos haciendo el RUN
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
  --set-env-vars SUPERSET_SECRET_KEY=$SUPERSET_KEY

# Gol !

