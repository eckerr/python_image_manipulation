"""
 pseudo-plugin fine for various CV filter functions
  to provide bilateral, blur, box, gaussian, median,
  filter2D, derivatives, and morph
  Created by Ed on 12/29/2019
 """

import cv2
import numpy as np
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtWidgets

from cvplugins.ui_filter import Ui_PluginGui

""" constants """
BILATERAL_FILTER_PAGE = 0
BLUR_FILTER_PAGE = 1
BOX_FILTER_PAGE = 2
GAUSSIAN_FILTER_PAGE = 3
MEDIAN_FILTER_PAGE = 4
FILTER2D_FILTER_PAGE = 5
DERIVATIVES_FILTER_PAGE = 6
MORPH_FILTER_PAGE = 7

class Plugin(QtWidgets.QWidget):

    updateNeeded = pyqtSignal()
    infoMessage = pyqtSignal(str)
    errorMessage = pyqtSignal(str)

    def __init__(self):
        super(Plugin, self).__init__()
        self.title = self.__class__
        self.version = "1.0.0"
        self.description = "filters an image"
        self.help = ""
        self.ui = None

    def setupUi(self, parent):
        self.ui = Ui_PluginGui()
        self.ui.setupUi(parent)

        self.ui.morph_shape_combo.addItems(["MORPH_RECT",
                                           "MORPH_CROSS",
                                           "MORPH_ELLIPSE"])
        self.ui.morph_type_combo.addItems(["MORPH_ERODE",
                                          "MORPH_DILATE",
                                          "MORPH_OPEN",
                                          "MORPH_CLOSE",
                                          "MORPH_GRADIENT",
                                          "MORPH_TOPHAT",
                                          "MORPH_BLACKHAT"])
        items = []
        item_list = ["BORDER_CONSTANT",
                     "BORDER_REPLICATE",
                     "BORDER_REFLECT",
                     "BORDER_WRAP",
                     "BORDER_REFLECT_101"]
        self.ui.bilateral_border_type_combo.addItems(item_list)
        self.ui.blur_border_type_combo.addItems(item_list)
        self.ui.box_border_type_combo.addItems(item_list[:2])
        self.ui.gaussian_border_type_combo.addItems(item_list)
        self.ui.derivatives_border_type_combo.addItems(item_list)
        self.ui.morph_border_type_combo.addItems(item_list)

        # connect signals to update when changed
        self.ui.bilateral_dia_spin.valueChanged.connect(self.call_update)
        self.ui.bilateral_sigma_color_spin.valueChanged.connect(self.call_update)
        self.ui.bilateral_sigma_space_spin.valueChanged.connect(self.call_update)
        self.ui.bilateral_border_type_combo.currentIndexChanged.connect(self.call_update)

        self.ui.blur_kernel_spin.valueChanged.connect(self.call_update)
        self.ui.blur_anchor_x_spin.valueChanged.connect(self.call_update)
        self.ui.blur_anchor_y_spin.valueChanged.connect(self.call_update)
        self.ui.blur_border_type_combo.currentIndexChanged.connect(self.call_update)

        self.ui.box_kernel_spin.valueChanged.connect(self.call_update)
        self.ui.box_depth_spin.valueChanged.connect(self.call_update)
        self.ui.box_kernel_spin.valueChanged.connect(self.call_update)
        self.ui.box_anchor_x_spin.valueChanged.connect(self.call_update)
        self.ui.box_anchor_y_spin.valueChanged.connect(self.call_update)
        self.ui.box_normalize_check.toggled.connect(self.call_update)
        self.ui.box_border_type_combo.currentIndexChanged.connect(self.call_update)

        self.ui.gaussian_kernel_spin.valueChanged.connect(self.call_update)
        self.ui.gaussian_sig_x_spin.valueChanged.connect(self.call_update)
        self.ui.gaussian_sig_y_spin.valueChanged.connect(self.call_update)
        self.ui.gaussian_border_type_combo.currentIndexChanged.connect(self.call_update)

        self.ui.median_kernel_spin.valueChanged.connect(self.call_update)

        self.ui.derivatives_ddepth_spin.valueChanged.connect(self.call_update)
        self.ui.derivatives_dx_spin.valueChanged.connect(self.call_update)
        self.ui.derivatives_dy_spin.valueChanged.connect(self.call_update)
        self.ui.derivatives_scale_spin.valueChanged.connect(self.call_update)
        self.ui.derivatives_delta_spin.valueChanged.connect(self.call_update)
        self.ui.derivatives_border_type_combo.currentIndexChanged.connect(self.call_update)
        self.ui.derivatives_normalize_check.toggled.connect(self.call_update)
        self.ui.derivatives_kernel_spin.valueChanged.connect(self.call_update)

        self.ui.morph_shape_combo.currentIndexChanged.connect(self.call_update)
        self.ui.morph_iteration_spin.valueChanged.connect(self.call_update)
        self.ui.morph_anchor_x_spin.valueChanged.connect(self.call_update)
        self.ui.morph_anchor_y_spin.valueChanged.connect(self.call_update)
        self.ui.morph_kernel_spin.valueChanged.connect(self.call_update)
        self.ui.morph_type_combo.currentIndexChanged.connect(self.call_update)
        self.ui.morph_iteration_spin.valueChanged.connect(self.call_update)
        self.ui.morph_border_type_combo.currentIndexChanged.connect(self.call_update)

    def process_image(self, input_image, output_image):

        width = input_image.shape[1]
        height = input_image.shape[0]

        current_page = self.ui.mainTabs.currentIndex()
        print("current_page_index: ", current_page)

        if current_page == BILATERAL_FILTER_PAGE:
            output_image = cv2.bilateralFilter(input_image,
                                               self.ui.bilateral_dia_spin.value(),
                                               self.ui.bilateral_sigma_color_spin.value(),
                                               self.ui.bilateral_sigma_space_spin.value(),
                                               self.ui.bilateral_border_type_combo.currentIndex())
            return output_image

        elif current_page == BLUR_FILTER_PAGE:
            print("kernel: ", self.ui.blur_kernel_spin.value())
            # print("anchor: ", self.ui.blur_anchor_x_spin.value(), self.ui_blur anchor_y_spin.value())
            output_image = cv2.blur(input_image,
                                    (self.ui.blur_kernel_spin.value(),
                                    self.ui.blur_kernel_spin.value()),
                                    output_image,
                                    (self.ui.blur_anchor_x_spin.value(),
                                    self.ui.blur_anchor_y_spin.value()),
                                    self.ui.blur_border_type_combo.currentIndex())
            return output_image

        elif current_page == BOX_FILTER_PAGE:
            print("normalize: ", self.ui.box_normalize_check.isChecked())
            output_image = cv2.boxFilter(src=input_image,
                                         ddepth=self.ui.box_depth_spin.value(),
                                         ksize=(self.ui.box_kernel_spin.value(),
                                         self.ui.box_kernel_spin.value()),
                                         dst=output_image,
                                         anchor=(self.ui.box_anchor_x_spin.value(),
                                         self.ui.box_anchor_y_spin.value()),
                                         normalize=self.ui.box_normalize_check.isChecked(),
                                         borderType=self.ui.box_border_type_combo.currentIndex())
            return output_image

        elif current_page == GAUSSIAN_FILTER_PAGE:
            output_image = cv2.GaussianBlur(input_image,
                                            ksize=(self.ui.gaussian_kernel_spin.value(),
                                                   self.ui.gaussian_kernel_spin.value()),
                                            sigmaX=self.ui.gaussian_sig_x_spin.value(),
                                            dst=output_image,
                                            sigmaY=self.ui.gaussian_sig_y_spin.value(),
                                            borderType=self.ui.gaussian_border_type_combo.currentIndex())

            return output_image

        elif current_page == MEDIAN_FILTER_PAGE:
            output_image = cv2.medianBlur(input_image,
                                          self.ui.median_kernel_spin.value())
            return output_image

        elif current_page == FILTER2D_FILTER_PAGE:
            f2dkernel = (0, 1.5, 0,
                         1.5, -6, 1.5,
                         0, 1.5, 0)
            output_image = cv2.filter2D(input_image,
                                        output_image,
                                        -1,
                                        f2dkernel,
                                        (-1, -1))
            return output_image

        elif current_page == DERIVATIVES_FILTER_PAGE:
            if self.ui.derivatives_sobel_radio.isChecked():
                cv2.Sobel(src=input_image,
                          ddepth=self.ui.derivatives_ddepth_spin.value(),
                          dx=self.ui.derivatives_dx_spin.value(),
                          dy=self.ui.derivatives_dy_spin.value(),
                          dst=output_image,
                          ksize=self.ui.derivatives_kernel_spin.value(),
                          scale=self.ui.derivatives_scale_spin.value(),
                          delta=self.ui.derivatives_delta_spin.value(),
                          borderType=self.ui.derivatives_border_type_combo.currentIndex())

            elif self.ui.derivatives_scharr_radio.isChecked():
                cv2.Scharr(src=input_image,
                           ddepth=self.ui.derivatives_ddepth_spin.value(),
                           dx=self.ui.derivatives_dx_spin.value(),
                           dy=self.ui.derivatives_dy_spin.value(),
                           dst=output_image,
                           ksize=self.derivatives_kernel_spin.value(),
                           scale=self.ui.derivatives_scale_spin.value(),
                           delta=self.ui.derivatives_delta_spin.value(),
                           borderType=self.ui.derivatives_border_type_combo.currentIndex())

            elif self.ui.derivatives_laplacian_radio.isChecked():
                output_image = cv2.Laplacian(src=input_image,
                                             ddepth=self.ui.derivatives_ddepth_spin.value(),
                                             dst=output_image,
                                             ksize=self.ui.derivatives_kernel_spin.value(),
                                             scale=self.ui.derivatives_scale_spin.value(),
                                             delta=self.ui.derivatives_delta_spin.value(),
                                             borderType=self.ui.derivatives_border_type_combo.currentIndex())

            return output_image

        elif current_page == MORPH_FILTER_PAGE:
            if self.ui.morph_erode_radio.isChecked():
                cv2.erode(input_image,
                          output_image,
                          cv2.getStructuringElement(self.ui.morph_shape_combo.currentIndex(),
                                                    (5, 5)),
                          (-1, -1),
                          self.ui.morph_iteration_spin.value())
            elif self.ui.morph_dilate_radio.isChecked():
                cv2.dilate(input_image,
                           output_image,
                           cv2.getStructingElement(self.ui.morph_shape_combo.currentIndex(),
                                                   (5,5)),
                           (-1,-1),
                           self.ui.morph_iteration_spin.value())

            elif self.ui.morph_morph_radio.isChecked():
                m_anchor = (self.ui.morph_anchor_x_spin.value(),
                            self.ui.morph_anchor_y_spin.value())
                m_kernel = self.ui.morph_kernel_spin.value(), self.ui.morph_kernel_spin.value()

                output_image = cv2.morphologyEx(input_image,
                                                self.ui.morph_type_combo.currentIndex(),
                                                cv2.getStructuringElement(self.ui.morph_shape_combo.currentIndex(),
                                                                         m_kernel),
                                                anchor=m_anchor,
                                                iterations=self.ui.morph_iteration_spin.value(),
                                                borderType=self.ui.morph_border_type_combo.currentIndex()
                                                # borderValue=
                                                )


                                 # return outputImage
            return output_image

    def call_update(self):
        self.updateNeeded.emit()

    def on_bilateral_dia_spin_valueChanged(self):
        self.updateNeeded.emit()

    def on_blur_kernel_spin_valueChanged(self):
        self.updateNeeded.emit()

    def on_remapRadio_toggled(self):
        self.updateNeeded.emit()

    def on_affineRadio_toggled(self):
        self.updateNeeded.emit()

    def on_perspectiveRadio_toggled(self):
        self.updateNeeded.emit()

    def on_interpolationCombo_currentIndexChanged(self, int):
        print('box value when updateNeeded sent: ', int)
        self.updateNeeded.emit()

    def on_borderTypeCombo_currentIndexChanged(self, int):
        print('box value when updateNeeded sent: ', int)
        self.updateNeeded.emit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    pluginGui = QtWidgets.QWidget()
    ui = Ui_pluginGui()
    ui.setupUi(pluginGui)
    pluginGui.show()
    sys.exit(app.exec_())
