# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_segmentation.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PluginGui(object):
    def setupUi(self, PluginGui):
        PluginGui.setObjectName("PluginGui")
        PluginGui.resize(400, 558)
        self.layoutWidget = QtWidgets.QWidget(PluginGui)
        self.layoutWidget.setGeometry(QtCore.QRect(7, 10, 381, 531))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.threshAdaptiveCheck = QtWidgets.QCheckBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.threshAdaptiveCheck.sizePolicy().hasHeightForWidth())
        self.threshAdaptiveCheck.setSizePolicy(sizePolicy)
        self.threshAdaptiveCheck.setMinimumSize(QtCore.QSize(94, 0))
        self.threshAdaptiveCheck.setObjectName("threshAdaptiveCheck")
        self.horizontalLayout.addWidget(self.threshAdaptiveCheck)
        self.threshAdaptiveCombo = QtWidgets.QComboBox(self.layoutWidget)
        self.threshAdaptiveCombo.setObjectName("threshAdaptiveCombo")
        self.horizontalLayout.addWidget(self.threshAdaptiveCombo)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.threshTypeCombo = QtWidgets.QComboBox(self.layoutWidget)
        self.threshTypeCombo.setObjectName("threshTypeCombo")
        self.horizontalLayout_2.addWidget(self.threshTypeCombo)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.threshLabel = QtWidgets.QLabel(self.layoutWidget)
        self.threshLabel.setMinimumSize(QtCore.QSize(66, 0))
        self.threshLabel.setObjectName("threshLabel")
        self.horizontalLayout_3.addWidget(self.threshLabel)
        self.threshSlider = QtWidgets.QSlider(self.layoutWidget)
        self.threshSlider.setMaximum(255)
        self.threshSlider.setProperty("value", 20)
        self.threshSlider.setOrientation(QtCore.Qt.Horizontal)
        self.threshSlider.setObjectName("threshSlider")
        self.horizontalLayout_3.addWidget(self.threshSlider)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.maxLabel = QtWidgets.QLabel(self.layoutWidget)
        self.maxLabel.setMinimumSize(QtCore.QSize(66, 0))
        self.maxLabel.setObjectName("maxLabel")
        self.horizontalLayout_4.addWidget(self.maxLabel)
        self.threshMaxSlider = QtWidgets.QSlider(self.layoutWidget)
        self.threshMaxSlider.setMaximum(255)
        self.threshMaxSlider.setSliderPosition(128)
        self.threshMaxSlider.setOrientation(QtCore.Qt.Horizontal)
        self.threshMaxSlider.setObjectName("threshMaxSlider")
        self.horizontalLayout_4.addWidget(self.threshMaxSlider)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(PluginGui)
        QtCore.QMetaObject.connectSlotsByName(PluginGui)

    def retranslateUi(self, PluginGui):
        _translate = QtCore.QCoreApplication.translate
        PluginGui.setWindowTitle(_translate("PluginGui", "Form"))
        self.threshAdaptiveCheck.setText(_translate("PluginGui", "Adaptive"))
        self.label.setText(_translate("PluginGui", "Threshold Type:"))
        self.threshLabel.setText(_translate("PluginGui", "Threshold: "))
        self.maxLabel.setText(_translate("PluginGui", "Max:"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PluginGui = QtWidgets.QWidget()
    ui = Ui_PluginGui()
    ui.setupUi(PluginGui)
    PluginGui.show()
    sys.exit(app.exec_())
