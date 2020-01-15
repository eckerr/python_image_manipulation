# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'transform_ui.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PluginGui(object):
    def setupUi(self, PluginGui):
        PluginGui.setObjectName("PluginGui")
        PluginGui.resize(321, 539)
        self.borderTypeCombo = QtWidgets.QComboBox(PluginGui)
        self.borderTypeCombo.setGeometry(QtCore.QRect(100, 340, 211, 22))
        self.borderTypeCombo.setObjectName("borderTypeCombo")
        self.label_border_type = QtWidgets.QLabel(PluginGui)
        self.label_border_type.setGeometry(QtCore.QRect(10, 340, 75, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_border_type.sizePolicy().hasHeightForWidth())
        self.label_border_type.setSizePolicy(sizePolicy)
        self.label_border_type.setObjectName("label_border_type")
        self.interpolationCombo = QtWidgets.QComboBox(PluginGui)
        self.interpolationCombo.setGeometry(QtCore.QRect(100, 420, 211, 22))
        self.interpolationCombo.setObjectName("interpolationCombo")
        self.label_interpolation = QtWidgets.QLabel(PluginGui)
        self.label_interpolation.setGeometry(QtCore.QRect(10, 420, 77, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_interpolation.sizePolicy().hasHeightForWidth())
        self.label_interpolation.setSizePolicy(sizePolicy)
        self.label_interpolation.setObjectName("label_interpolation")
        self.resizeHalfRadio = QtWidgets.QRadioButton(PluginGui)
        self.resizeHalfRadio.setGeometry(QtCore.QRect(10, 40, 323, 20))
        self.resizeHalfRadio.setObjectName("resizeHalfRadio")
        self.remapRadio = QtWidgets.QRadioButton(PluginGui)
        self.remapRadio.setGeometry(QtCore.QRect(10, 160, 323, 20))
        self.remapRadio.setObjectName("remapRadio")
        self.affineRadio = QtWidgets.QRadioButton(PluginGui)
        self.affineRadio.setGeometry(QtCore.QRect(10, 220, 323, 20))
        self.affineRadio.setObjectName("affineRadio")
        self.perspectiveRadio = QtWidgets.QRadioButton(PluginGui)
        self.perspectiveRadio.setGeometry(QtCore.QRect(10, 270, 323, 20))
        self.perspectiveRadio.setObjectName("perspectiveRadio")
        self.resizeDoubleRadio = QtWidgets.QRadioButton(PluginGui)
        self.resizeDoubleRadio.setGeometry(QtCore.QRect(10, 100, 323, 20))
        self.resizeDoubleRadio.setObjectName("resizeDoubleRadio")

        self.retranslateUi(PluginGui)
        QtCore.QMetaObject.connectSlotsByName(PluginGui)

    def retranslateUi(self, PluginGui):
        _translate = QtCore.QCoreApplication.translate
        PluginGui.setWindowTitle(_translate("PluginGui", "Form"))
        self.label_border_type.setText(_translate("PluginGui", "Border Type:"))
        self.label_interpolation.setText(_translate("PluginGui", "Interpolation:"))
        self.resizeHalfRadio.setText(_translate("PluginGui", "Resize (1/2 X)"))
        self.remapRadio.setText(_translate("PluginGui", "Remap"))
        self.affineRadio.setText(_translate("PluginGui", "Affine"))
        self.perspectiveRadio.setText(_translate("PluginGui", "Perspective"))
        self.resizeDoubleRadio.setText(_translate("PluginGui", "Resize (2 X)"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PluginGui = QtWidgets.QWidget()
    ui = Ui_PluginGui()
    ui.setupUi(PluginGui)
    PluginGui.show()
    sys.exit(app.exec_())
