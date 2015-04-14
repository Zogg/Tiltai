#!/bin/bash

mkdir ./libs
cp -f ../../dist/*.tar.gz ./libs/
sudo docker build -t zogg/feeder .
