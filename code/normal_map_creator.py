# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\normal_map_creator.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1881, 941)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1871, 871))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_progress = QtWidgets.QWidget()
        self.tab_progress.setObjectName("tab_progress")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.tab_progress)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 851, 631))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.groupBox_3 = QtWidgets.QGroupBox(self.verticalLayoutWidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox_3)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 228, 171))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.fontComboBox = QtWidgets.QFontComboBox(self.layoutWidget)
        self.fontComboBox.setBaseSize(QtCore.QSize(0, 400))
        self.fontComboBox.setInsertPolicy(QtWidgets.QComboBox.InsertAtTop)
        self.fontComboBox.setObjectName("fontComboBox")
        self.verticalLayout_5.addWidget(self.fontComboBox)
        self.label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_5.addWidget(self.label)
        self.frame = QtWidgets.QFrame(self.groupBox_3)
        self.frame.setGeometry(QtCore.QRect(280, 140, 481, 401))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_6.addWidget(self.groupBox_3)
        self.horizontalLayout_3.addLayout(self.verticalLayout_6)
        self.horizontalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tabWidget.addTab(self.tab_progress, "")
        self.tab_image = QtWidgets.QWidget()
        self.tab_image.setObjectName("tab_image")
        self.layoutWidget1 = QtWidgets.QWidget(self.tab_image)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 0, 1851, 801))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontal_scroll_layout = QtWidgets.QHBoxLayout()
        self.horizontal_scroll_layout.setObjectName("horizontal_scroll_layout")
        self.vertical_scroll_layout = QtWidgets.QVBoxLayout()
        self.vertical_scroll_layout.setObjectName("vertical_scroll_layout")
        self.image_label = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image_label.sizePolicy().hasHeightForWidth())
        self.image_label.setSizePolicy(sizePolicy)
        self.image_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.image_label.setObjectName("image_label")
        self.vertical_scroll_layout.addWidget(self.image_label)
        self.horizontalScrollBar = QtWidgets.QScrollBar(self.layoutWidget1)
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")
        self.vertical_scroll_layout.addWidget(self.horizontalScrollBar)
        self.horizontal_scroll_layout.addLayout(self.vertical_scroll_layout)
        self.verticalScrollBar = QtWidgets.QScrollBar(self.layoutWidget1)
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.horizontal_scroll_layout.addWidget(self.verticalScrollBar)
        self.horizontalLayout.addLayout(self.horizontal_scroll_layout)
        self.groupBox = QtWidgets.QGroupBox(self.layoutWidget1)
        self.groupBox.setObjectName("groupBox")
        self.hist_label = QtWidgets.QLabel(self.groupBox)
        self.hist_label.setGeometry(QtCore.QRect(560, 30, 351, 771))
        self.hist_label.setText("")
        self.hist_label.setObjectName("hist_label")
        self.horizontalLayout.addWidget(self.groupBox)
        self.tabWidget.addTab(self.tab_image, "")
        self.tab_SQL = QtWidgets.QWidget()
        self.tab_SQL.setObjectName("tab_SQL")
        self.layoutWidget2 = QtWidgets.QWidget(self.tab_SQL)
        self.layoutWidget2.setGeometry(QtCore.QRect(21, 31, 95, 135))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.button_view_data = QtWidgets.QPushButton(self.layoutWidget2)
        self.button_view_data.setObjectName("button_view_data")
        self.verticalLayout_11.addWidget(self.button_view_data)
        self.button_add_row = QtWidgets.QPushButton(self.layoutWidget2)
        self.button_add_row.setObjectName("button_add_row")
        self.verticalLayout_11.addWidget(self.button_add_row)
        self.button_delete_row = QtWidgets.QPushButton(self.layoutWidget2)
        self.button_delete_row.setObjectName("button_delete_row")
        self.verticalLayout_11.addWidget(self.button_delete_row)
        self.button_create_db = QtWidgets.QPushButton(self.layoutWidget2)
        self.button_create_db.setObjectName("button_create_db")
        self.verticalLayout_11.addWidget(self.button_create_db)
        self.tableView = QtWidgets.QTableView(self.tab_SQL)
        self.tableView.setGeometry(QtCore.QRect(130, 30, 601, 551))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setDefaultSectionSize(75)
        self.tableView.horizontalHeader().setMinimumSectionSize(75)
        self.tabWidget.addTab(self.tab_SQL, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1881, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionUndo = QtWidgets.QAction(MainWindow)
        self.actionUndo.setObjectName("actionUndo")
        self.actionRedo = QtWidgets.QAction(MainWindow)
        self.actionRedo.setObjectName("actionRedo")
        self.actionCut = QtWidgets.QAction(MainWindow)
        self.actionCut.setObjectName("actionCut")
        self.actionDelete = QtWidgets.QAction(MainWindow)
        self.actionDelete.setObjectName("actionDelete")
        self.actionSelect_All = QtWidgets.QAction(MainWindow)
        self.actionSelect_All.setObjectName("actionSelect_All")
        self.action_Preferences = QtWidgets.QAction(MainWindow)
        self.action_Preferences.setObjectName("action_Preferences")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionDelete)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionSelect_All)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.action_Preferences)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        self.actionExit.triggered.connect(MainWindow.close)
        self.fontComboBox.activated['QString'].connect(self.label.setText)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Normal Map Creator"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Font Picker"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_progress), _translate("MainWindow", "Progress Bar"))
        self.image_label.setText(_translate("MainWindow", "Image"))
        self.groupBox.setTitle(_translate("MainWindow", "Histograms"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_image), _translate("MainWindow", "Open GL"))
        self.button_view_data.setStatusTip(_translate("MainWindow", "list items in database"))
        self.button_view_data.setText(_translate("MainWindow", "View Data"))
        self.button_add_row.setStatusTip(_translate("MainWindow", "Add a new row to the database"))
        self.button_add_row.setText(_translate("MainWindow", "Add Row"))
        self.button_delete_row.setStatusTip(_translate("MainWindow", "Delete selected row from the database"))
        self.button_delete_row.setText(_translate("MainWindow", "Delete Row"))
        self.button_create_db.setStatusTip(_translate("MainWindow", "Create the database if does not exist"))
        self.button_create_db.setText(_translate("MainWindow", "Create db"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_SQL), _translate("MainWindow", "SQL"))
        self.menuFile.setStatusTip(_translate("MainWindow", "File handling choices"))
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menuEdit.setStatusTip(_translate("MainWindow", "Editing options"))
        self.menuEdit.setTitle(_translate("MainWindow", "&Edit"))
        self.actionOpen.setText(_translate("MainWindow", "&Open"))
        self.actionOpen.setStatusTip(_translate("MainWindow", "Choose file to open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "&Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionSave_As.setText(_translate("MainWindow", "Save &As..."))
        self.actionSave_As.setStatusTip(_translate("MainWindow", "Save file with a different name"))
        self.actionSave_As.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.actionExit.setText(_translate("MainWindow", "&Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionCopy.setText(_translate("MainWindow", "&Copy"))
        self.actionCopy.setStatusTip(_translate("MainWindow", "copy selected"))
        self.actionCopy.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionPaste.setText(_translate("MainWindow", "&Paste"))
        self.actionPaste.setStatusTip(_translate("MainWindow", "Paste from clipboard"))
        self.actionPaste.setShortcut(_translate("MainWindow", "Ctrl+V"))
        self.actionUndo.setText(_translate("MainWindow", "&Undo"))
        self.actionUndo.setStatusTip(_translate("MainWindow", "Undo last action"))
        self.actionUndo.setShortcut(_translate("MainWindow", "Ctrl+Z"))
        self.actionRedo.setText(_translate("MainWindow", "&Redo"))
        self.actionRedo.setShortcut(_translate("MainWindow", "Ctrl+Y"))
        self.actionCut.setText(_translate("MainWindow", "&Cut"))
        self.actionCut.setStatusTip(_translate("MainWindow", "remove and copy to clipboard"))
        self.actionCut.setShortcut(_translate("MainWindow", "Ctrl+X"))
        self.actionDelete.setText(_translate("MainWindow", "&Delete"))
        self.actionDelete.setStatusTip(_translate("MainWindow", "Delete selected item"))
        self.actionDelete.setShortcut(_translate("MainWindow", "Ctrl+D"))
        self.actionSelect_All.setText(_translate("MainWindow", "Select All"))
        self.actionSelect_All.setStatusTip(_translate("MainWindow", "Select all items"))
        self.actionSelect_All.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.action_Preferences.setText(_translate("MainWindow", "&Preferences"))
        self.action_Preferences.setShortcut(_translate("MainWindow", "Ctrl+K"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
