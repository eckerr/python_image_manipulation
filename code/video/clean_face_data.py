"""
limit_out_of_range.py
  limit x and y values if upper_left_corner of the range of interest gets too close
  to the edge of the frame  TODO: may want to move this to a different part of the process

  Created by Ed on 1/20/2020
 """

import csv

in_filename = 'MVI_9468_small_p.csv'
out_filename = None
count_low_x = 0
count_high_x = 0
count_low_y = 0
count_high_y = 0
count_bad_size = 0
count_bad_x_rate = 0

size_min_x = 47
size_min_y = 47
size_max_x = 67
size_max_y = 67

last_ul_x = 0
last_ul_y = 0
last_frame_num = 0
rate_of_change_x = 0
rate_of_change_y = 0
rate_of_change_limit = 3
ACT = 0
EST = 1

frame_width_min = 50
frame_width_max = 960 - 325
frame_height_min = 50
frame_height_max = 540 - 325

def check_UL_values():
    global ul_x, ul_y, count_low_x, count_high_x, count_low_y, count_high_y
    # check if bounding-box reaches frame boundaries, if so,
    # stop window at boundary
    if ul_x < frame_width_min:
        count_low_x += 1
        # print(frame_num, ul_x, ul_y, f_width, f_height, 'low ul_x')
        ul_x = frame_width_min
    if ul_x > frame_width_max:
        count_high_x += 1
        # print(frame_num, ul_x, ul_y, f_width, f_height, 'high ul_x')
        ul_x = frame_width_max
    if ul_y < frame_height_min:
        count_low_y += 1
        # print(frame_num, ul_x, ul_y, f_width, f_height, 'low ul_y')
        ul_y = frame_height_min
    if ul_y > frame_height_max:
        count_high_y += 1
        # print(frame_num, ul_x, ul_y, f_width, f_height, 'high ul_y')
        ul_y = frame_height_max
    return count_high_x, count_high_y, count_low_x, count_low_y


def check_size_values():
    # test whether to remove this value from file (out of range)
    global count_bad_size
    if f_width < size_min_x or f_width > size_max_x or f_height < size_min_y or f_height > size_max_y:
        count_bad_size += 1
        # print(row, "bad size")
        # suspect value, drop this frame from the list
        return False
    else:
        # values appear to be in range - safe to write
        return True

def compute_rate_of_change_x():
    valid = False
    frame_dif = frame_num - last_frame_num
    ul_x_dif = ul_x - last_ul_x
    ul_y_dif = ul_y - last_ul_y

    x_rate = abs(ul_x_dif / frame_dif)
    y_rate = abs(ul_y_dif / frame_dif)

    if x_rate < rate_of_change_limit:
        valid = True

    return x_rate, y_rate, valid


if __name__ == '__main__':

    with open(in_filename, 'r') as in_file:
        reader = csv.reader(in_file)

        # setup output file
        out_filename = in_filename[:-11] + 'clean.csv'
        with open(out_filename, 'w', newline='') as out_file:
            writer = csv.writer(out_file)
            first_time = True
            for row in reader:
                # load entry
                frame_num = int(row[0])
                ul_x = int(row[1])
                ul_y = int(row[2])
                f_width = int(row[3])
                f_height = int(row[4])

                # disregard first row for differences
                if first_time:
                    last_frame_num = frame_num -1
                    first_time = False
                    # write the first found record
                    writer.writerow([frame_num, ul_x, ul_y, f_width,
                                     f_height, 0.0, 0.0])
                    last_frame_num = frame_num
                    last_ul_x = ul_x
                    last_ul_y = ul_y

                else:
                    check_UL_values()
                    rate_of_change_x, rate_of_change_y, valid_rate = \
                        compute_rate_of_change_x()
                    if check_size_values():
                        if valid_rate:
                            writer.writerow([frame_num, ul_x, ul_y, f_width,
                                             f_height, rate_of_change_x, rate_of_change_y])
                            # update values of previous
                            last_frame_num = frame_num
                            last_ul_x = ul_x
                            last_ul_y = ul_y
                        else:
                            count_bad_x_rate += 1
            # print counts changed
            print('Changes made to file:')
            print('\tLow x count: ', count_low_x)
            print('\tHigh x count: ', count_high_x)
            print('\tLow y count: ', count_low_y)
            print('\tHigh y count: ', count_high_y)
            print('\tBad size count: ', count_bad_size)
            print('\tBad x change rate count: ', count_bad_x_rate)

            print('Cleaned data saved as ', out_filename)




