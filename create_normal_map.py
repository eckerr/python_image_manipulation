"""
create_normal_map.py
Steps to creating a normal map from a grayscale image

  Created by Ed and Zack on 1/22/2019
 """
import cv2
import numpy as np
from slope_math import central_dif_cols, central_dif_rows


def read_image_to_gray(file):
    gray = cv2.imread(file, 0)
    return gray


def convert_array_to_float(array):
    return array.astype(np.float32)


def normalize_float_array(array):
    return array / 255


def convert_signed_channel_to_image(channel):
    """channel contains float values between -1 and 1"""
    float_array = ((channel + 1) / 2) * 255
    return np.array(float_array, dtype=np.uint8)


def convert_unsigned_channel_to_image(channel):
    """ channel contains float values between 0 and 1 """
    float_array = channel * 255
    return np.array(float_array, dtype=np.uint8)


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


def display_grayscale(grayscale_array):
    cv2.imshow('grayscale', grayscale_array)


def display_channel_list(channels):
    cv2.imshow('Blue', channels[0])
    cv2.imshow('Green', channels[1])
    cv2.imshow('Red', channels[2])


def build_normal_image(col_array, row_array):
    """ start building channels from slope info """
    # create an array to hold the channels
    size = col_array.shape
    blank_array = np.zeros((size[0], size[1], 3))
    channels = []
    channels = cv2.split(blank_array, channels)
    for row in range(size[0]):
        for col in range(size[1]):
            dx = col_array[row, col]
            dx2 = dx * dx
            dy = row_array[row, col]
            dy2 = dy * dy
            sum_of_squares = dx2 + dy2 + 1
            distance = np.sqrt(sum_of_squares)
            # blue channel
            channels[0][row, col] = 1 / distance
            # green channel
            channels[1][row, col] = dx / distance
            # red channel
            channels[2][row, col] = dy / distance
    return convert_channels_to_images(channels)


def display_normal_image(channels):
    normal_img = cv2.merge(channels)
    cv2.imshow('normal', normal_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def convert_channels_to_images(channels):
    """ changes channel to be uint8 compliant """
    # blue channel
    channels[0] = convert_unsigned_channel_to_image(channels[0])
    # green channel
    channels[1] = convert_signed_channel_to_image(channels[1])
    # red channel
    channels[2] = convert_signed_channel_to_image((channels[2]))
    return channels


def process_image(img_in):
    float_array = convert_array_to_float(img_in)
    n_float = normalize_float_array(float_array)
    y_array = central_dif_rows(n_float)
    x_array = central_dif_cols(n_float)
    channels = build_normal_image(y_array, x_array)
    # display
    display_grayscale(img_in)
    display_channel_list(channels)
    display_normal_image(channels)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':

    filename = 'brick.jpg'
    image_in = read_image_to_gray(filename)
    original = cv2.imread(filename)
    cv2.imshow('original', original)
    process_image(image_in)







