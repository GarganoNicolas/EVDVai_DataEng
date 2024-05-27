#!/bin/bash

wget -P /home/hadoop/landing "https://dataengineerpublic.blob.core.windows.net/data-engineer/f1/drivers.csv"

/home/hadoop/hadoop/bin/hdfs dfs -put /home/hadoop/landing/drivers.csv /ingest