"""
Threaded version
  Created by Ed on 2/20/2019
 """

import sys
import sqlite3
from time import sleep
from pprint import pprint

from my_opencv import MyCVImage, MyCVHist
from file_open_dialog import Ui_Dialog
from PyQt5 import QtSql
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow
from PyQt5.QtGui import QColor

from normal_map_creator import Ui_MainWindow
from file_getter import file_dialog
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
        self.ui.button_view_data.clicked.connect(self.print_data)
        self.model = None
        self.ui.button_view_data.clicked.connect(self.sql_tableview_model)
        self.ui.button_add_row.clicked.connect(self.sql_add_row)
        self.ui.button_delete_row.clicked.connect(self.sql_delete_row)
        self.ui.button_create_db.clicked.connect(self.create_key_db)

        # -----------------------------------
        self.disp_image = MyCVImage(parent=self.ui.image_label)
        self.disp_image.setMinimumSize(800, 800)
        self.disp_image.show()
        self.disp_hist = MyCVHist(parent=self.ui.hist_label)
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
        #fname = QFileDialog.getOpenFileName(None, 'Open file', '..\\images', '*.jpg;*.png')
        #if fname[0]:
        #    print('file exists')
        #    self.disp_image.read_image(fname[0])
        #    self.disp_image.show()
        self.disp_image.read_image()
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

    # -------------------------------------------------
    # SQL code
    # -------------------------------------------------
    def sql_delete_row(self):
        if self.model:
            self.model.removeRow(self.ui.tableview.currentIndex().row())
        else:
            self.sql_tableview_model()

    # -------------------------------------------------
    def sql_add_row(self):
        if self.model:
            self.model.insertRows(self.model.rowCount(), 1)
        else:
            self.sql_tableview_model()

    # -------------------------------------------------
    def sql_tableview_model(self):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('KEYS.db')

        tableview = self.ui.tableView
        tableview.columnWidth(4)

        self.model = QtSql.QSqlTableModel()
        tableview.setModel(self.model)

        self.model.setTable('KEYS')
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.model.select()
        # self.model.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, 'I')
        self.model.setHeaderData(3, QtCore.Qt.Horizontal, "II")
        self.model.setHeaderData(4, QtCore.Qt.Horizontal, "III")
        self.model.setHeaderData(5, QtCore.Qt.Horizontal, "IV")
        self.model.setHeaderData(6, QtCore.Qt.Horizontal, "V")
        self.model.setHeaderData(7, QtCore.Qt.Horizontal, "VI")
        self.model.setHeaderData(8, QtCore.Qt.Horizontal, "VII")
        tableview.hideColumn(0)

    # -------------------------------------------------
    def print_data(self):
        sqlite_file = 'KEYS.db'
        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM 'KEYS' ORDER BY ID")
        all_rows = cursor.fetchall()
        pprint(all_rows)

        conn.commit()
        conn.close()

    # -------------------------------------------------
    def create_key_db(self):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('KEYS.db')
        db.open()

        query = QtSql.QSqlQuery()

        query.exec_("create table KEYS(ID int primary key, "
                    "I varchar(2),"
                    "II varchar(2),"
                    "III varchar(2),"
                    "IV varchar(2),"
                    "V varchar(2),"
                    "VI varchar(2),"
                    "VII varchar(2))")
        query.exec_("insert into KEYS values(1, 'Gb', 'Ab', 'Bb', 'Cb', 'Db', 'Eb','F')")
        query.exec_("insert into KEYS values(2, 'Db', 'Eb','F', 'Gb', 'Ab', 'Bb', 'C')")
        query.exec_("insert into KEYS values(3, 'Ab', 'Bb', 'C', 'Db', 'Eb','F', 'G')")
        query.exec_("insert into KEYS values(4, 'Eb','F', 'G', 'Ab', 'Bb', 'C', 'D')")
        query.exec_("insert into KEYS values(5, 'Bb', 'C', 'D', 'Eb','F', 'G', 'A')")
        query.exec_("insert into KEYS values(6, 'F', 'G', 'A', 'Bb', 'C', 'D', 'E')")
        query.exec_("insert into KEYS values(7, 'C', 'D', 'E', 'F', 'G', 'A', 'B')")
        query.exec_("insert into KEYS values(8, 'G', 'A', 'B', 'C', 'D', 'E', 'F#')")
        query.exec_("insert into KEYS values(9, 'D', 'E', 'F#', 'G', 'A', 'B', 'C#')")
        query.exec_("insert into KEYS values(10, 'A', 'B', 'C#', 'D', 'E', 'F#', 'G#')")
        query.exec_("insert into KEYS values(11, 'E', 'F#', 'G#', 'A', 'B', 'C#', 'D#')")
        query.exec_("insert into KEYS values(12, 'B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#')")
        query.exec_("insert into KEYS values(13, 'F#', 'G#', 'A#', 'B', 'C#', 'D#', 'E#')")

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


