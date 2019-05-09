import os
import platform
import sys

from PyQt5.QtCore import (Qt,
                         QSettings,
                         QVariant,
                         QSize,
                         QPoint,
                         QByteArray,
                         QTimer,
                         QFile,
                         QFileInfo)

from PyQt5.QtGui import (QImage,
                        QIcon,
                        QKeySequence,
                        QColor,
                        QPixmap,
                        QImageReader,
                        QImageWriter)

from PyQt5.QtWidgets import *

from PyQt5.QtWidgets import (QLabel,
                             QApplication,
                             QDockWidget,
                             QListWidget,
                             QMainWindow,
                             QFrame,
                             QAction,
                             QActionGroup,
                             QMenu,
                             QSpinBox,
                             QMessageBox,
                             QDialog,
                             QColorDialog,
                             QFileDialog)

from debug_dec import debug


app = None

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        editMenu = menubar.addMenu('Edit')
        self.resize(800, 600)

        openAction = QAction('Open Image', self)  
        openAction.triggered.connect(self.openImage) 
        fileMenu.addAction(openAction)

        closeAction = QAction('Exit', self)  
        closeAction.triggered.connect(self.close) 
        fileMenu.addAction(closeAction)
        self.label = QLabel()
        self.setCentralWidget(self.label)

    def openFileNameDialog(self):
        formats = ["Images PNG (*.png);;Jpeg (*.jpg *.jpeg);;Targa (*.tga);;SVG (*.svg)"]
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, caption="Choose image file to open", directory='..\\images',
                                                  filter=formats[0], options=options)
        if fileName:
            print(fileName)
            self.load_pic(fileName)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                "All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)
            print(options)
            print(_)

    def openImage(self, image_path):
        self.openFileNameDialog()

    def load_pic(self, image_path):
        print(image_path)
        pixmap = QPixmap(image_path)
        self.label.setPixmap(pixmap)

        self.resize(pixmap.size())
        self.adjustSize()

def main():
    global app
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    # return app.exec_()
    sys.exit(app.exec_())



if __name__ == '__main__':
    # sys.exit(main())
    main()