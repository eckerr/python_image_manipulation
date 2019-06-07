"""
blurs.py - performs a series of blurs for creating normals

  Created by Ed on 5/20/2019
 """

import cv2
import numpy as np

def bilat_blur(src, kernel, dst, freq):
    cv2.bilateralFilter(src, kernel, kernel*2, kernel/2, dst, cv2.BORDER_WRAP)
    freq = src.astype(np.float) - dst.astype(np.float)
    cv2.imwrite('..\\images\\blur0.png', freq.astype(np.int8))

def blurs(image_inst):
    # freq = image_inst.hf
    kernel = 3
    src = image_inst.cv_img_gray
    dst = image_inst.cv_blur0
    image_inst.cv_blur0 = image_inst.cv_img_gray.copy()
    cv2.imwrite('..\\images\\blur0.png', image_inst.cv_blur0)
    print("blur0")
    image_inst.cv_blur1 = cv2.bilateralFilter(image_inst.cv_blur0, 3, 7, 3, image_inst.cv_blur1, cv2.BORDER_WRAP)
    cv2.imwrite('..\\images\\blur1.png', image_inst.cv_blur1)
    print("blur1")
    image_inst.cv_blur2 = cv2.bilateralFilter(image_inst.cv_blur1, 9, 15, 7, image_inst.cv_blur2, cv2.BORDER_WRAP)
    cv2.imwrite('..\\images\\blur2.png', image_inst.cv_blur2)
    print("blur2")
    image_inst.cv_blur3 = cv2.bilateralFilter(image_inst.cv_blur2, 27, 31, 15, image_inst.cv_blur3, cv2.BORDER_WRAP)
    cv2.imwrite('..\\images\\blur3.png', image_inst.cv_blur3)
    print("blur3")
    image_inst.cv_blur4 = cv2.bilateralFilter(image_inst.cv_blur3, 81, 63, 31, image_inst.cv_blur4, cv2.BORDER_WRAP)
    cv2.imwrite('..\\images\\blur4.png', image_inst.cv_blur4)
    print("blur4")
    image_inst.cv_blur5 = cv2.bilateralFilter(image_inst.cv_blur4, 163, 123, 61, image_inst.cv_blur5, cv2.BORDER_WRAP)
    cv2.imwrite('..\\images\\blur5.png', image_inst.cv_blur5)
    print("blur5")
    image_inst.cv_blur6 = cv2.bilateralFilter(image_inst.cv_blur5, 251, 199, 121, image_inst.cv_blur6, cv2.BORDER_WRAP)
    cv2.imwrite('..\\images\\blur6.png', image_inst.cv_blur6)
    print("blur6")

    image_inst.vhf = image_inst.cv_blur0.astype(np.float)/255 - image_inst.cv_blur1.astype(np.float)/255
    image_inst.hf = image_inst.cv_blur1.astype(np.float)/255 - image_inst.cv_blur2.astype(np.float)/255
    image_inst.mhf = image_inst.cv_blur2.astype(np.float)/255 - image_inst.cv_blur3.astype(np.float)/255
    image_inst.mf = image_inst.cv_blur3.astype(np.float)/255 - image_inst.cv_blur4.astype(np.float)/255
    image_inst.mlf = image_inst.cv_blur4.astype(np.float)/255 - image_inst.cv_blur5.astype(np.float)/255
    image_inst.lf = image_inst.cv_blur5.astype(np.float)/255 - image_inst.cv_blur6.astype(np.float)/255
    # remaining blur is the remaining base image with higher frequencies removed
    image_inst.vlf = image_inst.cv_blur6

    vhf = (image_inst.vhf + 1)/2 * 255
    cv2.imwrite('..\\images\\b0_vhf.png', vhf.astype(np.int8))
    hf = (image_inst.hf + 1)/2 * 255
    cv2.imwrite('..\\images\\b1_hf.png', hf.astype(np.int8))
    mhf = (image_inst.mhf + 1)/2 * 255
    cv2.imwrite('..\\images\\b2_mhf.png', mhf.astype(np.int8))
    mf = (image_inst.mf + 1)/2 * 255
    cv2.imwrite('..\\images\\b3_mf.png', mf.astype(np.int8))
    mlf = (image_inst.mlf + 1)/2 * 255
    cv2.imwrite('..\\images\\b4_mlf.png', mlf.astype(np.int8))
    lf = (image_inst.lf + 1)/2 * 255
    cv2.imwrite('..\\images\\b5_lf.png', lf.astype(np.int8))
    # vlf =(image_inst.vlf + 1)/2 * 255
    # cv2.imwrite('..\\images\\b6_vlf.png', vlf.astype(np.int8))
    cv2.imwrite('..\\images\\b6_vlf.png', image_inst.vlf)

    all_img = (image_inst.vhf + image_inst.hf + image_inst.mhf + image_inst.mf + image_inst.mlf +\
              image_inst.lf)  # + image_inst.vlf)
    all_img_int = ((all_img + 1)/2) * 255 + image_inst.vlf
    all_freq = all_img_int.astype(np.int8)
    # array is currently signed integers, convert to unsigned int while saving
    cv2.imwrite('..\\images\\b_all_freq.png', all_freq + 128)
    cv2.imshow("all frequencies", all_freq)
    cv2.waitKey()
    cv2.destroyAllWindows()
    return all_freq

def initialize_blurs(image_inst):
    shape = image_inst.cv_img_gray.shape
    blank_gray = np.zeros(shape, dtype=np.int8)
    blank_gray_float = np.zeros(shape, dtype=np.float32)
    image_inst.cv_blur0 = blank_gray.copy()
    image_inst.cv_blur1 = blank_gray.copy()
    image_inst.cv_blur2 = blank_gray.copy()
    image_inst.cv_blur3 = blank_gray.copy()
    image_inst.cv_blur4 = blank_gray.copy()
    image_inst.cv_blur5 = blank_gray.copy()
    image_inst.cv_blur6 = blank_gray.copy()
    image_inst.vhf = blank_gray_float.copy()
    image_inst.hf = blank_gray_float.copy()
    image_inst.mhf = blank_gray_float.copy()
    image_inst.mf = blank_gray_float.copy()
    image_inst.mlf = blank_gray_float.copy()
    image_inst.lf = blank_gray_float.copy()
    image_inst.vlf = blank_gray_float.copy()




