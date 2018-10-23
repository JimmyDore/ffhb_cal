#!/bin/bash

#FIXME : Ne pas exécuter toutes les instructions si pas nécessaires, effectuer des tests à chaque fois
#Genre, pas besoin de copier le fichier s'il est déjà présent, etc
git_root=$(git rev-parse --show-toplevel)
cd $git_root || exit

echo -e "\033[45m**** We get the sources on repo\033[0m"
git pull || exit
cd ffhb_cal || exit
echo -e "\033[45m **** We will use your conf file\033[0m"
cp ffhb_cal/conf.local.py ffhb_cal/conf.py || exit
echo -e "\033[45m **** Mise en place du git commit\033[0m"
cp ../pre-commit ../.git/hooks/pre-commit || exit
chown jimmydore:jimmydore ../.git/hooks/pre-commit || exit #TODO : Recup LES noms des env virtuels, des user unix dans la config 
chmod +x ../.git/hooks/pre-commit
#CHANGE THE NAME OF USER HERE
#source ../myvenv/bin/activate || sudo ../ffhb_venv/bin/activate || exit #!!!!!!!!! CHANGER NOM ENV VIRTUAL ICI
echo -e "\033[45m **** Installation des requirements\033[0m" 
../ffhb_venv/bin/pip install -r ../requirements.txt || ../myvenv/bin/pip install -r ../requirements.txt || exit
echo -e "\033[45m **** Installation des migrations\033[0m" 
../ffhb_venv/bin/python manage.py makemigrations ffhb_cal_app || myvenv/ffhb_venv/bin/python manage.py makemigrations ffhb_cal_app || exit
../ffhb_venv/bin/python manage.py migrate || ../my_venv/bin/python manage.py migrate || exit
echo -e "\033[45m **** On récupère les fichiers statiques\033[0m" 
../ffhb_venv/bin/python manage.py collectstatic || ../myvenv/bin/python manage.py collectstatic || exit
#sudo -u ${USERNAME} chown -R jimmydore:www-data static/ || exit
sudo chown -R jimmydore:www-data static/ || exit
if [ "$1" == "prod" ] #Si la variable input 1 est prod, on redémarre le démon gunicorn, sinon serveur local
then
	echo -e "\033[45m **** Redémarrage sur le serveur\033[0m" 
        sudo systemctl restart gunicorn_ffhb_cal.service || exit
else
	port=8000 
	echo -e "\033[45m **** Démarrage sur le serveur local\033[0m" 
	echo "---tentative de démarrage sur le port $port" #On utilise les variables comme ça"
        ../ffhb_venv/bin/python manage.py runserver $port || ../myvenv/bin/python manage.py runserver $port || exit
	test $? -gt 128 && break #Si ctrl+c, on quitte le serveur  
	rc=$? #on recup code de retour
	if [[ $rc != 0 ]] #Si c'est une erreur
	then
		echo "Apparemment le port est déjà utilisé :"
		echo "Utilise python manage.py runserver 8080 pour relancer le serveur"
		echo "sur un autre port que le port 8000 par défaut"
	fi
fi
