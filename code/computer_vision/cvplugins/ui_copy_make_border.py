# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plugin.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PluginGui(object):
    def setupUi(self, PluginGui):
        PluginGui.setObjectName("PluginGui")
        PluginGui.resize(320, 207)
        self.gridLayout = QtWidgets.QGridLayout(PluginGui)
        self.gridLayout.setObjectName("gridLayout")
        self.borderTypeLabel = QtWidgets.QLabel(PluginGui)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.borderTypeLabel.sizePolicy().hasHeightForWidth())
        self.borderTypeLabel.setSizePolicy(sizePolicy)
        self.borderTypeLabel.setObjectName("borderTypeLabel")
        self.gridLayout.addWidget(self.borderTypeLabel, 0, 0, 1, 1)
        self.borderTypeComboBox = QtWidgets.QComboBox(PluginGui)
        self.borderTypeComboBox.setObjectName("borderTypeComboBox")
        self.gridLayout.addWidget(self.borderTypeComboBox, 0, 1, 1, 1)

        self.retranslateUi(PluginGui)
        QtCore.QMetaObject.connectSlotsByName(PluginGui)

    def retranslateUi(self, PluginGui):
        _translate = QtCore.QCoreApplication.translate
        PluginGui.setWindowTitle(_translate("PluginGui", "Form"))
        self.borderTypeLabel.setText(_translate("PluginGui", "Border Type :"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PluginGui = QtWidgets.QWidget()
    ui = Ui_PluginGui()
    ui.setupUi(PluginGui)
    PluginGui.show()
    sys.exit(app.exec_())
