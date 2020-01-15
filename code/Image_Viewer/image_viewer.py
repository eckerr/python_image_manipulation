"""
  image_viewer.py
  application to view image in pyQT5
  Created by Ed on 8/29/2019
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
                             )


from main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    """ drag and drop image viewer """
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # set up variables
        self.pixmap = QPixmap()
        self.f = QFileInfo()

        self.setAcceptDrops(True)


# ---------------------------------------
# Drag / Drop code
# ---------------------------------------
    def dragEnterEvent(self, event):
        acceptedFileTypes = []
        acceptedFileTypes.append("jpg")
        acceptedFileTypes.append("png")
        acceptedFileTypes.append("bmp")
        print(acceptedFileTypes)

        if (event.mimeData().hasUrls())and \
                (len(event.mimeData().urls()) == 1):
            self.f = QFileInfo(event.mimeData().urls()[0].toLocalFile())
            print(self.f.suffix().lower())
            if self.f.suffix().lower() in acceptedFileTypes:
                event.acceptProposedAction()

    def dropEvent(self, event):
        print('Drop Event happening')
        print(self.f.absoluteFilePath())
        if(self.pixmap.load(self.f.absoluteFilePath())):
            self.ui.label.setPixmap(self.pixmap.scaled(self.ui.label.size(),
                                             Qt.KeepAspectRatio,
                                             Qt.SmoothTransformation))
        else:
            QMessageBox.critical(self,
                                 "Error",
                                 "The image file cannot be read!")

    def resizeEvent(self, event):
        if not(self.pixmap.isNull()):
            self.ui.label.setPixmap(self.pixmap.scaled(self.ui.label.width()-5,
                                                       self.ui.label.height()-5,
                                                       Qt.KeepAspectRatio,
                                                       Qt.SmoothTransformation))


if __name__=="__main__":
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
