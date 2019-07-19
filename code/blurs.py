"""
blurs.py - performs a series of gaussian blurs for creating normals

  Created by Ed on 5/20/2019
 """

import cv2
import numpy as np

def g_blur(src, kernel, dst, freq):
    # TODO: need to check functionality
    cv2.GaussianBlur(src, kernel, dst, cv2.BORDER_WRAP)
    freq = src.astype(np.float) - dst.astype(np.float)
    cv2.imwrite('..\\images\\gblur0.png', freq.astype(np.int8))

def blurs(image_inst):
    # freq = image_inst.hf
    kernel = 0
    src = image_inst.cv_img_gray
    dst = image_inst.cv_gblur0
    image_inst.cv_gblur0 = image_inst.cv_img_gray.copy().astype(np.float64)
    cv2.imwrite('..\images\\gblur0.png', image_inst.cv_gblur0)
    kernel = 3
    print("gblur0", kernel)
    image_inst.cv_gblur1 = cv2.GaussianBlur(image_inst.cv_gblur0, (kernel, kernel), kernel, image_inst.cv_gblur1, 0)
    kernel = kernel * 2 + 1
    cv2.imwrite('..\\images\\gblur1.png', image_inst.cv_gblur1)
    print("gblur1", kernel)
    kernel = kernel * 2 + 1
    image_inst.cv_gblur2 = cv2.GaussianBlur(image_inst.cv_gblur1, (kernel, kernel), kernel, image_inst.cv_gblur2, 0)
    cv2.imwrite('..\\images\\gblur2.png', image_inst.cv_gblur2)
    print("gblur2", kernel)
    kernel = kernel * 2 + 1
    image_inst.cv_gblur3 = cv2.GaussianBlur(image_inst.cv_gblur2, (kernel, kernel), kernel, image_inst.cv_gblur3, 0)
    cv2.imwrite('..\\images\\gblur3.png', image_inst.cv_gblur3)
    print("gblur3", kernel)
    kernel = kernel * 2 + 1
    image_inst.cv_gblur4 = cv2.GaussianBlur(image_inst.cv_gblur3, (kernel, kernel), kernel, image_inst.cv_gblur4, 0)
    cv2.imwrite('..\\images\\gblur4.png', image_inst.cv_gblur4)
    print("gblur4", kernel)
    kernel = kernel * 2 + 1
    image_inst.cv_gblur5 = cv2.GaussianBlur(image_inst.cv_gblur4, (kernel, kernel), kernel, image_inst.cv_gblur5, 0)
    cv2.imwrite('..\\images\\gblur5.png', image_inst.cv_gblur5)
    print("gblur5", kernel)
    kernel = kernel * 2 + 1
    image_inst.cv_gblur6 = cv2.GaussianBlur(image_inst.cv_gblur5, (kernel, kernel), kernel, image_inst.cv_gblur6, 0)
    cv2.imwrite('..\\images\\gblur6.png', image_inst.cv_gblur6)
    print("gblur6", kernel)

    image_inst.vhf = image_inst.cv_gblur0.astype(np.float64)/255.0 - image_inst.cv_gblur1.astype(np.float64)/255.0
    image_inst.hf = image_inst.cv_gblur1.astype(np.float64)/255.0 - image_inst.cv_gblur2.astype(np.float64)/255.0
    image_inst.mhf = image_inst.cv_gblur2.astype(np.float64)/255.0 - image_inst.cv_gblur3.astype(np.float64)/255.0
    image_inst.mf = image_inst.cv_gblur3.astype(np.float64)/255.0 - image_inst.cv_gblur4.astype(np.float64)/255.0
    image_inst.mlf = image_inst.cv_gblur4.astype(np.float64)/255.0 - image_inst.cv_gblur5.astype(np.float64)/255.0
    image_inst.lf = image_inst.cv_gblur5.astype(np.float64)/255.0 - image_inst.cv_gblur6.astype(np.float64)/255.0
    # remaining blur is the remaining base image with higher frequencies removed
    image_inst.vlf = image_inst.cv_gblur6.astype(np.float64)

    vhf = (image_inst.vhf + 1)/2 * 255
    cv2.imwrite('..\\images\\gb0_vhf.png', vhf.astype(np.uint8))
    hf = (image_inst.hf + 1)/2 * 255
    cv2.imwrite('..\\images\\gb1_hf.png', hf.astype(np.uint8))
    mhf = (image_inst.mhf + 1)/2 * 255
    cv2.imwrite('..\\images\\gb2_mhf.png', mhf.astype(np.uint8))
    mf = (image_inst.mf + 1)/2 * 255
    cv2.imwrite('..\\images\\gb3_mf.png', mf.astype(np.uint8))
    mlf = (image_inst.mlf + 1)/2 * 255
    cv2.imwrite('..\\images\\gb4_mlf.png', mlf.astype(np.uint8))
    lf = (image_inst.lf + 1)/2 * 255
    cv2.imwrite('..\\images\\gb5_lf.png', lf.astype(np.uint8))
    vlf = (image_inst.vlf + 1)/2 * 255
    cv2.imwrite('..\\images\\gb6_vlf.png', vlf.astype(np.uint8))
    # cv2.imwrite('..\\images\\gb6_vlf.png', image_inst.vlf)

    all_img = (image_inst.vhf + image_inst.hf + image_inst.mhf + image_inst.mf + image_inst.mlf +
               image_inst.lf + image_inst.vlf)
    all_img_int = ((all_img + 1)/2) * 255 + image_inst.vlf
    all_freq = all_img_int.astype(np.uint8)
    # array is currently signed integers, convert to unsigned int while saving
    # #TODO: is this right ???????????????????????????????????????
    cv2.imwrite('..\\images\\b_all_freq.png', all_freq)
    cv2.imshow("all frequencies", all_freq)
    cv2.waitKey()
    cv2.destroyAllWindows()
    return all_freq

def initialize_blurs(image_inst):
    shape = image_inst.cv_img_gray.shape
    # blank_gray = np.zeros(shape, dtype=np.int8)
    blank_gray = np.zeros(shape, dtype=np.float64)
    blank_gray_float = np.zeros(shape, dtype=np.float64)
    image_inst.cv_gblur0 = blank_gray.copy()
    image_inst.cv_gblur1 = blank_gray.copy()
    image_inst.cv_gblur2 = blank_gray.copy()
    image_inst.cv_gblur3 = blank_gray.copy()
    image_inst.cv_gblur4 = blank_gray.copy()
    image_inst.cv_gblur5 = blank_gray.copy()
    image_inst.cv_gblur6 = blank_gray.copy()
    image_inst.vhf = blank_gray_float.copy()
    image_inst.hf = blank_gray_float.copy()
    image_inst.mhf = blank_gray_float.copy()
    image_inst.mf = blank_gray_float.copy()
    image_inst.mlf = blank_gray_float.copy()
    image_inst.lf = blank_gray_float.copy()
    image_inst.vlf = blank_gray_float.copy()




