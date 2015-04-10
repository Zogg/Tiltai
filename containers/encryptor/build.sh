#!/bin/bash

cp -f ../../libs/* ./src
sudo docker build -t zogg/encryptor .
