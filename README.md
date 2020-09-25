# Bienvenue!

## tesseraktApiFlask est le back-end de Tesserakt.

 Il permet d'acceder à la base de donnée local ou sont enregistré les cubes connecté au cube master,
 ainsi que les données relatifs aux utilisateurs sur les exercices.

### Pour l'installation :

* Activer l'environnement virtuel

Lors de la première fois, il faut creer un environnement virtuel python à la base du projet :

> $ pip install virtualenv
> $ virtualenv flask

* il faut ensuite activer l'environnement virtuel

> $ source flask/Scripts/activate

(flask) doit apparaitre sur la ligne de commande.

* il faut ensuite installer flask

> $ pip install flask

* et les autres librairies

> $ sudo apt-get install libmariadb-dev

> $ pip3 install flask-mysqldb
> $pip3 install flask_bcrypt
> $ pip3 install flask_cors
> $ pip3 install pyyaml
> $ pip3 install flask_jwt_extended

* Enfin, pour lancer le projet

> flask run --host=0.0.0.0

### Et voila ! 
