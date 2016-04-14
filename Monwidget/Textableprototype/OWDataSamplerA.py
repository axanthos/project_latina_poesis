"""<name>Latina Poesis</name>
<description>Versifies a Latin text with the CLTK</description>
<icon>LatinaPoesis.svg</icon>
<priority>10</priority>"""

import Orange
from OWWidget import *
import OWGUI

class OWDataSamplerA(OWWidget):
    
    def __init__(self, parent=None, signalManager=None):
        OWWidget.__init__(self, parent, signalManager)

        self.inputs = [("Data", Orange.data.Table, self.set_data)]
        self.outputs = [("Versified Data", Orange.data.Table)]

        #variables definitions
        authors = [get.ElementById]
        pieces = []
        # GUI
        box = OWGUI.widgetBox(self.controlArea, "Info")
        self.infoa = OWGUI.widgetLabel(box, 'No data on input yet, waiting to get something.')
        self.infob = OWGUI.widgetLabel(box, '')
        self.resize(100,50)

        OWGUI.separator(self.controlArea)
        self.optionsBox = OWGUI.widgetBox(self.controlArea, "Options")
        #list authors
        OWGUI.listBox(self.optionsBox, self, 'author', labels=authors,
                 callback=[self.selection, self.checkCommit])
        #list pieces
        OWGUI.listBox(self.optionsBox, self, 'piece', labels=pieces,
                 callback=[self.selection, self.checkCommit])
        #radio replic or verse
        OWGUI.radioButtonsInBox(self.optionsBox, self, value='sizeofinterest', btnLabels=["replic","verse"], callback=self.commit)
        self.optionsBox.setDisabled(True)
        #line number
        OWGUI.spin(self.optionsBox, self, 'linenumber', min=1, max=max, step=1,
                   label='Line number', callback=[self.selection, self.checkCommit])
        #output name
        OWGUI.
        #button apply choices
        OWGUI.button(self.optionsBox, self, "applyversification", callback=self.commit)
        self.optionsBox.setDisabled(True)
        
    
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