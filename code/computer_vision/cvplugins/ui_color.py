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
        PluginGui.resize(319, 530)
        self.gridLayout = QtWidgets.QGridLayout(PluginGui)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(PluginGui)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.colorMapCombo = QtWidgets.QComboBox(PluginGui)
        self.colorMapCombo.setObjectName("colorMapCombo")
        self.gridLayout.addWidget(self.colorMapCombo, 0, 1, 1, 1)

        self.retranslateUi(PluginGui)
        QtCore.QMetaObject.connectSlotsByName(PluginGui)

    def retranslateUi(self, PluginGui):
        _translate = QtCore.QCoreApplication.translate
        PluginGui.setWindowTitle(_translate("PluginGui", "Form"))
        self.label.setText(_translate("PluginGui", "Color Maps :"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PluginGui = QtWidgets.QWidget()
    ui = Ui_PluginGui()
    ui.setupUi(PluginGui)
    PluginGui.show()
    sys.exit(app.exec_())
