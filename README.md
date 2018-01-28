# Eistiens.net v3




## Introduction

Bienvenue sur le dépôt du projet [eistiens.net](http://eistiens.net). Ce projet est géré par l'association [ATILLA](http://atilla.org),
Si vous souhaitez participer, n'hésitez pas à nous contacter pour prendre part au projet!

----------

## Pré-requis

Nous vous recommandons fortement d'utiliser virtualenv afin de travailler sur le projet dans un environnement contrôlé. (https://virtualenv.pypa.io/en/stable/). Il vous sera nécessaire d'utiliser :

- arcanist ```apt install arcanist```
- python 3.5
- Django 1.9
- virtualenv ```apt install virtualenv```

----------

## Développement

Le développement d'Eistiens.net se fait via la plateforme [phabricator.atilla.org](http://phabricator.atilla.org).

Vous pouvez également suivre l'avancement du projet ici :

- Développement : [dev.eistiens.net](http://dev.eistiens.net)
- Pré-production : [preprod.eistiens.net](http://preprod.eistiens.net)

Si vous souhaitez participer au développement des fonctionnalités de ce projet,
rendez vous sur la plateforme de gestion du projet.

----------

## Informations complémentaires


1. Avant de travailler sur le projet, et sous conditions que vous utiliez un virtualenv, il est _nécessaire_ d'activer le virtualenv avant de travailler sans quoi les dépendances ne seront pas disponibles.
2. Notre processus de developpement est détaillé sur [cette page](http://phabricator.atilla.org/w/eistiens-net/code_review_workflow/), et nécessite l'utilisation d'Arcanist (voir [ici](https://secure.phabricator.com/book/phabricator/article/arcanist_quick_start/))


----------

##  Setup

A la racine du projet (contenant ce README.md et le requirements.txt), exécutez les lignes ci-dessous : 
```
    $ virtualenv -p `which python3` venv # Create a virtualenv called venv and using local python3 distribution available on your box
    $ source venv/bin/activate  # You should create an alias of this, you will use this one often
    $ pip install -r requirements.txt # Install projet dependancies
```

----------

## Installation des données de base
---

Ce projet, pour permettre aux développeurs de démarrer rapidement à bosser sur la plateforme, contient des _fixtures_ pour initialiser les différentes tables de la BDD sans avoir à le faire à la main. Avant de s'en servir, il est important de s'assurer que la base de donnée est propre (et donc vide afin d'éviter des collisions). Pour faire une installation from scratch de la base, executez les commandes suivantes :
```
    $ ./manage.py flush    # Flush all data from DB
    $ rm db.sqlite3        # Make sure that DB is really empty (destroys it)
    $ ./manage.py migrate  # Recreate tables in database
    $ ./manage.py loaddata */fixtures/*/* # Loads sample data into the database
```
----------

## Fin de développement

Lorsque vous avez terminé de travailler sur Enet, il est important de penser à sortir du virtualenv. Pour ce faire, fermez le terminal ou executez : 
```
    $ deactivate
```
