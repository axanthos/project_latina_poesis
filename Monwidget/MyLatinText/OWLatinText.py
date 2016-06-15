"""
<name>OWLatinText</name>
<description>Programme de recuperation des fichiers sur thelatinlibrary.com</description>
<icon>LatinText.svg</icon>
"""

__version__ = u'0.0.5'


import Orange
from OWWidget import *
import OWGUI
from _textable.widgets.LTTL.Segmentation import Segmentation
from _textable.widgets.LTTL.Input import Input


from _textable.widgets.TextableUtils import *   # Provides several utilities.

import urllib2
import re
import json
import textwrap
import codecs


class OWLatinText(OWWidget):
    """Orange widget for importing XML-TEI data from the Latin Library
    website (http://www.thelatinlibrary.com/)
    """

    # Widget settings declaration...
    settingsList = [
        u'autoSend',
        u'label',
        u'uuid',
        u'oeuvresSelectionnees',
        u'auteur',
        u'piece',
        u'importesURLs',
        u'displayAdvancedSettings',
    ]

    def __init__(self, parent=None, signalManager=None):
        """Createur de widget."""

        # Appel du createur de widget (OWWidget).
        OWWidget.__init__(self, parent, signalManager, wantMainArea=0)
        
        # Definition des chaines d entree et de sortie...
        self.inputs = []
        self.outputs = [("LatinTextData", Segmentation)]
        
        # Les etapes de recuperation suivantes sont inutiles desormais grace au OWLatinTest.py
        # Elles peuvent etre sorties des commentaires pour avoir une meilleure visualisation du rendu final du widget mais ne le rende pas reactif
        # Cette partie doit etre remplacee par un appel a la liste des auteurs creee dans OWLatinTest.py
        
        # #1)Recuperer la mainpage du site

        # link = "http://www.thelatinlibrary.com"
        # f = urllib2.urlopen(link)
        # mainpage = f.read()
        # #print mainpage

        # #2)Sur la mainpage, recuperer la liste deroulante des auteurs avec leurs liens

        # regex = r"<form name=myform>(.+ ?)"

        # if re.search(regex, mainpage):
           # match1 = re.search(regex, mainpage)
           # #print "%s" % (match1.group(0))
           # listederoulante = (match1.group(0))

        # else:
            # print "The regex pattern does not match."

        # #3)Dans la liste deroulante, recuperer les liens des pages des auteurs
            
        # regex = r"(?<=value=)(.+?)(?=>)"
        # matches = re.findall(regex, listederoulante)
        # #supprimer la derniere ligne en xml
        # #normaliser les noms de pages en supprimant les guillemets
        # #rajouter le nom de domaine pour que les urls soit complet
        # urls = list()
        # for matchA in matches[:-1]:
            # matchA = re.sub('"','',matchA)
            # linkauthorpage = "http://www.thelatinlibrary.com/%s" % (matchA)
            # urls.append(linkauthorpage)


        # #4)Dans la liste deroulante, recuperer les noms des auteurs

        # regex = r"(?<=>)(.+?)(?=<option)"
        # matches2 = re.findall(regex, listederoulante)
        # #supprimer la première ligne en xml
        # auteurs = list()
        # for matchB in matches2[1:]:
            # nomdauteur = "%s" % (matchB) 
            # auteurs.append(nomdauteur)

        
        #5)Creation des differents modules du widget
        #Definition attribut sendButton
        self.sendButton = SendButton(
            widget=self.controlArea,
            master=self,
            callback=self.sendData,
            infoBoxAttribute='infoBox',
            sendIfPreCallback=self.updateGUI,
        )
        self.auteur = list()
        self.piece = list()
        self.autoSend = True
        self.infoBox = InfoBox(widget=self.controlArea)
        # GUI

        OWGUI.separator(self.controlArea)
        self.optionsBox = OWGUI.widgetBox(self.controlArea, "Options")

        #list authors
        OWGUI.comboBox(
            self.optionsBox,
            self,
            'auteur',
            items = auteurs,
            sendSelectedValue=True,
            label='Auteur',
            callback=self.sendButton.settingsChanged
        )
        #list pieces
        
        #recuperer les noms des pieces
        
        OWGUI.listBox(
            self.optionsBox,
            self,
            'piece',
            labels='piece',
            callback=self.sendButton.settingsChanged
        )

        OWGUI.separator(self.controlArea)

        box = OWGUI.widgetBox(self.controlArea, "Info")
        self.infoa = OWGUI.widgetLabel(box, 'No data on input yet, waiting to get something.')
        self.infob = OWGUI.widgetLabel(box, '')
        self.resize(100,50)

    def sendData(self):
        
        # Celles-ci aussi / il faudra remplir cette fonction avec un appel au tableau final par les occurences de la valeur de l auteur selectionne
        
        # linktextspage = list()
        # #Recuperer les pages html de chaque oeuvre
        # for value in urls:
            # f2 = urllib2.urlopen(value)
            # pageoeuvres = f2.read()
            # #print pageoeuvres

            # oeuvresTitle = list()
            # oeuvresURL = list()

            # regex = r"(?<=<a )(.+?)(?=</a>)"
            # if re.findall(regex, pageoeuvres, re.IGNORECASE):       
                # for match2 in re.findall(regex, pageoeuvres, re.IGNORECASE):        
                    # listederoulanteoeuvres = (match2)       
                    # linktextspage.append(listederoulanteoeuvres)
                    # #print "%s" % (match2)    

            # else:
            
                # print "The regex pattern does not match"

            # regex = r"(?<=<h2 class=\"work\">)(.+?)(?=</h2>)"
            # if re.findall(regex, pageoeuvres, re.IGNORECASE):
                # for matchE in re.findall(regex, pageoeuvres, re.IGNORECASE):
                    # nomdeloeuvre = "%s" % (matchE)
                    # oeuvresTitle.append(nomdeloeuvre)
                    # # print nomdeloeuvre
            # else:   

                # regex = r"(?<=shtml\">)(.+?)(?=</a>)"
                # matches3 = re.findall(regex, listederoulanteoeuvres)
                
                # for matchC in matches3:
                    # nomduTexte = "%s" % (matchC)
                    # oeuvresTitle.extend(nomduTexte)
                    
                
                # regex = r"(?<=href=\")(.+?)(?=\">)"
                # matches4 = re.findall(regex, listederoulanteoeuvres)
                
                # for matchD in matches4[:-3]:
                    # urlTexte = "%s" % (matchD)
                    # oeuvresURL.extend(urlTexte)
                    
        # # retirer les liens inutiles de la liste 
        # i = 'href="misc.html">The Miscellany'
        # j = 'href="index.html">The Latin Library'
        # k = 'href="/index.html">The Latin Library'
        # l = 'href="classics.html">The Classics Page'


        # result0 = filter(lambda a: a != i, linktextspage)
        # result1 = filter(lambda a: a != j, result0)
        # result2 = filter(lambda a: a != k, result1)
        # result3 = filter(lambda a: a != l, result2)        

    def updateGUI(self):
        pass

    def commit(self):
        pass

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
    
if __name__ == '__main__':
    myApplication = QApplication(sys.argv)
    myWidget = OWLatinText()
    myWidget.show()
    myApplication.exec_()
