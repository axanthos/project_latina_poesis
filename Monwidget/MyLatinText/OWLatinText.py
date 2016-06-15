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
import inspect
import os
import pickle


class OWLatinText(OWWidget):
    """Orange widget for importing XML-TEI data from the Latin Library
    website (http://www.thelatinlibrary.com/)
    """

    # Widget settings declaration...
    settingsList = [
        u'autoSend',
        u'label',
        u'uuid',
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
        
        # Initialisation des commandes
        self.autoSend = True
        self.auteur = list()
        self.piece = u'piece'
        self.titleLabels =  list()
        self.oeuvresSelectionnees = list()
        self.importesURLs = list()
        
        # Always end Textable widget settings with the following 3 lines...
        self.uuid = None
        self.loadSettings()
        self.uuid = getWidgetUuid(self)
        
        # Other attributes...
        self.segmentation = Input()
        self.titleSeg = None
        self.filteredTitleSeg = None
        self.filterValues = dict()
        self.base_url =     \
          u'http://www.thelatinlibrary.com'
        self.document_base_url =     \
          u'http://www.thelatinlibrary.com'
          
        # Next two instructions are helpers from TextableUtils. Corresponding
        # interface elements are declared here and actually drawn below (at
        # their position in the UI)...
        self.infoBox = InfoBox(widget=self.controlArea)
        self.sendButton = SendButton(
            widget=self.controlArea,
            master=self,
            callback=self.sendData,
            infoBoxAttribute=u'infoBox',
            sendIfPreCallback=self.updateGUI,
        )
		# Les etapes de recuperation suivantes sont inutiles desormais grace au OWLatinTest.py
        # Elles peuvent etre sorties des commentaires pour avoir une meilleure visualisation du rendu final du widget mais ne le rende pas reactif
		# Cette partie doit a present etre remplacee par un appel a la liste des auteurs creee dans OWLatinTest.py
        
        # #2)Recuperer la mainpage du site à la création du widget

        # link = "http://www.thelatinlibrary.com"
        # f = urllib2.urlopen(link)
        # mainpage = f.read()
        # #print mainpage

        # #3)Sur la mainpage, recuperer la liste deroulante des auteurs avec leurs liens

        # regex = r"<form name=myform>(.+ ?)"

        # if re.search(regex, mainpage):
           # match1 = re.search(regex, mainpage)
           # #print "%s" % (match1.group(0))
           # listederoulante = (match1.group(0))

        # else:
            # print "The regex pattern does not match."

        # #4)Dans la liste deroulante, recuperer les liens des pages des auteurs
            
        # regex = r"(?<=value=)(.+?)(?=>)"
        # matches = re.findall(regex, listederoulante)
        # #supprimer la derniere ligne en xml
        # #normaliser les noms de pages en supprimant les guillemets
        # #rajouter le nom de domaine pour que les urls soit complet
        # global urls
        # urls = list()
        # for matchA in matches[:-1]:
            # matchA = re.sub('"','',matchA)
            # linkauthorpage = "http://www.thelatinlibrary.com/%s" % (matchA)
            # urls.append(linkauthorpage)


        # #5)Dans la liste deroulante, recuperer les noms des auteurs

        # regex = r"(?<=>)(.+?)(?=<option)"
        # matches2 = re.findall(regex, listederoulante)
        # #supprimer la première ligne en xml
        # auteurs = list()
        # for matchB in matches2[1:]:
            # nomdauteur = "%s" % (matchB) 
            # auteurs.append(nomdauteur)
        
        #1)Creation des differents modules du widget
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


        self.infob = OWGUI.widgetLabel(self.optionsBox, '')
        self.resize(100,50)
        
        # Now Info box and Send button must be drawn...
        
        self.infoBox.draw()
        self.sendButton.draw()
        
        # Show the first pieces
        self.getPieces()

        # Send data if autoSend.
        self.sendButton.sendIf()
        
    def getPieces (self):
        
		# Celles-ci aussi / il faudra remplir cette fonction avec un appel au tableau final par les occurences de la valeur de l auteur selectionne
        
		# if self.auteur is not None:
            # urlValue = urls[len(self.auteur)]
            
            # linktextspage = list()
            # oeuvresTitle = list()
            # #Recuperer les pages html de chaque oeuvre
            # f2 = urllib2.urlopen(urlValue)
            # pageoeuvres = f2.read()
            # # print pageoeuvres
            
            # regex = r"(?<=<h2 class=\"work\">)(.+?)(?=</h2>)"
            # match5 = re.findall(regex, pageoeuvres, re.IGNORECASE) 
            # for matchE in match5:
                
                # nomdeloeuvre = "%s" % (matchE)
                # oeuvresTitle.append(nomdeloeuvre)

            # global oeuvresTitleName   
            # oeuvresTitleName = list()
            # oeuvresURL = list()

            # regex = r"(?<=<a )(.+?)(?=</a>)"
            # if re.findall(regex, pageoeuvres, re.IGNORECASE):
                # for match2 in re.findall(regex, pageoeuvres, re.IGNORECASE):
                    # listederoulanteoeuvres = (match2)
                    # linktextspage.append(listederoulanteoeuvres)
                    # # print "%s" % (match2)   
            # else:

                # print "The regex pattern does not match"

                    
            # # retirer les liens inutiles de la liste 
            # i = 'href="misc.html">The Miscellany'
            # j = 'href="index.html">The Latin Library'
            # k = 'href="/index.html">The Latin Library'
            # l = 'href="classics.html">The Classics Page'
            # result0 = filter(lambda a: a != i, linktextspage)
            # result1 = filter(lambda a: a != j, result0)
            # result2 = filter(lambda a: a != k, result1)
            # result3 = filter(lambda a: a != l, result2)

            # stringtexts = ''.join(result3) 
                          
            # # print stringtexts

            # regex = r"(?<=html\">)(.+?)(?=href)"
            # matches3 = re.findall(regex, stringtexts, re.IGNORECASE)

            # for matchC in matches3:
                # nomduTexte = "%s" % (matchC)
                # oeuvresTitleName.append(nomduTexte)


            # regex = r"(?<=href=\")(.+?)(?=\">)"
            # matches4 = re.findall(regex, stringtexts, re.IGNORECASE)

            # for matchD in matches4:
                # urlTexte = "http://www.thelatinlibrary.com/%s" % (matchD)
                # oeuvresURL.append(urlTexte)        
                    
            # # print result3
            # # self.piece = oeuvresTitleName
            # # print oeuvresTitle
            # # print oeuvresTitleName
            # # print oeuvresURL

    def sendData(self):
        pass
        
    
    def updateGUI(self):
        pass
            
    def commit(self):
        pass
    
#Controleur sur cmd
    
if __name__ == '__main__':
    myApplication = QApplication(sys.argv)
    myWidget = OWLatinText()
    myWidget.show()
    myApplication.exec_()
