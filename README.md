<p align="center">
  <img src="./icon.jpg" alt="Image Description">
</p>

# SoftDesk API RESTful 

Notre nouvelle application SoftDesk met à disposition une API RESTful permettant principalement la création et le suivi de projet via différents endpoints (points d'entrée). 

Ces endpoints fournissent des informations à partir d'urls interrogeables à l'aide d'un client HTTP graphique comme un navigateur web ou postman, ou d'un client HTTP programmatique comme requests en python ou fetch/axios en javascript.

Ces endpoints supportent les requêtes HTTP utilisant la méthode GET et POST. Seuls les auteurs des ressources (compte utilisateur, projet, issue, comment) peuvent utiliser avoir recours aux méthodes PUT et DELETE.



## L'usage 

L’application présente quatre cas d’utilisation :

1. Créer un projet ;
2. Ajouter des contributeurs au projet ;
3. Créer une issue (bug, tache ou fonctionnalité à réaliser) dans le projet et l'assigner à un contributeur ;
4. Créer un commentaire sur une issue pour faire remonter des informations importantes à tous les contributeurs du projet ;

## Les endpoints utilisateurs

### Ressource User

0. Il est nécessaire d'avoir plus de 15ans pour s'inscrire et être en mesure de partager ses données.

1.  http://127.0.0.1:8000/api/user/ : permet de s'inscrire (POST) ou de consulter (GET) la liste des utilisateurs actifs acceptant de partager leurs données.

2.  http://127.0.0.1:8000/api/user/user.id/ : permet de consulter (GET) la vue détaillée et de mettre à jour ou supprimer la ressource (PUT ou DELETE). 

3. http://127.0.0.1:8000/api/change-password/ : permet à un utilisateur authentifié de modifier son mot de passe (PUT).

### Ressource Project

0. Seul l'auteur du projet peut mettre à jour ou supprimer le projet (PUT ou DELETE). Seuls les contributeurs du projet peuvent lire les données du projet (GET).

1. http://127.0.0.1:8000/api/project/ : Fourni la liste des projets aux contributeurs (GET). Permet également la création de projet (POST).

2.  http://127.0.0.1:8000/api/project/project.id/ : permet de consulter (GET) la vue détaillée et de mettre à jour ou supprimer la ressource (PUT ou DELETE).  

### Ressource Contributor

0. Seul l'auteur d'un projet peut ajouter un contributeur (POST), modifier ou supprimer un contributeur (PUT ou DELETE).

1. http://127.0.0.1:8000/api/contributor/ : fourni la liste des contributeurs aux projets dont l'utilisateur connecté est l'auteur (GET). Permet d'ajouter un contributeur aux projets dont l'utilisateur connecté est l'auteur (POST).

2. http://127.0.0.1:8000/api/contributor/contributor.id : permet de consulter (GET) la vue détaillée et de mettre à jour ou supprimer la ressource (PUT ou DELETE). 

### Ressource Issue

0. Seuls les contributeurs d'un projet peuvent consulter les issues de ce dernier (GET) ou créer une issue (POST) liée à ce projet. Seul l'auteur d'une Issue peut modifier ou supprimer (PUT ou DELETE) son issue.

1. http://127.0.0.1:8000/api/issue/ : fourni la liste des issues liées aux projets dont l'utilisateur connecté est contributeur (GET). Permet de créer une issue liée à un des projets dont l'utilisateur connecté est contributeur (POST).

2. http://127.0.0.1:8000/api/issue/issue.id : permet de consulter (GET) la vue détaillée et de mettre à jour ou supprimer la ressource (PUT ou DELETE). 

### Ressource Comment

0. Seuls les contributeurs d'un projet peuvent consulter les comment sur les issues (GET) ou créer un comment sur une issue (POST) liée à ce projet. Seul l'auteur d'un comment peut modifier ou supprimer (PUT ou DELETE) son comment.

1. http://127.0.0.1:8000/api/comment/ : fourni la liste des comments liées aux projets dont l'utilisateur connecté est contributeur (GET). Permet de créer un comment sur une issue liée à un des projets dont l'utilisateur connecté est contributeur (POST).

2. http://127.0.0.1:8000/api/comment/comment.id : permet de consulter (GET) la vue détaillée et de mettre à jour ou supprimer la ressource (PUT ou DELETE). 


## Les endpoints admin donnant plein droit (GET, PUT, DELETE) sur les ressources 

0. (identifiant : admin ; password : 00000000pw)

1. http://127.0.0.1:8000/api/admin/user/ : accès et gestion des ressources user

2. http://127.0.0.1:8000/api/admin/project/ : accès et gestion des ressources project

3. http://127.0.0.1:8000/api/admin/issue/ : accès et gestion des ressources issue

4. http://127.0.0.1:8000/api/admin/comment/ : accès et gestion des ressources comment



## Installation

Cette application Django exécutable localement peut être installée en suivant les étapes décrites ci-dessous. Si vous n'avez pas encore installé Python sur votre PC, vous pouvez le télécharger via ce lien : https://www.python.org/downloads/ puis l'installer.

### Installation et exécution de l'application avec venv et pip

1. Cloner ce dépôt de code à l'aide de la commande `$ git clone https://github.com/NidalChateur/OC_P10_SOFTDESK.git` (vous pouvez également télécharger le code [en temps qu'archive zip](https://github.com/NidalChateur/OC_P10_SOFTDESK/archive/refs/heads/main.zip))
2. Rendez-vous depuis un terminal à la racine du répertoire OC_P10_SOFTDESK avec la commande `$ cd OC_P10_SOFTDESK`
3. Créer un environnement virtuel pour le projet avec `$ python -m venv env` sous windows ou `$ python3 -m venv env` sous macos ou linux.
4. Activez l'environnement virtuel avec `$ env\Scripts\activate` sous windows ou `$ source env/bin/activate` sous macos ou linux.
5. Installez les dépendances du projet avec la commande `$ pip install -r requirements.txt`
6. Démarrer le serveur avec `$ python manage.py runserver`

### Installation et exécution de l'application avec venv, pip et poetry

1. Cloner ce dépôt de code à l'aide de la commande `$ git clone https://github.com/NidalChateur/OC_P10_SOFTDESK.git` (vous pouvez également télécharger le code [en temps qu'archive zip](https://github.com/NidalChateur/OC_P10_SOFTDESK/archive/refs/heads/main.zip))
2. Rendez-vous depuis un terminal à la racine du répertoire OC_P10_SOFTDESK avec la commande `$ cd OC_P10_SOFTDESK`
3. Créer un environnement virtuel pour le projet avec `$ python -m venv env` sous windows ou `$ python3 -m venv env` sous macos ou linux.
4. Activez l'environnement virtuel avec `$ env\Scripts\activate` sous windows ou `$ source env/bin/activate` sous macos ou linux.
5. Installez poetry avec la commande `$ pip install poetry`
6. Installez les dépendances du projet avec la commande`$ poetry install`
7. Démarrer le serveur avec `$ poetry run python manage.py runserver`
Lorsque le serveur fonctionne, après l'étape 7 de la procédure, l'application peut être consultée à partir de l'url [http://127.0.0.1:8000/].

Les étapes 1 à 7 ne sont requises que pour l'installation initiale. Pour les lancements ultérieurs du serveur de l'application, il suffit d'exécuter les étapes 4 et 7 à partir du répertoire racine du projet.
