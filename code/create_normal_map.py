"""
create_normal_map.py
Steps to creating a normal map from a grayscale image

  Created by Ed and Zack on 1/22/2019
 """
import numpy as np
import cv2 as cv2


def add_channels(channel_list):
    """ adds and scales channels based on pre-determined scale factors """
    normal_channel = channel_list[0].copy()
    scale_factor = [.03125, .0625, .125, .25, .5, 1]
    for i in range(1, len(channel_list)):
        for j in range(3):
            normal_channel[j] += channel_list[i][j] * scale_factor[i]
    return normal_channel


def array_to_prev_next():
    pass


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


def build_normal_image(col_array, row_array, channels):
    """ start building tangent-space channels from slope info

        blue channel is set to 1
        """
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


def convert_array_to_float(array):
    """ Image files use unsigned integers, convert to float 32 for math manipulations"""
    return array.astype(np.float32)


def convert_signed_channel_to_image(channel):
    """channel contains float values between -1 and 1"""
    float_array = ((channel + 1) / 2) * 255
    return np.array(float_array, dtype=np.uint8)


def convert_signed_channels_to_uint8_channels(channels):
    """ changes channel list to be uint8 compliant """
    for i in range(len(channels)):
        channels[i] = convert_signed_channel_to_image(channels[i])
    return channels


def convert_unsigned_channel_to_image(channel):
    """ channel contains float values between 0 and 1 """
    float_array = channel * 255
    return np.array(float_array, dtype=np.uint8)


def central_dif_cols(array):
    """ add column to each side to facilitate subtraction
        subtract and return difference values for core section """
    first_col = array[:, 0:1]
    last_col = array[:, -1:]
    first_part = np.append(last_col, array, axis=1)
    master_array = np.append(first_part, first_col, axis=1)
    after = master_array[:, 2:]
    before = master_array[:, :-2]
    out_array = (after - before) / 2
    return out_array


def central_dif_rows(array):
    """ add row to top and bottom to facilitate subtraction
        subtract and return difference values for core section """
    first_row = array[0:1, :]
    last_row = array[-1:, :]
    first_part = np.append(last_row, array, axis=0)
    master_array = np.append(first_part, first_row, axis=0)
    after = master_array[2:, :]
    before = master_array[:-2, :]
    out_array = (after - before) / 2
    return out_array


def create_array_of_3_channels(size):
    """ build a ones-filled list of 3 arrays of needed size """
    blank_array = np.ones((size[0], size[1], 3))
    channels = []
    return cv2.split(blank_array, channels)


def create_black_window():
    pass
    # img = np.zeros((size[0], size[1], 3), np.uint8)
    # return cv2.namedWindow("image")


def display_channel_list(channel_list):
    cv2.imshow("Blue", channel_list[0])
    cv2.imshow("Green", channel_list[1])
    cv2.imshow("Red", channel_list[2])


def display_grayscale(grayscale_array):
    cv2.imshow("grayscale", grayscale_array)


def display_normal_image(channel_list):
    normal_img = cv2.merge(channel_list)
    cv2.imshow("image", normal_img)
    return normal_img


def invert_image(image_array):
    """ Inverts 8 bit image """
    return 255 - image_array


def image_parts_to_colors(image):
    """ separate color channels for display as color images """
    blue = (image.copy() * [1, 0, 0]).astype(np.uint8)
    green = (image.copy() * [0, 1, 0]).astype(np.uint8)
    red = (image.copy() * [0, 0, 1]).astype(np.uint8)
    return blue, green, red


def normalize_float_array(array):
    """ normalize positive image values for math manipulations """
    return array / 255


def process_image(img_in):
    # create a single normal map
    float_array = convert_array_to_float(img_in)
    n_float = normalize_float_array(float_array)
    y_slopes = central_dif_rows(n_float)
    x_slopes = central_dif_cols(n_float)
    y_norms = y_slopes * -1
    x_norms = x_slopes * -1
    raw_channel_list = [n_float, y_norms, x_norms]
    scaled_channel_list = rescale_x_y(raw_channel_list, 1)
    r_scaled_channel_list = rebalance_norms(scaled_channel_list)

    channel_list = convert_signed_channels_to_uint8_channels(r_scaled_channel_list)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return channel_list


def read_image_to_gray(file):
    gray = cv2.imread(file, 0)
    return gray


def rebalance_all(multi_channels):
    new_list = []
    for channels in multi_channels:
        new_list.append(rebalance_norms(channels))
    return new_list


def rebalance_norms(channel_list):
    size = channel_list[0].shape
    f = np.zeros(3, dtype=np.float32)
    for row in range(size[0]):
        for col in range(size[1]):
            dx = channel_list[1][row, col]
            dy = channel_list[2][row, col]
            dz = 1
            vector = np.array([dx, dy, dz], dtype=np.float32)
            f = cv2.normalize(vector, f)
            channel_list[1][row, col] = f[0]
            channel_list[2][row, col] = f[1]
            channel_list[0][row, col] = f[2]
    return channel_list


def remove_bias(array):
    return array.astype(np.float32) - np.mean(array.astype(np.float32))


def rescale_x_y(channel_float_list, scale_factor):
    # determine max and min to scale by
    green_range = channel_float_list[1].max() - channel_float_list[1].min()
    red_range = channel_float_list[2].max() - channel_float_list[2].min()
    s_range = max(green_range, red_range) / 2
    max_scale = 1 / s_range
    scale_val = max_scale * scale_factor
    channel_float_list[1] *= scale_val
    channel_float_list[2] *= scale_val
    print(max_scale, scale_factor)

    return channel_float_list


def rework_channels(channels_list):
    # take list of channels of normal maps ranging from vhf to lf and remove bias and normalize
    new_list = []
    new_channel = []
    for channel in channels_list:
        for i in range(3):
            temp_chan = convert_array_to_float(channel[i])
            temp_chan = normalize_float_array(temp_chan)
            new_channel.append(remove_bias(temp_chan))
        new_list.append(new_channel)
        new_channel = []
    return new_list


def scale_callback():
    pass


if __name__ == "__main__":

    filename = "..\\images\\qbA.png"
    filenameO = "..\\images\\qb2_output_normal.jpg"
    filenameN = "..\\images\\qb912_normal.jpg"

    image_in = read_image_to_gray(filename)
    channels_out = process_image(image_in)
    n_img_out = display_normal_image(channels_out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite(filenameO, n_img_out)
    print("we got to end")
