#!/bin/bash

wget -P /home/hadoop/landing "https://dataengineerpublic.blob.core.windows.net/data-engineer/f1/races.csv"

/home/hadoop/hadoop/bin/hdfs dfs -put /home/hadoop/landing/races.csv /ingest