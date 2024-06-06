#!/bin/bash

# Create Docker network
if [ $( docker network ls | grep taskpilot | wc -l ) -eq 0 ]; then
  docker network create taskpilot
fi

# Start services
start_service () {
  docker stop taskpilot-"$1" && docker rm taskpilot-"$1"
  docker rmi taskpilot-"$1"

  docker build -f taskpilot/"$1"/Dockerfile_"$1" -t bogdanivan12/taskpilot-"$1":latest .

  docker run --net taskpilot -p "$2":"$2" --name taskpilot-"$1" bogdanivan12/taskpilot-"$1":latest &
}

start_service api 8080


# Elasticsearch
if [ $( docker ps -a | grep taskpilot-elastic | wc -l ) -gt 0 ]; then
  docker start taskpilot-elastic
else
  docker run --net taskpilot --name taskpilot-elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.11.4 &
fi


# Testing
set -x

SCRIPT_PATH=$(dirname "$0")

python3 -m pylint taskpilot \
  --init-hook="import sys; sys.path.append('$SCRIPT_PATH')" \
  --rcfile=.pylintrc

python3 -m pytest --disable-warnings