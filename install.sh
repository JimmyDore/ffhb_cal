#!/bin/bash


git pull
cd ffhb_cal || exit
cp ffhb_cal/conf.local.py ffhb_cal/conf.py
source ../myvenv/bin/activate
pip install -r ../requirements.txt
python manage.py makemigrations ffhb_cal_app
python manage.py migrate
if [ "$1" == "prod" ] #Si la variable input 1 est prod, on redémarre le démon gunicorn, sinon serveur local
then
        sudo systemctl restart gunicorn_ffhb_cal.service
else
	port=8000
	echo "tentative de démarrage sur le port $port" #On utilise les variables comme ça"
        python manage.py runserver $port
	test $? -gt 128 && break #Si ctrl+c, on quitte le serveur  
	rc=$? #on recup code de retour
	if [[ $rc != 0 ]] #Si c'est une erreur (port déjà utilisé) on boucle
	then
		echo "python manage.py runserver 8000 pour relancer le serveur"
	fi
fi
