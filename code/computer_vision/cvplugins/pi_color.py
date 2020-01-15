"""
 pseudo-plugin fine for CV color function to provide pseudo-coloring of image
  Created by Ed on 12/23/2019
 """

import cv2
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtWidgets

from cvplugins.ui_color import Ui_PluginGui

class Plugin(QtWidgets.QWidget):

    updateNeeded = pyqtSignal()
    infoMessage = pyqtSignal(str)
    errorMessage = pyqtSignal(str)

    def __init__(self):
        super(Plugin, self).__init__()
        self.title = self.__class__
        self.version = "1.0.0"
        self.description = "pseudo-color an image"
        self.help = ""
        self.ui = None

    def setupUi(self, parent):
        self.ui = Ui_PluginGui()
        self.ui.setupUi(parent)
        items = []
        item_list = ["COLORMAP_AUTUMN",
                     "COLORMAP_BONE",
                     "COLORMAP_JET",
                     "COLORMAP_WINTER",
                     "COLORMAP_RAINBOW",
                     "COLORMAP_OCEAN",
                     "COLORMAP_SUMMER",
                     "COLORMAP_SPRING",
                     "COLORMAP_COOL",
                     "COLORMAP_HSV",
                     "COLORMAP_PINK",
                     "COLORMAP_HOT",
                     "COLORMAP_PARULA"]
        self.ui.colorMapCombo.addItems(item_list)
        self.ui.colorMapCombo.currentIndexChanged.connect(self.on_colorMapCombo_currentIndexChanged)

    def processImage(self, inputImage, outputImage):
        current_index = self.ui.colorMapCombo.currentIndex()
        before_shape = outputImage.shape
        outputImage = cv2.applyColorMap(inputImage, current_index)
        return outputImage

    def on_colorMapCombo_currentIndexChanged(self, int):
        print('box value when updateNeeded sent: ', int)
        self.updateNeeded.emit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    pluginGui = QtWidgets.QWidget()
    ui = Ui_pluginGui()
    ui.setupUi(pluginGui)
    pluginGui.show()
    sys.exit(app.exec_())
