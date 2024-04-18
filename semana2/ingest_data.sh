#!/bin/bash

# Check if a URL was provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <URL>"
    exit 1
fi

URL="$1"

# Check if the URL exists
HTTP_STATUS=$(curl -o /dev/null --silent --head --write-out '%{http_code}\n' "$URL")

if [ "$HTTP_STATUS" -eq 404 ]; then
    echo "Error: The URL $URL was not found (HTTP 404)."
    exit 1
fi

# Clean landing directory and get data
rm /home/hadoop/landing/*
wget -P /home/hadoop/landing "$URL"

# Extract the filename from the URL
FILENAME=${URL##*/}

# Clean HDFS directory and put the data from landing into Hadoop
hdfs dfs -rm /ingest/*
hdfs dfs -put /home/hadoop/landing/* /ingest

# Send a happy message if the process works
echo "The file $FILENAME has been successfully downloaded and uploaded to HDFS."


# to copy the file into the container
# sudo docker cp ingest_data.sh edvai_hadoop:/home/hadoop/scripts/

# to give permision to exectute the script
# chmod +x /home/hadoop/scripts/ingest_data.sh

# to run with other url
# /home/hadoop/scripts/ingest_data.sh https://dataengineerpublic.blob.core.windows.net/data-engineer/yellow_tripdata_2021-01.csv
# or you can change the url