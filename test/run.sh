#!/bin/bash

docker-compose down -v

docker-compose up -d api
echo "WAITING FOR API TO INITIALIZE"
sleep 5
docker-compose up test
docker-compose down -v