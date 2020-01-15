"""
 pseudo-plugin fine for CV copyMakeBorder function
  Created by Ed on 11/27/2019
 """

import cv2
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtWidgets

# from copy_make_border_ui import Ui_PluginGui
from cvplugins.ui_copy_make_border import Ui_PluginGui

class Plugin(QtWidgets.QWidget):

    updateNeeded = pyqtSignal()
    infoMessage = pyqtSignal(str)
    errorMessage = pyqtSignal(str)


    def __init__(self):
        # super.__init__()
        super(Plugin, self).__init__()
        self.title = self.__class__
        self.version = "1.0.0"
        self.description = "add border to image"
        self.help = ""
        self.ui = None

    def setupUi(self, parent):
        self.ui = Ui_PluginGui()
        self.ui.setupUi(parent)
        items = []
        items.append("BORDER_CONSTANT")
        items.append("BORDER_REPLICATE")
        items.append("BORDER_REFLECT")
        items.append("BORDER_WRAP")
        items.append("BORDER__101")
        self.ui.borderTypeComboBox.addItems(items)
        self.ui.borderTypeComboBox.currentIndexChanged.connect(self.on_borderTypeComboBox_currentIndexChanged)

    def processImage(self, inputImage, outputImage):
        topval = botval = inputImage.shape[0]//2
        leftval = rightval = inputImage.shape[1]//2
        current_index = self.ui.borderTypeComboBox.currentIndex()
        outputImage = cv2.copyMakeBorder(inputImage,
                                         top=2,
                                         bottom=2,
                                         left=2,
                                         right=2,
                                         borderType=current_index,
                                         value=[255, 0, 0])
        return outputImage

    def on_borderTypeComboBox_currentIndexChanged(self):
        self.updateNeeded.emit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    pluginGui = QtWidgets.QWidget()
    ui = Ui_pluginGui()
    ui.setupUi(pluginGui)
    pluginGui.show()
    sys.exit(app.exec_())
