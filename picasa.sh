#!/bin/bash

source /home/utada/.virtualenvs/picasa/bin/activate

host=`hostname`

if [ "$host" = "utada-i7" ];then
  user=utada4@gmail.com
  password=megumegu6
  picasa=/home/utada/git/picasauploader/picasa.py
elif [ "$host" = "ThinkPad-T400" ];then
  user=utada6@gmail.com
  password=sizue9109
  picasa=/home/utada/picasauploader/picasa.py
fi


$picasa --email $user --password $password --source /home/utada/Pictures/$1
