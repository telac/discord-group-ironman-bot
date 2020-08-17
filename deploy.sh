#!/usr/bin/env bash
docker build . -t group:latest
sudo docker run -d group:latest