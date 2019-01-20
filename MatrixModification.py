"""
  Created by Ed and Zack on 1/4/2019
 """
import numpy as np
import cv2

mf_normal = cv2.imread('Marblefloor_normal.jpg')
mf_panels = []
mf_panels = cv2.split(mf_normal, mf_panels)
cv2.imshow('mf blue', mf_panels[0])
cv2.imshow('mf green', mf_panels[1])
cv2.imshow('mf red', mf_panels[2])


# initialize matrices
grayscaleMatrix = cv2.imread('Marblefloor_diffuse.jpg', 0)

cv2.imshow('grayscale', grayscaleMatrix)

# Column matrix code
first_col = grayscaleMatrix[:, :1]
other_Col = grayscaleMatrix[:, 1:]

edited_col_Matrix = np.append(other_Col, first_col, axis=1)

# row matrix code
first_row = grayscaleMatrix[:1, :]
other_rows = grayscaleMatrix[1:, :]

edited_row_Matrix = np.append(other_rows, first_row, axis=0)

# Subtraction of values (Column)

subtracted_col_Matrix = grayscaleMatrix - edited_col_Matrix

normalize_col_Matrix = (subtracted_col_Matrix * 0.5) + 127.5

normal_col = np.array(normalize_col_Matrix, dtype=np.uint8)
cv2.imshow('column_matrix', normal_col)


# Subtraction of values (Row)

subtracted_row_Matrix = grayscaleMatrix - edited_row_Matrix

normalize_row_Matrix = (subtracted_row_Matrix * 0.5) + 127.5

normal_row = np.array(normalize_row_Matrix, dtype=np.uint8)
cv2.imshow('row_matrix', normal_row)

merged = cv2.merge([grayscaleMatrix, normal_row, normal_col])
cv2.imshow('final_picture', merged)

#unsignedColumnMatrix = np.uint8(normalize_col_Matrix)

#cv2.imshow('image', unsignedColumnMatrix)
cv2.waitKey(0)
cv2.destroyAllWindows()

#cv2.imwrite('Brick_Column.jpg', unsignedColumnMatrix)
