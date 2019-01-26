"""
create_normal_map.py
Steps to creating a normal map from a grayscale image

  Created by Ed and Zack on 1/22/2019
 """
import cv2
import numpy as np

def read_image_to_gray(filename):
    return cv2.imread(filename, 0)

def convert_array_to_float(array):
    return np.array(array, dtype=np.float64)

def normalize_float_array(array):
    return array / 255

def array_to_prev_next(array, axis):
    if axis == 0:
        first = array[:1, :]
        others = array[1:, :]
        next_rows = np.append(others, first, axis=0)
        last = [array[-1, :]]
        firsts = array[:-1, :]
        prev_rows = np.append(last, firsts, axis=0)
        return [prev_rows, next_rows]
    else:
        first = array[:, :1]
        others = array[:, 1:]
        next_cols = np.append(others, first, axis=1)
        last = array[:, -1:]
        firsts = array[:, : -1]
        prev_cols = np.append(last, firsts, axis=1)
        return [prev_cols, next_cols]

def calculate_prev_next_slopes(prev_next_array):
    pass

def calculate_slope_at_points(prev_next_slopes):
    pass

def create_BGR_channels():
    pass

def normalize_unit_vectors():
    pass

def convert_signed_channel_to_image(channel):

    """channel contains float values between -1 and 1"""
    float_array = ((channel + 1) / 2) * 255
    return np.array(float_array, dtype=np.uint8)
def convert_unsigned_channel_to_image(channel):
    """ channel contains float values between 0 and 1 """
    float_array = channel * 255
    return np.array(float_array, dtype=np.uint8)

def display_grayscales(grayscale_matrix):
    cv2.imshow('grayscale', grayscale_matrix)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def build_normal_image():
    pass

def display_normal_image():
    pass







