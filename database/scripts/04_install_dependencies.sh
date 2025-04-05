#!/bin/bash
# Install Python and dependencies needed for data generation
apt-get update
apt-get install -y python3 python3-pip
pip3 install -r /requirements.txt 