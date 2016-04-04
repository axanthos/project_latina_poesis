# project_latina_poesis
Widget Textable which get the CLTK versification tool and apply it to texts segments
##################################
Specification: Widget Textable Latina Poesis
##################################



1 Introduction
**************


1.1 But du projet
=================
Créer un Widget Textable qui permettrait l'affichage de la versification de la poésie latine, à partir du CLTK

Dernière version en python 2 disponible


1.2 Aperçu des étapes
=====================
* Premiere version de la specification: 17 mars 2016
* Remise de la specification: 24 mars 2016
* Version alpha du projet:  28 avril 2016
* Remise et presentation du projet:  26 mai 2016

1.3 Equipe et responsabilités
==============================

* Julien Andenmatten `julien.andenmatten@unil.ch`_ :

.. _julien.andenmatten@unil.ch: mailto:julien.andenmatten@unil.ch

    - Documentation
    - GitHub
    - Code
    - Test



2 Technique
************


2.1 Mock-up de l'interface
==========================
![Mockup](https://cloud.githubusercontent.com/assets/17759898/14255359/ffc2ac5c-fa93-11e5-9798-0003284a5737.png)

2.2 Fonctionnalités minimales
=============================
    1) Récupération des textes sur CLTK
    2) Annotation des textes par auteurs
    3) Normalisation des textes
    4) Segmenter en répliques/vers
    5) Imposer la versification de CLTK au passage désiré (soit une réplique ou un vers)
    6) Réaliser ces fonctionnalités selon les choix de l'utilisateur
    7) Afficher les résultats lisiblement avec un algorithme de tri

2.3 Fonctionnalités principales
===============================
    1) Utilisateur choisi quel auteur l'intéresse
    2) Utilisateur choisi quelle pièce de cet auteur l'intéresse
    3) Utilisateur choisi quel taille de passage (segmentation) il désire
    4) Utilisateur entre le chiffre indiquant à quelle ligne apparait ce passage
    5) Utilisateur clique pour demander l'affichage du passage en question avec sa versification

2.4 Fonctionnalités optionelles
===============================
Possibilité de sélectionner plusieurs passages d'un seul coup


2.5 Tests
=========
    Les Auteurs sont sélectables
    Les Pièces sont sélectables
    L'Indexation des lignes fonctionne
    Les Segmentations fonctionnent
    Le programme réagit à une erreur dans la ligne donnée
    Le programme réagit à une valeur NULL dans la segmentation output
    L'outil de versification de CLTK est intégré au programme et fonctionnel
    L'affichage fonctionne
    L'affichage est organisable


3 Etapes
*********



3.1 Version alpha
=================
* L'interface graphique est complétement construite.
* Les fonctionnalités minimales sont prises en charge par le logiciel.



3.2 Remise et présentation
==========================
* Les fonctionnalités principales sont complétement prises en charge par le logiciel.
* La documentation du logiciel est complète.
* Le logiciel possède des routines de test de ses fonctionnalitées, principales ou optionelles.


4. Infrastructure
=================
Le projet est disponible sur GitHub à l'adresse https://github.com/Jandenm/project_latina_poesis
