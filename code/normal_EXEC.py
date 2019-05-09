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
# from PyQt5 import QtSql
# from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread
# from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow
# from PyQt5.QtGui import QColor

from normal_map_creator import Ui_MainWindow
from file_getter import file_dialog
# from myOpenGL import PyQtOpenGL

class MainWindow_EXEC():

    def __init__(self):
        app = QApplication(sys.argv)
        self.filename = None


        self.MainWindow = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        # -----------------------------------
        #  menu stuff
        self.ui.actionOpen.triggered.connect(self.show_dialog)
        self.ui.actionSave.triggered.connect(self.save_dialog)
        # -----------------------------------
        self.disp_image = MyCVImage(parent=self.ui.image_label)
        self.disp_image.setMinimumSize(800, 800)
        self.disp_image.show()
        self.disp_hist = MyCVHist(self.disp_image.filename, parent=self.ui.hist_label)
        self.disp_hist.setMinimumSize(257, 700)
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
        self.disp_image.read_image()
        self.disp_image.show()
        print(self.disp_image.__dict__)
        self.disp_hist.read_image(self.disp_image.filename)
        self.disp_hist.show()
        return


    def save_dialog(self):
        fname = QFileDialog.getSaveFileName(None, 'Save file', '..\\images', '*.jpg;*.png')
        if fname[0]:
            print('save file exists')
        else:
            print('no save file found')


    # -------------------------------------------------
    # Threading code
    # -------------------------------------------------


class RunThread(QThread):

    counter_value = pyqtSignal(int)  # define new Signal

    def __init__(self, parent=None, counter_start=0):
        super(RunThread, self).__init__(parent)
        self.counter = counter_start
        self.is_running = True

    def run(self):
        while self.counter < 100 and self.is_running:
            sleep(0.1)
            self.counter += 1
            print(self.counter)
            self.counter_value.emit(self.counter)  # emit a new Signal

    def stop(self):
        self.is_running = False
        print('stopping thread...')
        self.terminate()

if __name__ == '__main__':
     MainWindow_EXEC()


