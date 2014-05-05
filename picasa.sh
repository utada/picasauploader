#!/bin/bash

source /home/utada/.virtualenvs/picasa/bin/activate

hostname=`hostname`

if [[ $hostname = 'utada-i7' ]];then
  user=utada4@gmail.com
  password=megumegu6
elif [[ $hostname = 'ThinkPad-T400' ]];then
  user=utada6@gmail.com
  password=sizue9109
fi

./picasa.py --email $user --password $password --source /home/utada/Pictures/$1
