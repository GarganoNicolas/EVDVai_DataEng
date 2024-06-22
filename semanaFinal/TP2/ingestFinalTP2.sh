#!/bin/bash

# Clean landing directory and get data
rm /home/hadoop/landing/*

wget -P /home/hadoop/landing -O /home/hadoop/landing/CarRentalData.csv "https://edvaibucket.blob.core.windows.net/data-engineer-edvai/CarRentalData.csv?sp=r&st=2023-11-06T12:52:39Z&se=2025-11-06T20:52:39Z&sv=2022-11-02&sr=c&sig=J4Ddi2c7Ep23OhQLPisbYaerlH472iigPwc1%2FkG80EM%3D"
wget -P /home/hadoop/landing -O /home/hadoop/landing/united-states-of-america-state-Buenos_Aires.csv "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/georef-united-states-of-america-state/exports/csv?lang=en&timezone=America%2FArgentina%2FBuenos_Aires&use_labels=true&delimiter=%3B"

test -f /home/hadoop/landing/CarRentalData.csv
test -f /home/hadoop/landing//home/hadoop/landing/united-states-of-america-state-Buenos_Aires.csv

# Clean HDFS directory and put the data from landing into Hadoop
/home/hadoop/hadoop/bin/hdfs dfs -rm /ingest/*
/home/hadoop/hadoop/bin/hdfs dfs -put /home/hadoop/landing/* /ingest