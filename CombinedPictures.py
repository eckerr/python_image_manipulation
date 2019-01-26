"""

  Created by Ed and Zack on 1/11/2019
 """

import cv2
import numpy as np

img1 = cv2.imread('brick.jpg', 0)
img3 = cv2.imread('Brick_Row.jpg', 0)
img2 = cv2.imread('Brick_Column.jpg', 0)
panels = []
panels.append(img1)
panels.append(img2)
panels.append(img3)

merged = cv2.merge(panels)

cv2.imshow('grayscale', img1)
cv2.imshow('rows', img2)
cv2.imshow('columns', img3)
cv2.imshow('merged', merged)

cv2.imwrite('Brick_Normal.jpg', merged)

add = cv2.add(merged, merged)
cv2.imwrite('Brick_Normal2.jpg', add)

cv2.imshow('Addition.jpg', add)

rust_diffuse_img = cv2.imread('rust_014.jpg')
cv2.imshow('rust Diffuse', rust_diffuse_img)

rust_img = cv2.imread('rust_normal.jpg')
cv2.imshow('rust Normal', rust_img)

rust_grayscale = cv2.imread('rust_014.jpg', 0)
cv2.imshow('rust grayscale', rust_grayscale)

panel = []
my_panels = cv2.split(rust_img, panel)
blue = my_panels[0]
green = my_panels[1]
red = my_panels[2]

new_panel = cv2.merge(my_panels)
cv2.imshow('merged_split', new_panel)

#blue[1] *= 0
#blue[1] += 128
#blue[2] *= 0
#blue[2] += 128
#blue_only = cv2.merge(blue)
#cv2.imshow('blue only', blue_only)

#green[0] *= 0
#green[0] += 128
#green[2] *= 0
#green[2] += 128
#green_only = cv2.merge(green)
#cv2.imshow('green only', green_only)

#red[0] *= 0
#red[0] += 128
#red[1] *= 0
#red[1] += 128
#red_only = cv2.merge(red)
#cv2.imshow('red only', red_only)
cv2.imshow('red', red)
cv2.imshow('green', green)
cv2.imshow('blue', blue)

cv2.waitKey(0)
cv2.destroyAllWindows()
