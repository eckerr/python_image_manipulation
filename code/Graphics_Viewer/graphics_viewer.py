"""
graphics_viewer.py

Builds basic graphics scene

  Created by Ed on 10/23/2019
 """

import sys
from PyQt5.QtGui import (
                         QPixmap,
                         QDragEnterEvent,
                         QDropEvent,
                         QResizeEvent,
                         )

from PyQt5.QtCore import (
                          QFileInfo,
                          QMimeData,
                          QStringListModel,

                          )

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
                             QApplication,
                             QMainWindow,
                             QMessageBox,
                             QGraphicsScene,
                             QGraphicsPixmapItem,
                             QGraphicsView
                             )

import MainWindow from MainWindow




class MainWindow(QMainWindow):
    """ drag and drop graphics viewer """
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.setAcceptDrops(True)

        # set up variables
        self.f = QFileInfo()
        self.scene = QGraphicsScene()
        self.ui.graphicsView.setAcceptDrops(False)
        self.ui.graphicsView.setScene(self.scene)
        self.ui.graphicsView.setInteractive(True)
        self.ui.graphicsView.setDragMode(QGraphicsView.RubberBandDrag)
        self.ui.graphicsView.setRubberBandSelectionMode(Qt.ContainsItemShape)



    # --------------------------------
    # Drag / Drop code
    # --------------------------------
    def dragEnterEvent(self, event):
        acceptedFileTypes = []
        acceptedFileTypes.append("jpg")
        acceptedFileTypes.append("png")
        acceptedFileTypes.append("bmp")
        print(acceptedFileTypes)

        if (event.mimeData().hasUrls()) and \
                (len(event.mimeData().urls()) == 1):
            self.f = QFileInfo(event.mimeData().urls()[0].toLocalFile())
            print(self.f.suffix().lower())
            if self.f.suffix().lower() in acceptedFileTypes:
                event.acceptProposedAction()

    def dropEvent(self, event):
        print('Drop Event happened')
 #       print(f.absoluteFilePath())
        file = QFileInfo(event.mimeData().urls()[0].toLocalFile())
        pixmap = QPixmap()
        if pixmap.load(self.f.absoluteFilePath()):
            item = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(item)
        else:
            QMessageBox.critical(self,
                                 'Error',
                                 'The image file cannot be read!')
        print(self.scene.items().count(item))
        print(self.scene.items().count(item))

        print(self.scene.items().count(item))
        print(self.scene)


if __name__=="__main__":
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())

