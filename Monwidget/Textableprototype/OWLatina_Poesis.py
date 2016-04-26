"""<name>Latina_Poesis</name>
<description>Select a Latin text from thelatinlibrary.com</description>
<icon>Latina_Poesis.svg</icon>
<priority>10</priority>"""

import Orange
from OWWidget import *
import OWGUI

from _textable.widgets.LTTL.Segmentation import Segmentation
from _textable.widgets.LTTL.Input import Input
from _textable.widgets.LTTL.Segmenter import Segmenter

from _textable.widgets.TextableUtils import *   # Provides several utilities.

import urllib2
import re
import inspect
import os
import pickle

settingsList = [
        'autoSend',
        'label',
        'uuid',
        'linenumber',
        'sizeofinterest',
        'piece',
        'author',
        'displayAdvancedSettings',
    ]
class OWLatina_Poesis(OWWidget):

    def __init__(self, parent=None, signalManager=None):
        OWWidget.__init__(self, parent, signalManager, wantMainArea=0)

        self.inputs = [("Data", Orange.data.Table, self.set_data)]
        self.outputs = [("Versified Data", Orange.data.Table)]

        #variables definitions
        self.autoSend = True
        self.label = u'xml_tei_data'
        self.linenumber = None
        #[get.ElementByAnnotations_seg1]
        self.author = list()
        #[get.ElementByAnnotations_seg2]
        self.piece = list()
        self.displayAdvancedSettings = False
        self.uuid = None
        self.loadSettings()
        self.uuid = getWidgetUuid(self)
        

        self.segmenter = Segmenter()
        self.segmentation = Input()
        self.titleSeg = None
        self.base_url =     \
          'https://github.com/cltk/latin_text_latin_library/nomdelauteur'
        self.document_base_url =     \
          'https://github.com/cltk/latin_text_latin_library'

        self.infoBox = InfoBox(widget=self.controlArea)
        self.sendButton = SendButton(
            widget=self.controlArea,
            master=self,
            callback=self.sendData,
            infoBoxAttribute='infoBox',
            sendIfPreCallback=self.updateGUI,
        )
        # GUI
        box = OWGUI.widgetBox(self.controlArea, "Info")
        self.infoa = OWGUI.widgetLabel(box, 'No data on input yet, waiting to get something.')
        self.infob = OWGUI.widgetLabel(box, '')
        self.resize(100,50)

        OWGUI.separator(self.controlArea)
        self.optionsBox = OWGUI.widgetBox(self.controlArea, "Options")

        #list authors
        OWGUI.listBox(
            self.optionsBox,
            self,
            'author',
            labels='author',
            callback=[
                self.selection,
                self.checkCommit,
                self.sendButton.settingsChanged
            ]
        )
        #list pieces
        OWGUI.listBox(
            self.optionsBox,
            self,
            'piece',
            labels='piece',
            callback=[
                self.selection,
                self.checkCommit,
                self.sendButton.settingsChanged
            ]
        )
        #radio replic or verse
        #OWGUI.radioButtonsInBox(
         #   self.optionsBox,
          #  self,
           # !!!!!!value!!!!!!!,
            #btnLabels=["replic","verse"],
            #callback=[
             #   self.optionsBox.setDisabled(True),
              #  self.commit,
               # self.sendButton.settingsChanged
           # ]
            
        #)
        #line number
        #OWGUI.spin(
        #    self.optionsBox,
        #    self,
        #    'linenumber',
        #    min=1,
        #    max=2,
        #    step=1,
        #    label='Line number',
        #    callback=[
        #        self.selection,
        #        self.checkCommit,
        #        self.sendButton.settingsChanged
        #    ]
        #)
        #output name
        #OWGUI.
        #button apply choices
        OWGUI.button(
            self.optionsBox,
            self,
            "applyversification",
            callback=[
                self.optionsBox.setDisabled(True),
                self.commit,
                self.sendButton.settingsChanged
            ]
            
        )

    
    def set_data(self, dataset):
        if dataset is not None:
            self.infoa.setText('%d instances in input data set' % len(dataset))
            indices = Orange.data.versified.SubsetIndices2(p0=0.1)
            ind = indices(dataset)
            versified = dataset.select(ind, 0)
            self.infob.setText('%d versified instances' % len(versified))
            self.send("Versified Data", versified)
        else:
            self.infoa.setText('No data on input yet, waiting to get something.')
            self.infob.setText('')
            self.send("Versified Data", None)
    def sendData(self):
        pass
        
    def updateGUI(self):
        pass
    
    def selection(self):
        pass
        
    def checkCommit(self):
        pass
    
    def commit(self):
        pass
    
        
if __name__ == '__main__':
    myApplication = QApplication(sys.argv)
    myWidget = OWLatina_Poesis()
    myWidget.show()
    myApplication.exec_()
