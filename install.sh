#!/bin/bash

git pull
cd ffhb_cal || exit
cp ffhb_cal/conf.local.py ffhb_cal/conf.py
source ../ffhb_venv/bin/activate
pip install -r ../requirements.txt
python manage.py makemigrations ffhb_cal_app
python manage.py migrate
if [ "$1" == "prod" ]
then
        sudo systemctl restart gunicorn_ffhb_cal.service
else
        python manage.py runserver
fi
