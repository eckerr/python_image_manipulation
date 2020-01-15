"""
 pseudo-plugin for CV segmentation functions

  Created by Ed on 12/23/2019
 """

import cv2
import numpy as np
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtWidgets

from cvplugins.ui_segmentation import Ui_PluginGui

class Plugin(QtWidgets.QWidget):

    updateNeeded = pyqtSignal()
    infoMessage = pyqtSignal(str)
    errorMessage = pyqtSignal(str)


    def __init__(self):
        super(Plugin, self).__init__()
        self.title = self.__class__
        self.version = "1.0.0"
        self.description = "segments an image"
        self.help = ""
        self.ui = None

    def setupUi(self, parent):
        self.ui = Ui_PluginGui()
        self.ui.setupUi(parent)
        item_list = ["ADAPTIVE_THRESH_MEAN_C",
                     "ADAPTIVE_THRESH_GAUSSIAN_C"]

        self.ui.threshAdaptiveCombo.addItems(item_list)

        item_list = ["THRESH_BINARY",
                     "THRESH_BINARY_INV",
                     "THRESH_TRUNC",
                     "THRESH_TOZERO",
                     "THRESH_TOZERO_INV"]
        self.ui.threshTypeCombo.addItems(item_list)

        self.ui.threshAdaptiveCheck.toggled.connect(self.on_threshAdaptiveCheck_toggled)
        self.ui.threshAdaptiveCombo.currentIndexChanged.connect(self.on_threshAdaptiveCombo_currentIndexChanged)
        self.ui.threshTypeCombo.currentIndexChanged.connect(self.on_threshTypeCombo_currentIndexChanged)
        self.ui.threshSlider.valueChanged.connect(self.on_threshSlider_valueChanged)
        self.ui.threshMaxSlider.valueChanged.connect(self.on_threshMaxSlider_valueChanged)

    def processImage(self, inputImage, outputImage):

        gray_scale = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)
        print("gray_scale type: ", type(gray_scale))

        if self.ui.threshAdaptiveCheck.isChecked():
            gray_scale = cv2.adaptiveThreshold(gray_scale,
                                               gray_scale,
                                               self.ui.threshMaxSlider.value(),
                                               self.ui.threshAdaptiveCombo.currentIndex(),
                                               self.ui.threshTypeCombo.currentIndex(),
                                               7)
        else:
            print("threshSlider: ", self.ui.threshSlider.value())
            print("threshMaxSlider: ", self.ui.threshMaxSlider.value())
            print("threshTypeCombo: ", self.ui.threshTypeCombo.currentIndex())
            outputImage = cv2.threshold(gray_scale,
                                       self.ui.threshSlider.value(),
                                       self.ui.threshMaxSlider.value(),
                                       self.ui.threshTypeCombo.currentIndex())


        # return cv2.cvtColor(gray_scale, cv2.COLOR_GRAY2BGR)
        return outputImage

    def on_threshAdaptiveCheck_toggled(self):
        self.updateNeeded.emit()

    def on_threshAdaptiveCombo_currentIndexChanged(self):
         self.updateNeeded.emit()

    def on_threshTypeCombo_currentIndexChanged(self):
        self.updateNeeded.emit()

    def on_threshSlider_valueChanged(self, value):
        str_val = str(value)
        self.infoMessage.emit('value: ' + str_val)
        self.updateNeeded.emit()

    def on_threshMaxSlider_valueChanged(self, value):
        str_val = str(value)
        self.infoMessage.emit('max value: ' + str_val)
        self.updateNeeded.emit()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    pluginGui = QtWidgets.QWidget()
    ui = Ui_pluginGui()
    ui.setupUi(pluginGui)
    pluginGui.show()
    sys.exit(app.exec_())
