#!/bin/bash

cp ../rump-server.py ./
sudo docker build -t "rumppy:1.0.0" -f Dockerfile .
sudo docker tag "rumppy:1.0.0" "rumppy:latest"
sudo docker compose up -d