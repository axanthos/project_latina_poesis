# project_latin_text
Widget Textable which get the CLTK versification tool and apply it to texts segments
##################################
Specification: Widget Textable Latin Text
##################################



1 Introduction
**************


1.1 But du projet
=================
Créer un Widget Textable qui permettrait de sélectionner les textes à partir de thelatinlibrary.com

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
![Mockup](https://cloud.githubusercontent.com/assets/17759898/16052528/dfa3aa26-3264-11e6-97c0-c79d45a04407.png)

2.2 Fonctionnalités minimales
=============================
    1) Récupération des textes sur thelatinlibrary.com
    2) Annotation des textes par auteurs
    3) Selection de l'auteur affiche ses pièces

2.3 Fonctionnalités principales
===============================
    1) Utilisateur choisi quel auteur l'intéresse
    2) Utilisateur choisi quelle pièce de cet auteur l'intéresse

2.4 Fonctionnalités optionnelles
===============================
Possibilité de sélectionner plusieurs textes d'un seul coup


2.5 Tests
=========
    Les Auteurs sont sélectables
    Les Pièces sont sélectables
    L'Indexation des lignes fonctionne
    Le programme réagit à une valeur NULL dans la segmentation output
    L'affichage fonctionne
    L'affichage est organisable


3 Etapes
*********



3.1 Version alpha
=================
* L'interface graphique est complétement construite.
* Les fonctionnalités minimales sont prises en charge par le logiciel.
* La documentation de base est intégrée


3.2 Remise et présentation
==========================
* Les fonctionnalités principales sont complétement prises en charge par le logiciel.
* La documentation du logiciel est complète.
* Le logiciel possède des routines de test de ses fonctionnalitées, principales ou optionelles.


4. Infrastructure
=================
Le projet est disponible sur GitHub à l'adresse https://github.com/Jandenm/project_latina_poesis
