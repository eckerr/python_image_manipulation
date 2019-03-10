"""

  Created by Zack and Ed on 1/27/2019
 """
import numpy as np

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



