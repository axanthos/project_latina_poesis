"""
<name>OWLatinText</name>
<description>Programme de recuperation des fichiers sur thelatinlibrary.com</description>
<icon>LatinText.svg</icon>
"""

__version__ = u'0.0.5'


import urllib2
import re



#1)Recuperer la mainpage du site
# class OWLatinTest:
    # """Programme de recuperation des fichiers sur thelatinlibrary.com"""
    # def __init__(self, parent):
        # """Recupere la liste des auteurs et leurs urls respectifs"""
link = "http://www.thelatinlibrary.com"
f = urllib2.urlopen(link)
mainpage = f.read()
#print mainpage

#2)Sur la mainpage, recuperer la liste deroulante des auteurs avec leurs liens

regex = r"<form name=myform>(.+ ?)"

if re.search(regex, mainpage):
    match1 = re.search(regex, mainpage)
    #print "%s" % (match1.group(0))
    listederoulante = (match1.group(0))

else:
    print "The regex pattern does not match."

#3)Dans la liste deroulante, recuperer les liens des pages des auteurs

regex = r"(?<=value=)(.+?)(?=>)"
matches = re.findall(regex, listederoulante)
#supprimer la derniere ligne en xml
#normaliser les noms de pages en supprimant les guillemets
#rajouter le nom de domaine pour que les urls soit complet
urls = list()
for matchA in matches[:-1]:
    matchA = re.sub('"','',matchA)
    linkauthorpage = "http://www.thelatinlibrary.com/%s" % (matchA)
    urls.append(linkauthorpage)


#4)Dans la liste deroulante, recuperer les noms des auteurs

regex = r"(?<=>)(.+?)(?=<option)"
matches2 = re.findall(regex, listederoulante)
#supprimer la première ligne en xml
auteurs = list()
for matchB in matches2[1:]:
    nomdauteur = "%s" % (matchB)
    auteurs.append(nomdauteur)

# def updateTitleList():
    # """Recupere la valeur de l auteur et l utilise pour selectionner
    # l'URL correspondant"""
linktextspage = list()
oeuvresTitle = list()
#Recuperer les pages html de chaque oeuvre
for value in urls:
    f2 = urllib2.urlopen(value)
    pageoeuvres = f2.read()
    # print pageoeuvres
    
    regex = r"(?<=<h2 class=\"work\">)(.+?)(?=</h2>)"
    match5 = re.findall(regex, pageoeuvres, re.IGNORECASE) 
    for matchE in match5:
        
        nomdeloeuvre = "%s" % (matchE)
        oeuvresTitle.append(nomdeloeuvre)

    oeuvresTitleName = list()
    oeuvresURL = list()

    regex = r"(?<=<a )(.+?)(?=</a>)"
    if re.findall(regex, pageoeuvres, re.IGNORECASE):
        for match2 in re.findall(regex, pageoeuvres, re.IGNORECASE):
            listederoulanteoeuvres = (match2)
            linktextspage.append(listederoulanteoeuvres)
            # print "%s" % (match2)   
    else:

        print "The regex pattern does not match"

        
# retirer les liens inutiles de la liste 
i = 'href="misc.html">The Miscellany'
j = 'href="index.html">The Latin Library'
k = 'href="/index.html">The Latin Library'
l = 'href="classics.html">The Classics Page'
result0 = filter(lambda a: a != i, linktextspage)
result1 = filter(lambda a: a != j, result0)
result2 = filter(lambda a: a != k, result1)
result3 = filter(lambda a: a != l, result2)

stringtexts = ''.join(result3) 
              
# print stringtexts

regex = r"(?<=html\">)(.+?)(?=href)"
matches3 = re.findall(regex, stringtexts, re.IGNORECASE)

for matchC in matches3:
    nomduTexte = "%s" % (matchC)
    oeuvresTitleName.append(nomduTexte)


regex = r"(?<=href=\")(.+?)(?=\">)"
matches4 = re.findall(regex, stringtexts, re.IGNORECASE)

for matchD in matches4:
    urlTexte = "http://www.thelatinlibrary.com/%s" % (matchD)
    oeuvresURL.append(urlTexte)        
        
# print result3

print oeuvresTitle
# print oeuvresTitleName
# print oeuvresURL
#Tester la fonction self.sendData
# OWLatinTest.__init__(self)
# OWLatinTest.updateTitleList(self)

    # def updateGUI(self):
        # pass

    # def commit(self):
        # pass

    # def recupererAuteurSelect(auteur, tuples_url_auteurs):
    #     if self.auteur is not None:
    #         self.piece.clear()
    #         self.piece.addItem(u'(all)')
    #         for piece in self.piece[self.auteur]:
    #             self.piece.addItem(piece)
    # recupererAuteurSelect()

    # def ouvreUrlOeuvres(urls):
        # for auteur in enumerate(auteurs):
            # file_name = "%s" %
            # response = urllib2.urlopen(url)
            # with open(file_name, 'wb') as out_file:
                # shutil.copyfileobj(response, out_file)

# fetch_urls(urls)

#Controleur sur cmd

# if __name__ == '__main__':
    # myApplication = QApplication(sys.argv)
    # myWidget = OWLatinTest()
    # myApplication.exec_()
