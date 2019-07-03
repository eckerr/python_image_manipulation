# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\newimagedlg.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_new_image_dlg(object):
    def setupUi(self, new_image_dlg):
        new_image_dlg.setObjectName("new_image_dlg")
        new_image_dlg.resize(344, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(new_image_dlg)
        self.buttonBox.setGeometry(QtCore.QRect(50, 240, 261, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(new_image_dlg)
        self.label.setGeometry(QtCore.QRect(50, 30, 55, 16))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(new_image_dlg)
        self.label_2.setGeometry(QtCore.QRect(50, 70, 55, 16))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.width_spinBox = QtWidgets.QSpinBox(new_image_dlg)
        self.width_spinBox.setGeometry(QtCore.QRect(120, 30, 81, 22))
        self.width_spinBox.setMinimum(32)
        self.width_spinBox.setMaximum(4096)
        self.width_spinBox.setObjectName("width_spinBox")
        self.height_spinbox = QtWidgets.QSpinBox(new_image_dlg)
        self.height_spinbox.setGeometry(QtCore.QRect(120, 70, 81, 22))
        self.height_spinbox.setMinimum(32)
        self.height_spinbox.setMaximum(4096)
        self.height_spinbox.setObjectName("height_spinbox")
        self.brush_pattern_comboBox = QtWidgets.QComboBox(new_image_dlg)
        self.brush_pattern_comboBox.setGeometry(QtCore.QRect(120, 130, 191, 22))
        self.brush_pattern_comboBox.setObjectName("brush_pattern_comboBox")
        self.label_3 = QtWidgets.QLabel(new_image_dlg)
        self.label_3.setGeometry(QtCore.QRect(24, 130, 81, 20))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(new_image_dlg)
        self.label_4.setGeometry(QtCore.QRect(50, 180, 55, 16))
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.color_label_pic = QtWidgets.QLabel(new_image_dlg)
        self.color_label_pic.setGeometry(QtCore.QRect(120, 180, 91, 31))
        self.color_label_pic.setText("")
        self.color_label_pic.setObjectName("color_label_pic")
        self.color_pushButton = QtWidgets.QPushButton(new_image_dlg)
        self.color_pushButton.setGeometry(QtCore.QRect(220, 180, 93, 28))
        self.color_pushButton.setObjectName("color_pushButton")
        self.label.setBuddy(self.width_spinBox)
        self.label_2.setBuddy(self.height_spinbox)
        self.label_3.setBuddy(self.brush_pattern_comboBox)

        self.retranslateUi(new_image_dlg)
        self.buttonBox.accepted.connect(new_image_dlg.accept)
        self.buttonBox.rejected.connect(new_image_dlg.reject)
        QtCore.QMetaObject.connectSlotsByName(new_image_dlg)

    def retranslateUi(self, new_image_dlg):
        _translate = QtCore.QCoreApplication.translate
        new_image_dlg.setWindowTitle(_translate("new_image_dlg", "New Image"))
        self.label.setText(_translate("new_image_dlg", "Width:"))
        self.label_2.setText(_translate("new_image_dlg", "Height:"))
        self.label_3.setText(_translate("new_image_dlg", "Brush Pattern:"))
        self.label_4.setText(_translate("new_image_dlg", "Color:"))
        self.color_pushButton.setText(_translate("new_image_dlg", "Color..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    new_image_dlg = QtWidgets.QDialog()
    ui = Ui_new_image_dlg()
    ui.setupUi(new_image_dlg)
    new_image_dlg.show()
    sys.exit(app.exec_())

