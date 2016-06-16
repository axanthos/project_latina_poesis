"""
<name>Latina Poesis</name>
<description>Import XML-TEI data from Theatre-classique website</description>
<icon>path_to_icon.svg</icon>
<priority>10</priority>
"""

__version__ = u'0.0.1'

import Orange
from OWWidget import *
import OWGUI

from _textable.widgets.LTTL.Segmentation import Segmentation
from _textable.widgets.LTTL.Input import Input
from _textable.widgets.LTTL.Segmenter import Segmenter
from _textable.widgets.LTTL.Processor import Processor

from _textable.widgets.TextableUtils import *   # Provides several utilities.

import urllib2
import re
import inspect
import os
import pickle


class OWTextableTheatreClassique(OWWidget):
    """Orange widget for importing XML-TEI data from the Theatre-classique
    website (http://github.com/cltk/)
    """

    # Widget settings declaration...
    settingsList = [
        u'autoSend',
        u'label',
        u'uuid',
        u'selectedTitles',
        u'filterCriterion',
        u'filterValue',
        u'importedURLs',
        u'displayAdvancedSettings',
    ]

    def __init__(self, parent=None, signalManager=None):
        """Widget creator."""

        # Standard call to creator of base class (OWWidget).
        OWWidget.__init__(self, parent, signalManager, wantMainArea=0)

        # Channel definitions...
        self.inputs = []
        self.outputs = [('Text data', Segmentation)]

        # Settings initializations...
        self.autoSend = True
        self.label = u'xml_tei_data'
        self.filterCriterion = u'author'
        self.filterValue = u'(all)'
        self.titleLabels = list()
        self.selectedTitles = list()
        self.importedURLs = list()
        self.displayAdvancedSettings = False

        # Always end Textable widget settings with the following 3 lines...
        self.uuid = None
        self.loadSettings()
        self.uuid = getWidgetUuid(self)

        # Other attributes...
        self.segmenter = Segmenter()
        self.processor = Processor()
        self.segmentation = Input()
        self.titleSeg = None
        self.filteredTitleSeg = None
        self.filterValues = dict()
        self.base_url =     \
          u'http://github.com/cltk/latin_text_latin_library/'
        self.document_base_url =     \
          u'http://github.com/cltk/latin_text_latin_library/'

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

        # The AdvancedSettings class, also from TextableUtils, facilitates
        # the management of basic vs. advanced interface. An object from this 
        # class (here assigned to self.advancedSettings) contains two lists 
        # (basicWidgets and advanceWidgets), to which the corresponding
        # widgetBoxes must be added.
        self.advancedSettings = AdvancedSettings(
            widget=self.controlArea,
            master=self,
            callback=self.updateFilterValueList,
        )
        self.selectBox = OWGUI.widgetBox(
                widget              = self.controlArea,
                box                 = u'Select',
                orientation         = 'vertical',
        )
        self.sampleBox = OWGUI.widgetBox(
                widget              = self.selectBox,
                orientation         = 'vertical',
        )
        # User interface...

        # Advanced settings checkbox (basic/advanced interface will appear 
        # immediately after it...
        self.advancedSettings.draw()

        # Filter box (advanced settings only)
        filterBox = OWGUI.widgetBox(
            widget=self.controlArea,
            box=u'Filter',
            orientation=u'vertical',
        ) 
        
        OWGUI.separator(widget=filterBox, height=3)
        
        # The following lines add filterBox (and a vertical separator) to the
        # advanced interface...
        self.advancedSettings.advancedWidgets.append(filterBox)
        self.advancedSettings.advancedWidgetsAppendSeparator()

        # Title box
        titleBox = OWGUI.widgetBox(
            widget=self.controlArea,
            box=u'Titles',
            orientation=u'vertical',
        )
        CriterionCombo = OWGUI.comboBox(
            widget=titleBox,
            master=self,
            value=u'filterValue',
            sendSelectedValue=True,
            orientation=u'horizontal',
            label=u'Author:',
            labelWidth=180,
            callback=self.updateFilterValueList,
            tooltip=(
                u"Tool\n"
                u"tips."
            ),
        )
        CriterionCombo.setMinimumWidth(120)
        OWGUI.separator(widget=filterBox, height=3)
        self.filterValueCombo = OWGUI.comboBox(
            widget=titleBox,
            master=self,
            value=u'filterValue',
            sendSelectedValue=True,
            orientation=u'horizontal',
            label=u'Piece:',
            labelWidth=180,
            callback=self.updateTitleList,
            tooltip=(
                u"Tool\n"
                u"tips."
            ),
        )
        self.titleListbox = OWGUI.listBox(
            widget=titleBox,
            master=self,
            value=u'selectedTitles',    # setting (list)
            labels=u'titleLabels',      # setting (list)
            callback=self.sendButton.settingsChanged,
            tooltip=u"The list of titles whose content will be imported",
        )
        self.titleListbox.setMinimumHeight(150)
        self.titleListbox.setSelectionMode(3)
        OWGUI.separator(widget=titleBox, height=3)
        OWGUI.button(
            widget=titleBox,
            master=self,
            label=u'Refresh',
            callback=self.refreshTitleSeg,
            tooltip=u"Connect to Theatre-classique website and refresh list.",
        )
        # OWGUI.spin(
                # widget              = self.sampleBox,
                # master              = self,
                # value               = 'samplingRate',
                # min                 = 1,
                # max                 = 1,
                # orientation         = 'horizontal',
                # label               = u'Sampling rate (%):',
                # labelWidth          = 180,
                # callback            = self.sendButton.settingsChanged,
                # tooltip             = (
                        # u"The proportion of segments that will be sampled."
                # ),
        # )
        OWGUI.separator(widget=titleBox, height=3)

        OWGUI.separator(widget=self.controlArea, height=3)

        # From TextableUtils: a minimal Options box (only segmentation label).
        basicOptionsBox = BasicOptionsBox(self.controlArea, self)
 
        OWGUI.separator(widget=self.controlArea, height=3)

        # Now Info box and Send button must be drawn...
        self.infoBox.draw()
        self.sendButton.draw()
        
        # This initialization step needs to be done after infoBox has been 
        # drawn (because getTitleSeg may need to display an error message).
        self.getTitleSeg()

        # Send data if autoSend.
        self.sendButton.sendIf()

    def sendData(self):
        """Compute result of widget processing and send to output"""

        # Skip if title list is empty:
        if self.titleLabels == list():
            return
        
        # Check that something has been selected...
        if len(self.selectedTitles) == 0:
            self.infoBox.noDataSent(u': no title selected.')
            self.send(u'Text data', None, self)
            return

        # Check that label is not empty...
        if not self.label:
            self.infoBox.noDataSent(warning=u'No label was provided.')
            self.send(u'Text data', None, self)
            return

        # Attempt to connect to Theatre-classique...
        try:
            response = urllib2.urlopen(
                self.document_base_url + 
                self.filteredTitleSeg[
                    self.selectedTitles[0]
                ].annotations[u'url']
            )
            xml_content = unicode(response.read(), u'utf8')

        # If unable to connect (somehow)...
        except:

            # Set Info box and widget to 'error' state.
            self.infoBox.noDataSent(
                error=u"Couldn't access theatre-classique website."
            )

            # Reset output channel.
            self.send(u'Text data', None, self)
            return
            
        # Store downloaded XML in segmentation attribute.
        self.segmentation.update(text=xml_content, label=self.label)

        # Store imported URLs as setting.
        self.importedURLs = [
            self.filteredTitleSeg[self.selectedTitles[0]].annotations[u'url']
        ]
        
        # Set status to OK...
        message = u'1 segment (%i character@p).' % len(xml_content)
        message = pluralize(message, len(xml_content))
        self.infoBox.dataSent(message)

        # Send token...
        self.send(u'Text data', self.segmentation, self)
        self.sendButton.resetSettingsChangedFlag()        
        
    def getTitleSeg(self):
        """Get title segmentation, either saved locally or online"""
        
        # Try to open saved file in this module's directory...
        path = os.path.dirname(
            os.path.abspath(inspect.getfile(inspect.currentframe()))
        )
        try:
            file = open(os.path.join(path, "cached_title_list"),'r')
            self.titleSeg = pickle.load(file)
            file.close()
        # Else try to load list from Theatre-classique and build new seg...
        except IOError:
            self.titleSeg = self.getTitleListFromTheatreClassique()

        # Build author list...
        if self.titleSeg is not None:
            self.filterValues[u'author'] = self.processor.count_in_context(
                units={
                    u'segmentation': self.titleSeg, 
                    u'annotation_key': u'author'
                }
            ).col_ids
            self.filterValues[u'author'].sort()

        # Update title and filter value lists (only at init and on manual
        # refresh, therefore separate from self.updateGUI).
        self.updateFilterValueList()
                    
    def refreshTitleSeg(self):
        """Refresh title segmentation from website"""
        self.titleSeg = self.getTitleListFromTheatreClassique()
        # Update title and filter value lists (only at init and on manual
        # refresh, therefore separate from self.updateGUI).
        self.updateFilterValueList()
        
    def getTitleListFromTheatreClassique(self):
        """Fetch titles from the Theatre-classique website"""

        self.infoBox.customMessage(
            u'Fetching data from Theatre-classique website, please wait'
        )
        
        # Attempt to connect to Theatre-classique...
        try:
            response = urllib2.urlopen(self.base_url)
            base_html = unicode(response.read(), 'iso-8859-1')
            self.infoBox.customMessage(
                u'Done fetching data from Theatre-classique website.'
            )

        # If unable to connect (somehow)...
        except:

            # Set Info box and widget to 'warning' state.
            self.infoBox.noDataSent(
                warning=u"Couldn't access theatre-classique website."
            )

            # Empty title list box.
            self.titleLabels = list()

            # Reset output channel.
            self.send(u'Text data', None, self)
            return None
            
        # Otherwise store HTML content in LTTL Input object.
        base_html_seg = Input(base_html)

        # Extract table containing titles from HTML.
        table_seg = self.segmenter.import_xml(
            segmentation=base_html_seg,
            element=u'table',
            conditions={u'title': re.compile(ur'^table_AA$')},
            remove_markup=False,
        )

        # Extract table lines.
        line_seg = self.segmenter.import_xml(
            segmentation=table_seg,
            element=u'tr',
            remove_markup=False,
        )

        # Compile the regex that will be used to parse each line.
        field_regex = re.compile(
            ur"^\s*<tr class=\"js-navigation-item\">(.+?)\s*<a.+?>\s*(.+?)\s*</a>\s*</span>\s*(.+?)</tr>\s*"  
        )

        # Parse each line and store the resulting segmentation in an attribute.
        titleSeg = self.segmenter.tokenize(
            segmentation=line_seg,
            regexes=[
                (field_regex, u'Tokenize', {u'author': u'&2'})               
            ],
            import_annotations=False,
        )

        # Sort this segmentation alphabetically based on author...
        titleSeg.segments.sort(key=lambda s: s.annotations[u'author'])
        
        # Try to save list in this module's directory for future reference...
        path = os.path.dirname(
            os.path.abspath(inspect.getfile(inspect.currentframe()))
        )
        try:
            file = open(os.path.join(path, u"cached_title_list"), u'wb')
            pickle.dump(titleSeg, file) 
            file.close()         
        except IOError:
            pass

        # Remove warning (if any)...
        self.error(0)
        self.warning(0)
        
        return titleSeg

    def updateFilterValueList(self):
        """Update the list of filter values"""
        
        # In Advanced settings mode, populate filter value list...
        if self.titleSeg is not None and self.displayAdvancedSettings:
            self.filterValueCombo.clear()
            self.filterValueCombo.addItem(u'(all)')
            for filterValue in self.filterValues[self.filterCriterion]:
                self.filterValueCombo.addItem(filterValue)

        # Reset filterValue if needed...
        if self.filterValue not in [
            unicode(self.filterValueCombo.itemText(i)) 
            for i in xrange(self.filterValueCombo.count())
        ]:
            self.filterValue = u'(all)'
        else:
            self.filterValue = self.filterValue
        
        self.updateTitleList()

    def updateTitleList(self):
        """Update the list of titles"""
        
        # If titleSeg has not been loaded for some reason, skip.
        if self.titleSeg is None:
            return
        
        # In Advanced settings mode, get list of selected titles...
        if self.displayAdvancedSettings and self.filterValue != u'(all)':
            self.filteredTitleSeg, _ = self.segmenter.select(
                segmentation=self.titleSeg,
                regex=re.compile(ur'^%s$' % self.filterValue),
                annotation_key=self.filterCriterion,
            )
        else:
            self.filteredTitleSeg = self.titleSeg
        
        # Populate titleLabels list with the titles...
        self.titleLabels = sorted(
            [s.annotations[u'title'] for s in self.filteredTitleSeg]
        )
        
        # Add author when title is duplicated (unless criterion is 'author')...
        if (self.filterCriterion != u'author' or self.filterValue == u'(all)'):
            titleLabels = self.titleLabels[:]
            for idx in xrange(len(titleLabels)):
                titleLabel = titleLabels[idx]
                if self.titleLabels.count(titleLabel) > 1:
                    author = self.filteredTitleSeg[idx].annotations[u'author']
                    titleLabels[idx] = titleLabel + " (%s)" % author
            self.titleLabels = titleLabels
        
        # Reset selectedTitles if needed...
        if not set(self.importedURLs).issubset(
            set(u.annotations[u'url'] for u in self.filteredTitleSeg)
        ):
            self.selectedTitles = list()
        else:
            self.selectedTitles = self.selectedTitles

        self.sendButton.settingsChanged()

    def updateGUI(self):
        """Update GUI state"""
        if self.displayAdvancedSettings:
            self.advancedSettings.setVisible(True)
        else:
            self.advancedSettings.setVisible(False)
            
        if len(self.titleLabels) > 0:
            self.selectedTitles = self.selectedTitles
            
    def onDeleteWidget(self):
        """Make sure to delete the stored segmentation data when the widget
        is deleted (overriden method)
        """
        self.segmentation.clear()

    # The following two methods need to be copied (without any change) in
    # every Textable widget...

    def getSettings(self, *args, **kwargs):
        """Read settings, taking into account version number (overriden)"""
        settings = OWWidget.getSettings(self, *args, **kwargs)
        settings["settingsDataVersion"] = __version__.split('.')[:2]
        return settings

    def setSettings(self, settings):
        """Write settings, taking into account version number (overriden)"""
        if settings.get("settingsDataVersion", None) \
                == __version__.split('.')[:2]:
            settings = settings.copy()
            del settings["settingsDataVersion"]
            OWWidget.setSettings(self, settings)


if __name__ == '__main__':
    myApplication = QApplication(sys.argv)
    myWidget = OWTextableTheatreClassique()
    myWidget.show()
    myApplication.exec_()