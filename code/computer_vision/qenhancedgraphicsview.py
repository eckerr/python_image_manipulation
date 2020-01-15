"""
QEnhancedGraphicsView class inherits from QWidget
  Created by Ed on 10/29/2019
 """
from pprint import pprint as pp
import math

from PyQt5.QtWidgets import (
                            QMenu,
                            QAction,
                            QGraphicsView,
                            QGraphicsEffect,
                            QGraphicsDropShadowEffect,
                            QGraphicsBlurEffect,
                            QGraphicsColorizeEffect,
                            QGraphicsOpacityEffect,


                             )
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QColor, QPainter, QPixmap, QImage
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal

class QThresholdEffect(QGraphicsEffect):
    def __init__(self):
        super().__init__()
        # painter = QPainter()

    def draw(self, painter):
        # image = QImage()
        print(QGraphicsEffect.sourceIsPixmap(self))
        source, offset = QGraphicsEffect.sourcePixmap(self)
        print(source)
        print(offset)
        image = source.toImage()
        image = image.convertToFormat(QImage.Format_Grayscale8)
        print(image.format())
        print(image.byteCount())
        print(image.size())
        print(image.height(), image.width())
        b = image.bits()
        print(type(b))

        b.setsize(image.byteCount())
        print(b[0][0])

        for i in range(image.byteCount()):
            if b[i][0] < 180:
                b[i] = b'\x00'
            # else:
            #     b[i] = bytes([100])
            #     b[i] = b'\xCC'
        painter.drawPixmap(0, 0, QPixmap.fromImage(image))




class QEnhancedGraphicsView(QGraphicsView):
    def __init__(self, parent):
        super().__init__(parent)
        self.sceneMousePos = QPointF()

    def wheelEvent(self, event):
        if event.angleDelta().y() != 0:
            angleDeltaY = event.angleDelta().y()
            zoomFactor = math.pow(1.0015, angleDeltaY)
            self.scale(zoomFactor, zoomFactor)
            if(angleDeltaY > 0):
                self.centerOn(self.sceneMousePos)
                sceneMousePos = self.mapToScene(event.pos())
            self.update()
            event.accept()
        else:
            event.ignore()

    # def mouseMoveEvent(self, event):
    #     self.sceneMousePos = self.mapToScene(event.pos())

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            menu = QMenu()
            clear_all_action = menu.addAction("Clear All")
            clear_all_action.triggered.connect(self.clear_all)

            clear_selected_action = menu.addAction("Clear Selected")
            clear_selected_action.triggered.connect(self.clear_selected)

            no_effect_action = menu.addAction('No Effect')
            no_effect_action.triggered.connect(self.no_effect)

            blur_effect_action = menu.addAction('Blur Effect')
            blur_effect_action.triggered.connect(self.blur_effect)

            drop_shadow_action = menu.addAction('Drop Shadow Effect')
            drop_shadow_action.triggered.connect(self.drop_shadow_effect)

            colorize_effect_action = menu.addAction('Colorize Effect')
            colorize_effect_action.triggered.connect(self.colorize_effect)

            opacity_effect_action = menu.addAction('Opacity Effect')
            opacity_effect_action.triggered.connect(self.opacity_effect)

            custom_effect_action = menu.addAction('Custom Effect')
            custom_effect_action.triggered.connect(self.threshold_effect)

            menu.exec(event.globalPos())
            event.accept()
        else:
            super().mousePressEvent(event)

    def clear_all(self):
        print('removing All items')
        self.scene().clear()

    def clear_selected(self):
        print('removing Selected items')
        while len(self.scene().selectedItems()) > 0:
            sel = self.scene().selectedItems()
            self.scene().removeItem(sel[0])


    def no_effect(self):
        print('No Effect')
        sel = self.scene().selectedItems()
        for i in range(len(sel)):
            self.effect = None
            sel[i].setGraphicsEffect(self.effect)


    def blur_effect(self):
        print('blur effect')
        sel = self.scene().selectedItems()
        for i in range(len(sel)):
            self.effect = QGraphicsBlurEffect(self)
            self.effect.setBlurRadius(5)
            sel[i].setGraphicsEffect(self.effect)


    def drop_shadow_effect(self):
        print('drop shadow effect')
        sel = self.scene().selectedItems()
        for i in range(len(sel)):
            self.effect = QGraphicsDropShadowEffect(self)
            self.effect.setBlurRadius(5)
            sel[i].setGraphicsEffect(self.effect)


    def colorize_effect(self):
        print('colorize effect')
        sel = self.scene().selectedItems()
        for i in range(len(sel)):
            self.effect = QGraphicsColorizeEffect(self)
            self.effect.setColor(QColor(0, 0, 192))
            sel[i].setGraphicsEffect(self.effect)

    def opacity_effect(self):
        print('colorize effect')
        sel = self.scene().selectedItems()
        for i in range(len(sel)):
            self.effect = QGraphicsOpacityEffect(self)
            self.effect.setOpacity(0.4)
            sel[i].setGraphicsEffect(self.effect)

    def threshold_effect(self):
        print('threshold effect')
        sel = self.scene().selectedItems()
        for i in range(len(sel)):
            self.effect = QThresholdEffect()
            sel[i].setGraphicsEffect(self.effect)








