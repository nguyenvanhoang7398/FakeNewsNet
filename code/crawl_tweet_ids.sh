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
esac
done

/home/nguyen/anaconda3/envs/fyp/bin/python crawl_tweet_ids.py
echo "COMPLETED" >> ${LOG_PATH}