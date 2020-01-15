"""
 pseudo-plugin fine for CV transform functions
  to provide resize, remap, affine, perspective,
  border_type, and interpolation
  Created by Ed on 12/23/2019
 """

import cv2
import numpy as np
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtWidgets

from cvplugins.ui_transform import Ui_PluginGui

class Plugin(QtWidgets.QWidget):

    updateNeeded = pyqtSignal()
    infoMessage = pyqtSignal(str)
    errorMessage = pyqtSignal(str)

    def __init__(self):
        super(Plugin, self).__init__()
        self.title = self.__class__
        self.version = "1.0.0"
        self.description = "transforms an image"
        self.help = ""
        self.ui = None

    def setupUi(self, parent):
        self.ui = Ui_PluginGui()
        self.ui.setupUi(parent)
        items = []
        item_list = ["BORDER_CONSTANT",
                     "BORDER_REPLICATE",
                     "BORDER_REFLECT",
                     "BORDER_WRAP",
                     "BORDER_REFLECT_101"]
        self.ui.borderTypeCombo.addItems(item_list)

        item_list = ["INTER_NEAREST",
                     "INTER_CUBIC",
                     "INTER_AREA",
                     "INTER_LANCZOS4"]
        self.ui.interpolationCombo.addItems(item_list)

        self.ui.resizeHalfRadio.toggled.connect(self.on_resizeHalfRadio_toggled)
        self.ui.resizeDoubleRadio.toggled.connect(self.on_resizeDoubleRadio_toggled)
        self.ui.remapRadio.toggled.connect(self.on_remapRadio_toggled)
        self.ui.affineRadio.toggled.connect(self.on_affineRadio_toggled)
        self.ui.perspectiveRadio.toggled.connect(self.on_perspectiveRadio_toggled)
        self.ui.borderTypeCombo.currentIndexChanged.connect(self.on_borderTypeCombo_currentIndexChanged)
        self.ui.interpolationCombo.currentIndexChanged.connect(self.on_interpolationCombo_currentIndexChanged)

    def processImage(self, inputImage, outputImage):

        width = inputImage.shape[1]
        height = inputImage.shape[0]

        if self.ui.resizeHalfRadio.isChecked():
            outputImage = cv2.resize(inputImage,
                                     None,
                                     fx=.5, fy=.5,
                                     interpolation=self.ui.interpolationCombo.currentIndex())

        elif self.ui.resizeDoubleRadio.isChecked():
            outputImage = cv2.resize(inputImage,
                                     None,
                                     fx=2, fy=2,
                                     interpolation=self.ui.interpolationCombo.currentIndex())

        elif self.ui.remapRadio.isChecked():
            map_x = np.empty([height, width], np.float32)
            map_y = np.empty([height, width], np.float32)
            print(type(map_x), map_x.size, map_x.shape)
            for row in range(height):
                for col in range(width):
                    map_x[row, col] = width-1 - col
                    map_y[row, col] = row
            outputImage = cv2.remap(inputImage,
                                    map_x,
                                    map_y,
                                    self.ui.interpolationCombo.currentIndex())

        elif self.ui.affineRadio.isChecked():
            cols = width
            rows = height
            pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
            pts2 = np.float32([[10, 100], [200, 50], [100, 250]])
            affine_mat = cv2.getAffineTransform(pts1, pts2)
            print("affine mat type: ", type(affine_mat))

            outputImage = cv2.warpAffine(inputImage,
                                         affine_mat,
                                         (cols, rows),
                                         self.ui.borderTypeCombo.currentIndex(),
                                         self.ui.interpolationCombo.currentIndex())

        elif self.ui.perspectiveRadio.isChecked():
            cols = width
            rows = height
            pts1 = np.float32([[56, 65], [368, 52], [28, 387], [389, 390]])
            pts2 = np.float32([[0, 0], [300, 0], [0, 300], [300, 300]])
            perspective_mat = cv2.getPerspectiveTransform(pts1, pts2)

            outputImage = cv2.warpPerspective(inputImage,
                                              perspective_mat,
                                              (cols, rows),
                                              self.ui.borderTypeCombo.currentIndex(),
                                              self.ui.interpolationCombo.currentIndex())
        return outputImage

    def on_resizeHalfRadio_toggled(self):
        self.updateNeeded.emit()

    def on_resizeDoubleRadio_toggled(self):
        self.updateNeeded.emit()

    def on_remapRadio_toggled(self):
        self.updateNeeded.emit()

    def on_affineRadio_toggled(self):
        self.updateNeeded.emit()

    def on_perspectiveRadio_toggled(self):
        self.updateNeeded.emit()

    def on_interpolationCombo_currentIndexChanged(self, int):
        print('box value when updateNeeded sent: ', int)
        self.updateNeeded.emit()

    def on_borderTypeCombo_currentIndexChanged(self, int):
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
