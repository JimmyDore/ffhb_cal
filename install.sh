#!/bin/bash

#FIXME : Ne pas exécuter toutes les instructions si pas nécessaires, effectuer des tests à chaque fois
#Genre, pas besoin de copier le fichier s'il est déjà présent, etc

echo -e "\033[45m**** We get the sources on repo\033[0m"
git pull || exit
cd ffhb_cal || exit
echo -e "\033[45m **** We will use your conf file\033[0m"
cp ffhb_cal/conf.local.py ffhb_cal/conf.py || exit
echo -e "\033[45m **** Mise en place du git commit\033[0m"
ln -s ../pre-commit ../.git/hooks/pre-commit || exit
source ../myvenv/bin/activate || ../ffhb_venv/bin/activate || exit #!!!!!!!!! CHANGER NOM ENV VIRTUAL ICI
echo -e "\033[45m **** Installation des requirements\033[0m" 
pip install -r ../requirements.txt || exit
echo -e "\033[45m **** Installation des migrations\033[0m" 
python manage.py makemigrations ffhb_cal_app || exit
python manage.py migrate || exit
echo -e "\033[45m **** On récupère les fichiers statiques\033[0m" 
python manage.py collectstatic || exit
sudo -u ${USERNAME} chown -R jimmydore:www-data static/ || exit
if [ "$1" == "prod" ] #Si la variable input 1 est prod, on redémarre le démon gunicorn, sinon serveur local
then
	echo -e "\033[45m **** Redémarrage sur le serveur\033[0m" 
        sudo systemctl restart gunicorn_ffhb_cal.service || exit
else
	port=8000 
	echo -e "\033[45m **** Démarrage sur le serveur local\033[0m" 
	echo "---tentative de démarrage sur le port $port" #On utilise les variables comme ça"
        python manage.py runserver $port || exit
	test $? -gt 128 && break #Si ctrl+c, on quitte le serveur  
	rc=$? #on recup code de retour
	if [[ $rc != 0 ]] #Si c'est une erreur
	then
		echo "Apparemment le port est déjà utilisé :"
		echo "Utilise python manage.py runserver 8080 pour relancer le serveur"
		echo "sur un autre port que le port 8000 par défaut"
	fi
fi
