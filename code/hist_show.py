"""
hist_show.py
  Created by Ed on 7/17/2019
 """

import cv2
import numpy as np
import create_normal_map as cn


def count_blue(my_blu):
    my_dict = {}
    for i in range(my_blu.shape[0]):
        for j in range(my_blu.shape[1]):
            if my_dict[my_blu[i][j]]:
                my_dict[my_blu[i][j]] += 1
            else:
                my_dict[my_blu[i][j]] = 1
    return my_dict

def scale_blues():
    for i in range(7):
        # read a normal image
        filename = '..\\images\\a_blur' + str(i) + '.png'
        img_in = cv2.imread(filename)
        print(filename)
        # retrieve blue channel only
        blue_only = img_in[:, :, 0].astype(np.float32)
        # normalize range
        blue_only = cv2.normalize(blue_only, blue_only, 255, 0, norm_type=cv2.NORM_MINMAX)
        fileout = '..\\images\\aa_blue' + str(i) + '.png'
        cv2.imwrite(fileout, blue_only.astype(np.uint8))


if __name__ == '__main__':

    norm_img = cv2.imread('..\\images\\old\\qb912_normal.jpg')
    cv2.imshow('norm_img', norm_img); cv2.waitKey(0); cv2.destroyAllWindows()

    blue, green, red = cn.image_parts_to_colors(norm_img)
    cv2.imshow('norm_img', np.hstack((blue, green))); cv2.waitKey(0); cv2.destroyAllWindows()



