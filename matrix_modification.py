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
grayscale_matrix = cv2.imread('brick.jpg', 0)

cv2.imshow('grayscale', grayscale_matrix)

grayscale_matrix = grayscale_matrix.astype(np.float32)


# Column matrix code
# rotate matrix left one column
first_col = grayscale_matrix[:, :1]
last_cols = grayscale_matrix[:, 1:]
next_col_slope = np.append(last_cols, first_col, axis=1)
# rotate matrix right one column
last_col = grayscale_matrix[:, -1:]
first_cols = grayscale_matrix[:, :-1]
prev_col_slope = np.append(last_col, first_cols, axis=1)

# subtracted column values
x_slope_at_point = next_col_slope - prev_col_slope

# row matrix code
# rotate matrix up one row
first_row = grayscale_matrix[:1, :]
last_rows = grayscale_matrix[1:, :]
next_row_slope = np.append(last_rows, first_row, axis=0)
# rotate matrix down one row
last_row = [grayscale_matrix[-1, :]]
first_rows = grayscale_matrix[:-1, :]
prev_row_slope = np.append(last_row, first_rows, axis=0)

# Subtracted row values
y_slope_at_point = next_row_slope - prev_row_slope

normalize_col_matrix = (x_slope_at_point * 0.5) + 127.5

normal_col = np.array(normalize_col_matrix, dtype=np.uint8)
cv2.imshow('column_matrix', normal_col)


# Subtraction of values (Row)
normalize_row_matrix = (y_slope_at_point * 0.5) + 127.5

normal_row = np.array(normalize_row_matrix, dtype=np.uint8)
cv2.imshow('row_matrix', normal_row)

merged = cv2.merge([grayscale_matrix, normal_row, normal_col])
cv2.imshow('final_picture', merged)

unsigned_column_matrix = normalize_col_matrix.astype(np.uint8)

cv2.imshow('image', unsigned_column_matrix)
cv2.waitKey(0)
cv2.destroyAllWindows()

#cv2.imwrite('Brick_Column.jpg', unsigned_column_matrix)
