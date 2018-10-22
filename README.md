Application réalisée avec le framework Django, Python 3.6
déployée à l'aide de gunicorn et nginx, sur un VPS Ubuntu Server 18.04 

Exctraction des données "Compétitions" du site de la fédération française de handball : http://www.ff-handball.org/competitions 

On veut centraliser les données de tous les matchs de hand de la fédération (matchs départementaux, régionaux, nationaux, du plus bas au plus niveau en france)

Deux fonctionnalités principales : 
- Récupérer le calendrier de son équipe (ou de n'importe quelle équipe en France) afin de l'importer dans son outil de calendrier personnel (Google Calendar dans mon cas). On va donc générer un lien pointant vers un fichier.ics : il faudra ajouter ce lien à vos agendas. La synchronisation avec les véritables données peuvent être de 24 à 48h.
- Datavisualisation complète et analyse exploratoire de données provenant du hand amateur et professionel français.

# Install app
1) Install mysql on server : 
Tutorial : https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04

2) Clone the project and go into it: 
```console
jimmydore@ubuntu:~/Projets$ git clone https://github.com/JimmyDore/ffhb_cal.git
jimmydore@ubuntu:~/Projets$ cd ffhb_cal/
```
3) Install python3 and virtualenv if not already done, and create a virtual env
```console
jimmydore@ubuntu:~/Projets/ffhb_cal$ sudo apt-get install python3-venv
jimmydore@ubuntu:~/Projets/ffhb_cal$ python3 -m venv ffhb_venv
```

4) Create database in mysql
```console
jimmydore@ubuntu:~/Projets/ffhb_cal$ mysql -u root -p
mysql> create database if not exists ffhb_cal_db character set UTF8mb4 collate utf8mb4_bin;
Query OK, 1 row affected (0.00 sec)
mysql> exit;

5) Create conf.local.py from conf.py in django project folder
```console
jimmydore@ubuntu:~/Projets/ffhb_cal/$ cd ffhb_cal/ffhb_cal
jimmydore@ubuntu:~/Projets/ffhb_cal/ffhb_cal/ffhb_cal$ sudo cp conf.py conf.local.py
jimmydore@ubuntu:~/Projets/ffhb_cal/ffhb_cal/ffhb_cal$ vim conf.local.py #Here, replace values with your own id/passwords...
jimmydore@ubuntu:~/Projets/ffhb_cal/ffhb_cal/ffhb_cal$ sudo cp conf.local.py conf.py #now, the file conf.py has your own values
```
> **Note:** **Never** push conf.local.py and push conf.py if only new fields in the file


5) Lancer le script d'installation

```console
jimmydore@ubuntu:~/Projets/ffhb_cal$ ./install.sh
```

6) Run the app
Run locally :
```console
(ffhb_venv) jimmydore@jimmydore-XPS-13-9360:~/Documents/Projets_perso/ffhb_cal/ffhb_cal$ python manage.py runserver 8000
```

Run on a server :
Plusieurs tutoriels existent pour installer un projet Django sur un serveur. J'ai personnellement choisi gunicorn couplé avec nginx :
- https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04
- https://tutos.readthedocs.io/en/latest/source/ndg.html

Le fichier de conf de gunicorn est le fichier **gunicorn_start.sh**
Le fichier de conf de nginx est le fichier **nginx_conf**
Le dernier fichier est le fichier de service pour gunicorn et cette app, afin de deamoniser le process **gunicorn_ffhb_cal.service**

# Useful commands
In the virtualenv of the Django project, you can make a lot of useful commands :

1) Manage SQL shell
```console
(myvenv) jimmydore@jimmydore-XPS-13-9360:~/Documents/Projets_perso/ffhb_cal/ffhb_cal$ python manage.py dbshell
```

2) Manage python shell
```console
(myvenv) jimmydore@jimmydore-XPS-13-9360:~/Documents/Projets_perso/ffhb_cal/ffhb_cal$ python manage.py shell
```

3) Generate UML File from your model database 
```console
(myvenv) jimmydore@jimmydore-XPS-13-9360:~/Documents/Projets_perso/ffhb_cal/ffhb_cal$ ./manage.py graph_models -a > ../ffhb_cal_UML.dot; dot ../ffhb_cal_UML.dot -Tpng -o ../ffhb_cal_UML.png
```

