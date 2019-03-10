"""
create_normal_map.py
Steps to creating a normal map from a grayscale image

  Created by Ed and Zack on 1/22/2019
 """
import cv2
import numpy as np


def read_image_to_gray(file):
    gray = cv2.imread(file, 0)
    return gray


def invert_image(image_array):
    """ Inverts 8 bit image """
    return 255 - image_array


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
    first_col = array[:, 0:1]
    last_col = array[:, -1:]
    first_part = np.append(last_col, array, axis=1)
    master_array = np.append(first_part, first_col, axis=1)
    after = master_array[:, 2:]
    before = master_array[:, :-2]
    out_array = (after - before) / 2
    return out_array


def central_dif_rows(array):
    """ add row to top and bottom to facilitate subtraction """
    first_row = array[0:1, :]
    last_row = array[-1:, :]
    first_part = np.append(last_row, array, axis=0)
    master_array = np.append(first_part, first_row, axis=0)
    after = master_array[2:, :]
    before = master_array[:-2, :]
    out_array = (after - before) / 2
    return out_array


def display_grayscale(grayscale_array):
    cv2.imshow("grayscale", grayscale_array)


def display_channel_list(channel_list):
    cv2.imshow("Blue", channel_list[0])
    cv2.imshow("Green", channel_list[1])
    cv2.imshow("Red", channel_list[2])


def create_array_of_3_channels(size):
    # build a blank array of needed size
    blank_array = np.ones((size[0], size[1], 3))
    channels = []
    return cv2.split(blank_array, channels)


def build_normal_image(col_array, row_array, channels):
    """ start building channels from slope info """
    size = channels[0].shape
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
            channels[1][row, col] = -dx / distance
            # red channel
            channels[2][row, col] = -dy / distance
    return channels


def balance_norms(channel_list):
    size = channel_list[0].shape
    f = np.zeros(3, dtype=np.float32)
    for row in range(size[0]):
        for col in range(size[1]):
            dx = channel_list[1][row, col]
            dy = channel_list[2][row, col]
            dz = channel_list[0][row, col]
            vector = np.array([dx, dy, dz], dtype=np.float32)
            f = cv2.normalize(vector, f)
            channel_list[1][row, col] = f[0]
            channel_list[2][row, col] = f[1]
            channel_list[0][row, col] = f[2]
    return channel_list


def rescale_x_y(channel_float_list, scale_factor):
    # determine max and min to scale by
    green_range = channel_float_list[1].max() - channel_float_list[1].min()
    red_range = channel_float_list[2].max() - channel_float_list[2].min()
    range = max(green_range, red_range) / 2
    max_scale = 1 / range
    scale_val = max_scale * scale_factor
    channel_float_list[1] *= scale_val
    channel_float_list[2] *= scale_val
    print(max_scale, scale_factor)

    return channel_float_list


def display_normal_image(channel_list):
    normal_img = cv2.merge(channel_list)
    cv2.imshow("image", normal_img)
    return normal_img
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def convert_channels_to_images(channels):
    """ changes channel to be uint8 compliant """
    # blue channel
    channels[0] = convert_signed_channel_to_image(channels[0])
    # green channel
    channels[1] = convert_signed_channel_to_image(channels[1])
    # red channel
    channels[2] = convert_signed_channel_to_image((channels[2]))
    return channels


def create_black_window(size):
    img = np.zeros((size[0], size[1], 3), np.uint8)
    return cv2.namedWindow("image")


def scale_callback(x):
    pass


def process_image(img_in):
    float_array = convert_array_to_float(img_in)
    n_float = normalize_float_array(float_array)
    y_slopes = central_dif_rows(n_float)
    x_slopes = central_dif_cols(n_float)
    y_norms = y_slopes * -1
    x_norms = x_slopes * -1
    # blank_channels = create_array_of_3_channels(y_slopes.shape)

    raw_channel_list = [n_float, y_norms, x_norms]
    scaled_channel_list = rescale_x_y(raw_channel_list, .5)
    #channel_list = convert_channels_to_images(raw_channel_list)
    r_scaled_channel_list = balance_norms(scaled_channel_list)
    channel_list = convert_channels_to_images(r_scaled_channel_list)
    # display
    display_grayscale(img_in)
    display_channel_list(channel_list)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return channel_list


if __name__ == "__main__":

    #filename = "..\\images\\Marblefloor_paintedblur.jpg"
    #filenameN = "..\\images\\Marblefloor_normal.jpg"

    # filename = "..\\images\\Marblefloor_diffuse.jpg"
    # filenameN = "..\\images\\Marblefloor_normal.jpg"

    filename = "..\\images\\qb2.jpg"
    filenameN = "..\\images\\qb912_normal.jpg"

    #filename = '..\\images\\brick.jpg'
    #filenameN = '..\\images\\brick_normal.jpg'

    #filename = '..\\images\\rust_014.jpg'
    #filenameN = '..\\images\\rust_normal.jpg'

    # filename = '..\\images\\Voronoi.png'
    # filenameN = '..\\images\\Voronoi.png'

    image_in = read_image_to_gray(filename)
    original = cv2.imread(filename)
    cv2.imshow("original", original)
    img_window = create_black_window(image_in.shape)
    channels_out = process_image(image_in)
    n_img_out = display_normal_image(channels_out)
    image_ref = cv2.imread(filenameN)
    res = np.hstack((n_img_out, image_ref))
    cv2.imshow('ours / reference', res)
    cv2.imshow(img_window, image_ref)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite("E2_N_" + filenameN, n_img_out)
