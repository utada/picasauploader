#!/bin/bash

source /home/utada/.virtualenvs/picasa/bin/activate

hostname=`hostname`

if [[ $hostname = 'utada-i7' ]];then
  user=utada4@gmail.com
  password=megumegu6
  picasa=/home/utada/git/picasauploader/picasa.sh
elif [[ $hostname = 'ThinkPad-T400' ]];then
  user=utada6@gmail.com
  password=sizue9109
  picasa=/home/utada/picasauploader/picasa.sh
fi

$picasa --email $user --password $password --source /home/utada/Pictures/$1
