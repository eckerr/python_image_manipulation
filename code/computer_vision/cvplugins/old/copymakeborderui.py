# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'copy_make_border_pi.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_pluginGui(object):
    def setupUi(self, pluginGui):
        pluginGui.setObjectName("pluginGui")
        pluginGui.resize(400, 300)
        self.comboBox = QtWidgets.QComboBox(pluginGui)
        self.comboBox.setGeometry(QtCore.QRect(220, 150, 73, 22))
        self.comboBox.setObjectName("comboBox")
        self.label = QtWidgets.QLabel(pluginGui)
        self.label.setGeometry(QtCore.QRect(50, 150, 55, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")

        self.retranslateUi(pluginGui)
        QtCore.QMetaObject.connectSlotsByName(pluginGui)

        items = []
        items.append("BORDER_CONSTANT")
        items.append("BORDER_REPLICATE")
        items.append("BORDER_REFLECT")
        items.append("BORDER_WRAP")
        items.append("BORDER_REFLECT_101")
        self.comboBox.addItems(items)
        self.comboBox.currentIndexChanged.connect(self.update_needed)

    def update_needed(self):
        print("update_needed triggered")
        MainWindow.ui.process_image()


    def retranslateUi(self, pluginGui):
        _translate = QtCore.QCoreApplication.translate
        pluginGui.setWindowTitle(_translate("pluginGui", "Form"))
        self.label.setText(_translate("pluginGui", "TextLabel"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    pluginGui = QtWidgets.QWidget()
    ui = Ui_pluginGui()
    ui.setupUi(pluginGui)
    pluginGui.show()
    sys.exit(app.exec_())
