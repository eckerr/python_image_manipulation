"""

  Created by Ed on 3/6/2019
 """

import sys
import cv2
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSignal, QPoint, Qt


class MyOpenCV(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.filename = "..\\images\\qb912_normal.jpg"
        self.img = cv2.imread(self.filename)

        image = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
#        image = cv2.cvtColor(self.img, cv2.COLOR_GRAY2RGB)
        height, width, chans = self.img.shape
        bValue = width * 3

#        qimage = image
        qimage = QImage(image, width, height,  bValue, QImage.Format_RGB888)

        self.setPixmap(QPixmap.fromImage(qimage))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    label = MyOpenCV()

    label.show()
    app.exec_()

#    cv2.waitKey()
#    cv2.destroyAllWindows()