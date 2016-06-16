"""
<name>OWLatinTest.py</name>
<description>Programme de recuperation des fichiers sur thelatinlibrary.com</description>

"""

# Tous les print sont là pour les tests des differentes etapes du code
import urllib2
import re

# 1) Premier niveau

#1.1) Recuperer la mainpage du site

link = "http://www.thelatinlibrary.com"
f = urllib2.urlopen(link)
mainpage = f.read()
# print mainpage

#1.2) Sur la mainpage, recuperer la liste deroulante des auteurs avec leurs liens

regex = r"<form name=myform>(.+ ?)"

if re.search(regex, mainpage):
    match1 = re.search(regex, mainpage)
    #print "%s" % (match1.group(0))
    listederoulante = (match1.group(0))

#1.3) Dans la liste deroulante, recuperer les liens des pages des auteurs

regex = r"(?<=value=)(.+?)(?=>)"
matches = re.findall(regex, listederoulante)
urls = list()
#supprimer la derniere ligne en xml pour ne pas prendre la value du button
for matchA in matches[:-1]:
    #normaliser les noms des pages en supprimant les guillemets
    matchA = re.sub('"','',matchA)
    #rajouter le nom de domaine pour que les urls soit complet
    linkauthorpage = "http://www.thelatinlibrary.com/%s" % (matchA)
    urls.append(linkauthorpage)


#1.4) Dans la liste deroulante, recuperer les noms des auteurs

regex = r"(?<=>)(.+?)(?=<option)"
matches2 = re.findall(regex, listederoulante)
auteurs = list()
#supprimer la première ligne en xml pour ne pas prendre ce qui precede le premier option
for matchB in matches2[1:]:
    nomdauteur = "%s" % (matchB)
    #normaliser les noms des auteurs en supprimant les espaces
    nomdauteur = re.sub(' ','',nomdauteur)
    #rajouter une etoile pour faciliter les regex delimitantes suivantes
    auteurs.append('*' + nomdauteur)
#ajouter Vitruvius qui n etait pas recupere par la regex car dernier pas suivi de <option
auteurs.append('*Vitruvius')
# print auteurs

# 2) Deuxieme niveau 

linktextspage = list()
oeuvresTitle = list()
# 2.1) Ouvrir les pages html de chaque oeuvre
for value, value2 in zip(urls, auteurs):
    f2 = urllib2.urlopen(value)
    pageoeuvres = f2.read() 
    # print pageoeuvres
    
    # 2.2) Recuperer les titres des oeuvres (pas termine // beaucoup d anomalies)     
    regex = r"(?<=<h2 class=\"work\">)(.+?)(?=</h2>)"
    matches3 = re.findall(regex, pageoeuvres, re.IGNORECASE) 
    for matchC in matches3:        
        nomdeloeuvre = "%s" % (matchC)
        oeuvresTitle.append(nomdeloeuvre)

    oeuvresTitlePartNames = list()
    oeuvresURL = list()
    authorPartName = list()
    
    # 2.3) Recuperer toutes les balises <a> qui possedent les informations pour chaque page individuelle de chaque oeuvre
    regex = r"(?<=<a )(.+?)(?=</a>)"
    matches4 = re.findall(regex, pageoeuvres, re.IGNORECASE)
    for matchD in matches4:
        listederoulanteoeuvres = "%s%s" % (matchD, value2)
        #corriger le # de Walter de Châtillon pour qu il ne soit pas suppr après
        listederoulanteoeuvres = re.sub('&#226;','a',listederoulanteoeuvres)
        #supprimer les espaces codes en dur
        listederoulanteoeuvres = re.sub('&nbsp;','',listederoulanteoeuvres)
        linktextspage.append(listederoulanteoeuvres)
        # print "%s%s" % (matchD, value2)
# print len(linktextspage)

# 2.4 ) Regrouper les liens qui ne correspondent pas à une oeuvre
# Liens qui possedent un name ou # pour permettre l appel a un chapitre precis
matching_name = [s for s in linktextspage if "name" in s]
matching_NAME = [s for s in linktextspage if "NAME" in s]
matching_DIESE = [s for s in linktextspage if "#" in s]
matching_NAME.extend(matching_DIESE)
matching_name.extend(matching_NAME)

# 2.5) Retirer les liens en 'name' 'NAME' et '#' de la liste des <a>
linktextspage = [s for s in linktextspage if s not in matching_name]

# print matching_name
# print linktextspage

# 3) Troisieme niveau

for value in auteurs:        
    # 3.1) Repertorier les liens inutiles de la liste
    # Chaque pi correspond a une anomalie du site originel
    # Certaines sont plus recurrentes que d autres / certaines sont uniques
    # Les trouver a pris une enorme quantite de temps
    # Penser a envoyer un mail aux createurs du site pour leur demander d uniformiser
    p1 = 'href="misc.html">The Miscellany%s' % (value) #Footer
    p2 = 'href="http://thelatinlibrary.com/misc.html">The Miscellany%s' % (value) #Footer
    p3 = 'href="index.html">The Latin Library%s' % (value) #Footer
    p4 = 'href="/index.html">The Latin Library%s' % (value) #Footer
    p5 = 'HREF="index.html">The Latin Library*Persius' #Footer
    p6 = 'href="http://thelatinlibrary.com/index">The Latin Library*Donatus' #Footer
    p7 = 'href="http://thelatinlibrary.com/index.html">The Latin Library%s' % (value) #Footer
    p8 = 'href="classics.html">The Classics Page%s' % (value) #Footer
    p9 = 'href="/classics.html">The Classics Page%s' % (value) #Footer
    p10 = 'href="http://thelatinlibrary.com/classics">The Classics Page%s' % (value) #Footer
    p11 = 'href="christian.html">Christian Latin%s' % (value) #Footer
    p12 = 'href="/christian">Christian Latin%s' % (value) #Footer
    p13 = 'href="medieval.html">Medieval Latin%s' % (value) #Footer
    p14 = 'href="neo.html">Neo-Latin%s' % (value) #Footer
    # Celui-ci typiquement est une erreur de code car les autres possedent tous un # et ont ete supprimes precedemment
    p15 = 'href="78b">78b*Catullus'
    # 3.2) La linktextspage passe par un filtre pour chaque anomalie
    # Cette liste de filtre a ete construite de telle sorte a pouvoir etre facilement transformee en boucle 'p'i++
    # Par manque de temps et des soucis avec la declaration de "p"i dans les filtres nous y avons renonce
    linktextspage = filter(lambda a: a != p1, linktextspage)   
    linktextspage = filter(lambda a: a != p2, linktextspage)
    linktextspage = filter(lambda a: a != p3, linktextspage)
    linktextspage = filter(lambda a: a != p4, linktextspage)
    linktextspage = filter(lambda a: a != p5, linktextspage)
    linktextspage = filter(lambda a: a != p6, linktextspage)
    linktextspage = filter(lambda a: a != p7, linktextspage)
    linktextspage = filter(lambda a: a != p8, linktextspage)
    linktextspage = filter(lambda a: a != p9, linktextspage)
    linktextspage = filter(lambda a: a != p10, linktextspage)
    linktextspage = filter(lambda a: a != p11, linktextspage)
    linktextspage = filter(lambda a: a != p12, linktextspage)
    linktextspage = filter(lambda a: a != p13, linktextspage)
    linktextspage = filter(lambda a: a != p14, linktextspage)
    linktextspage = filter(lambda a: a != p15, linktextspage) 

# print linktextspage

# 3.3) Transformer la list en string
stringtexts = ''.join(linktextspage)
# Corriger une erreur du code originel ou une guillemet surnumeraire existait
# Erreur trouvee dans le code source de http://thelatinlibrary.com/frontinus.html
stringtexts = re.sub('""','"',stringtexts)   
# print stringtexts

# 4) Creation du tableau de donnees

# 4.1) Recuperation des donnees de nom de partie d oeuvre (ex: Liber XII)
regex = r"(?<=html\">)(.+?)(?=\*)"
matches5 = re.findall(regex, stringtexts, re.IGNORECASE)
for matchE in matches5:
    nomduTexte = "%s" % (matchE)
    oeuvresTitlePartNames.append(nomduTexte)

# 4.2) Recuperation des donnees de nom d auteur qui avaient ete annotes (ex: Tacitus)
regex = r"\*(.+?)(?=href)"
matches6 = re.findall(regex, stringtexts, re.IGNORECASE)   
for matchF in matches6:
    nomAuteurPartie = "%s" % (matchF)
    authorPartName.append(nomAuteurPartie)

# 4.3) Recuperation des donnees du lien de la page de cette partie (ex: http://thelatinlibrary.com/tacitus/tac.ann12.shtml)
regex = r"(?<=href=\")(.+?)(?=html\">)"
matches7 = re.findall(regex, stringtexts, re.IGNORECASE)
for matchG in matches7:
    urlTexte = "http://www.thelatinlibrary.com/%shtml" % (matchG)
    oeuvresURL.append(urlTexte)

# 4.4)  Creation du tableau

#rajouter le Vitruvius manquant en fin de tableau       
authorPartName.extend(['Vitruvius'])
# print len(authorPartName)
# print oeuvresTitle
# print len(oeuvresTitlePartNames)
# print len(oeuvresURL)

partieNomUrl = zip(oeuvresTitlePartNames, oeuvresURL, authorPartName)

# 5) Afficher le tableau de donnees
print partieNomUrl

# manque 2 choses : 
# - récupérer les noms des oeuvres quand il n'y a que les livres (commencé)
# - widget incomplet / a relier avec ce tableau
