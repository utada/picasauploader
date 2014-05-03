#!/bin/bash

source /home/utada/.virtualenvs/picasa/bin/activate

./picasa.py --email $1 --password $2 --source /home/utada/Pictures/$3
