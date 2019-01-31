"""

  Created by Zack and Ed on 1/27/2019
 """
import numpy as np

def slope_compute(matrix):
    left_column = matrix[:, 0]
    right_column = matrix[:, 1]

    left_side_calculation = left_column - right_column
    middle_calculation = right_column - left_column
    right_side_calculation = left_column - right_column

    add_left_and_middle_columns = left_side_calculation + middle_calculation
    add_middle_and_right_columns = middle_calculation + right_side_calculation

    return np.append(add_left_and_middle_columns, add_middle_and_right_columns, axis=1)

def central_dif_cols(array):
    """ add column to each side to facilitate subtraction """
    first_col = array[:, 0: 1]
    last_col = array[:, -1:]
    first_part = np.append(last_col, array, axis=1)
    master_array = np.append(first_part, first_col, axis=1)
    after = master_array[:, 2:]
    before = master_array[:, :-2]
    out_array = (after - before) / 2
    return out_array * -1

def central_dif_rows(array):
    """ add row to top and bottom to facilitate subtraction """
    first_row = array[0: 1, :]
    last_row = array[-1:, :]
    first_part = np.append(last_row, array, axis=0)
    master_array = np.append(first_part, first_row, axis=0)
    after = master_array[2:, :]
    before = master_array[:-2, :]
    out_array = (after - before) / 2
    return out_array * -1

def loop_array_cols(array):
    """ for loop to compute normals """
    out_array = array.copy()
    row_count = array.shape[0]
    col_count = array.shape[1]
    for row_num in range(row_count):
        for col_num in range(col_count):
            if col_num == 0:
                # first column, use wrap of last column instead of previous value
                out_array[row_num, col_num] = (array[row_num, col_num+1] - array[row_num, -1]) / 2
            elif col_num == col_count - 1:
                # last column, use wrap of first column instead of next value
                out_array[row_num, col_num] = (array[row_num, 0] - array[row_num, col_num-1]) / 2
            else:
                # regular processing for all of the middle values
                out_array[row_num, col_num] = (array[row_num, col_num+1] - array[row_num, col_num-1]) / 2
    # out_array consists of slopes, need negative of slopes for normals
    return out_array * -1

def loop_array_rows(array):
    """ for loop to compute normals """
    out_array = array.copy()
    row_count = array.shape[0]
    col_count = array.shape[1]
    for row_num in range(row_count):
        for col_num in range(col_count):
            if row_num == 0:
                # first row, use wrap of last row instead of previous value
                out_array[row_num, col_num] = (array[row_num+1, col_num] - array[-1, col_num]) / 2
            elif row_num == row_count - 1:
                # last row, use wrap of first row instead of next value
                out_array[row_num, col_num] = (array[0, col_num] - array[row_num-1, col_num]) / 2
            else:
                # regular processing for all of the middle values
                out_array[row_num, col_num] = (array[row_num+1, col_num] - array[row_num-1, col_num]) / 2
    # out_array consists of slopes, need negative of slopes for normals
    return out_array * -1



