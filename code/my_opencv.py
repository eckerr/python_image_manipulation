"""

  Created by Ed on 3/6/2019
 """

import sys
import cv2

from PyQt5.QtWidgets import QApplication, QLabel, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSignal, QPoint, Qt
from histograms import hist_lines_split, hist_lines
from numpy import vstack

class MyCVImage(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.filename = ''
        self.fltr = ''
        self.img = None
        self.read_image()

    def read_image(self):
        # read the image
        fltr_types = "All files (*.*)\nJpeg (*.jpg *.jpeg)\nPng (*.png)"
        self.filename, self.fltr = QFileDialog.getOpenFileName(None, 'Open file', '..\\images', fltr_types)
        if self.filename:
            print('file exists')
            print(self.filename)
        else:
            print('no file found')
        self.img = cv2.imread(self.filename)
        self.convert_for_RGB_display()
        return self.filename

    def convert_for_RGB_display(self):
        height, width, chans = self.img.shape
        # if multiple channels convert from BGR to RGB
        if len(self.img.shape) == 3:
            image = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        else:
            image = cv2.cvtColor(self.img, cv2.COLOR_GRAY2RGB)
        bValue = width * 3
        qimage = QImage(image, width, height,  bValue, QImage.Format_RGB888)
        self.setPixmap(QPixmap.fromImage(qimage))
        self.img = qimage


class MyCVHist(QLabel):
    def __init__(self, filename, parent=None):
        super().__init__(parent)
        self.filename = filename
        self.fltr = ''
        self.img = None
        self.res = None

    # def read_img(self, filename):
    #     self.img = cv2.imread(self.filename)
    #     self.convert_for_RGB_display()
    #     return self.img

    def read_image(self, filename):
        # read the image
        # self.filename, self.fltr = QFileDialog.getOpenFileName(None, 'Open file', '..\\images',

        self.filename = filename
        if self.filename:
            print('file exists')
            # self.disp_image.read_image(fname[0])
            # self.disp_image.show()
            # self.disp_hist.read_image(fname[0])
            # self.disp_hist.show()
        else:
            print('no file found')

        # self.filename = filename
        # self.filename = "..\\images\\brick.jpg"
        self.img_all = cv2.imread(self.filename)
        self.img_gray = cv2.imread(self.filename, 0)


        hist_pics = hist_lines_split(self.img_all)
        hist_pics[3] = hist_lines(self.img_gray)
        self.res = vstack((hist_pics[0], hist_pics[1], hist_pics[2], hist_pics[3]))
        self.convert_for_hist_RGB_display()
        return self.filename

    def convert_for_hist_RGB_display(self):
        height, width, chans = self.res.shape
        # if multiple channels convert from BGR to RGB
        if len(self.res.shape) == 3:
            image = cv2.cvtColor(self.res, cv2.COLOR_BGR2RGB)
        else:
            image = cv2.cvtColor(self.res, cv2.COLOR_GRAY2RGB)
        bValue = width * 3
        qimage = QImage(image, width, height, bValue, QImage.Format_RGB888)
        self.setPixmap(QPixmap.fromImage(qimage))
        self.img = qimage

    def convert_hist_for_RGB_display(self):
        height, width = self.img_all.shape
        # convert from BGR to RGB
        image = cv2.cvtColor(self.img_all, cv2.COLOR_GRAY2RGB)
        bValue = width * 3
        qimage = QImage(image, width, height,  bValue, QImage.Format_RGB888)
        self.setPixmap(QPixmap.fromImage(qimage))





if __name__ == '__main__':
    app = QApplication(sys.argv)
    # label = MyOpenCV()
    label = MyCVImage()
    l2 = MyCVHist('..\\images\\brick.jpg')

    label.show()
    app.exec_()

#    cv2.waitKey()
#    cv2.destroyAllWindows()