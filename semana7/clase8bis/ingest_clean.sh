#!/bin/bash

rm -rf /home/hadoop/landing/*
/home/hadoop/hadoop/bin/hdfs dfs -rm -f /ingest/*

# sudo docker cp . edvai_hadoop2:/home/hadoop/scripts/clase8bis
