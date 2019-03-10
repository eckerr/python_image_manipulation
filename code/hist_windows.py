"""

  Created by Ed and Zack on 2/15/2019
 """

import sys
import cv2
import numpy as np
from histograms import hist_lines, hist_curve, hist_curve_split, hist_lines_split

if len(sys.argv) > 1:
    fname = sys.argv[1]
else:
    fname = '..\\images\\brick.jpg'
    print("usage: python hist_windows.py <image_file>")

image = cv2.imread(fname)

if image is None:
    print('Failed to load image file:', fname)
    sys.exit(1)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

print(''' Histogram plotting \n
Keymap:\n
a - show histogram for color image in curve mode \n
b - show histogram in bin mode \n
c - show equalized histogram (always in bin mode) \n
d - show histogram for color image in curve mode \n
e - show histogram for a normalized image in curve mode \n
Esc - exit \n
''')

cv2.imshow('image', image)
while True:
    k = cv2.waitKey(0)
    if k == ord('a'):
        curve = hist_curve(image)
        cv2.imshow('histogram', curve)
        cv2.imshow('image', image)
        print('a')

    elif k == ord('b'):
        print('b')
        lines = hist_lines(image)
        cv2.imshow('histogram', lines)
        cv2.imshow('image', gray)

    elif k == ord('c'):
        print('c')
        equ = cv2.equalizeHist(gray)
        lines = hist_lines(equ)
        cv2.imshow('image', equ)
        cv2.imshow('histogram', lines)

    elif k == ord('d'):
        print('d')
        curve = hist_curve(gray)
        cv2.imshow('histogram', curve)
        cv2.imshow('image', gray)

    elif k == ord('e'):
        print('e')
        norm = cv2.normalize(gray, gray, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        lines = hist_lines(norm)
        cv2.imshow('histogram', lines)
        cv2.imshow('image', norm)

    elif k == ord('f'):
        print('f')
        hist_pics = hist_curve_split(image)
        hist_pics[3] = hist_curve(gray)
        res = np.vstack((hist_pics[0], hist_pics[1], hist_pics[2], hist_pics[3]))
        cv2.imshow('histogram', res)
        cv2.imshow('image', image)

    elif k == ord('g'):
        print('g')
        hist_pics = hist_lines_split(image)
        hist_pics[3] = hist_lines(gray)
        res = np.vstack((hist_pics[0], hist_pics[1], hist_pics[2], hist_pics[3]))
        cv2.imshow('histogram', res)
        cv2.imshow('image', image)

    elif k == 27:
        print('ESC')
        cv2.destroyAllWindows()
        break
cv2.destroyAllWindows()




