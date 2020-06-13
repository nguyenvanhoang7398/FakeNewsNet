#!/bin/bash

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -p)
    LOG_PATH="$2"
    shift # past argument
    shift # past value
    ;;
    -j)
    JOB_ID="$2"
    shift # past argument
    shift # past value
    ;;
esac
done

rm -rf fakenewsnet_dataset
/home/nguyen/anaconda3/envs/fyp/bin/python main.py

# create a copy of the crawled data for later use
cp -r fakenewsnet_dataset data_${JOB_ID}

echo "COMPLETED" >> ${LOG_PATH}