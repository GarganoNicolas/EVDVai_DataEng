#!/bin/bash

# Clean landing directory and get data
rm /home/hadoop/landing/*

wget -P /home/hadoop/landing "https://dataengineerpublic.blob.core.windows.net/data-engineer/f1/results.csv"
wget -P /home/hadoop/landing "https://dataengineerpublic.blob.core.windows.net/data-engineer/f1/drivers.csv"
wget -P /home/hadoop/landing "https://dataengineerpublic.blob.core.windows.net/data-engineer/f1/constructors.csv"
wget -P /home/hadoop/landing "https://dataengineerpublic.blob.core.windows.net/data-engineer/f1/races.csv"

# Clean HDFS directory and put the data from landing into Hadoop
hdfs dfs -rm /ingest/*
hdfs dfs -put /home/hadoop/landing/* /ingest




# to copy the file into the container
# sudo docker cp ingest_data.sh edvai_hadoop:/home/hadoop/scripts/

# to give permision to exectute the script
# chmod +x /home/hadoop/scripts/ingest_data.sh

# to run 
# /home/hadoop/scripts/ingest_data.sh