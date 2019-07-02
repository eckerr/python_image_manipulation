"""
Threaded version
  Created by Ed on 2/20/2019
 """

import sys
import sqlite3
from time import sleep
from pprint import pprint

from my_opencv import MyCVImage, MyCVHist
# from file_open_dialog import Ui_Dialog
from PyQt5 import QtSql
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow
from PyQt5.QtGui import QColor

from normal_map_creator import Ui_MainWindow
# from file_getter import file_dialog
# from myOpenGL import PyQtOpenGL

class MainWindow_EXEC():

    def __init__(self):
        app = QApplication(sys.argv)

        self.MainWindow = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        #self.file_dialog = QFileDialog()

        # -----------------------------------
        #  menu stuff
        self.ui.actionOpen.triggered.connect(self.show_dialog)
        self.ui.actionSave.triggered.connect(self.save_dialog)
        # -----------------------------------
        #  Database stuff
        # self.ui.button_view_data.clicked.connect(self.print_data)
        # self.model = None
        # self.ui.button_view_data.clicked.connect(self.sql_tableview_model)
        # self.ui.button_add_row.clicked.connect(self.sql_add_row)
        # self.ui.button_delete_row.clicked.connect(self.sql_delete_row)
        # self.ui.button_create_db.clicked.connect(self.create_key_db)

        # -----------------------------------
        self.disp_image = MyCVImage(parent=self.ui.image_label)
        self.disp_image.setMinimumSize(800, 800)
        self.disp_image.show()
        self.disp_hist = MyCVHist("..\\images\\brick.jpg", parent=self.ui.hist_label)
        self.disp_hist.setMinimumSize(300, 800)
        self.disp_hist.show()
        """
        open_gl = PyQtOpenGL(parent=self.ui.graphicsView)
        open_gl.setMinimumSize(300, 300)

        open_gl.paint_0 = True
        open_gl.paint_1 = True
        open_gl.paint_2 = True
        open_gl.resize_lines = False
        open_gl.paint_rotation = True
        """
        # -----------------------------------
        self.MainWindow.show()
        sys.exit(app.exec_())

    # -------------------------------------------------
    # menu code
    # -------------------------------------------------
    def show_dialog(self):
        fname = "..\\images\\brick.jpg"
        #fname = QFileDialog.getOpenFileName(None, 'Open file', '..\\images', '*.jpg;*.png')
        #if fname[0]:
        #    print('file exists')
        #    self.disp_image.read_image(fname[0])
        #    self.disp_image.show()
        self.disp_image.read_image(fname)
        #self.disp_image.show()
        #    self.disp_hist.read_image(fname[0])
        #    self.disp_hist.show()
        # else:
        #    print('no file found')

    def save_dialog(self):
        fname = QFileDialog.getSaveFileName(None, 'Save file', '..\\images', '*.jpg;*.png')
        if fname[0]:
            print('save file exists')
            #self.disp_image.read_image(fname[0])
            #self.disp_image.show()
            #self.disp_hist.read_image(fname[0])
            #self.disp_hist.show()
        else:
            print('no save file found')


if __name__ == '__main__':
     MainWindow_EXEC()


