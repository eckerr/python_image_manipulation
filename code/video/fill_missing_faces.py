"""
fill_missing_faces.py
  fills blanks in front_faces.csv file
  by interpolating between known positions

  Created by Ed on 1/10/2020
 """

import csv

counter = 0
last_ul_x = 0
last_ul_y = 0
ACT = 0
EST = 1

in_filename = 'MVI_9464_clean.csv'
out_filename = in_filename[:-9] + 'filled.csv'

# open the file for processing
with open(in_filename, 'r') as in_file:
    reader = csv.reader(in_file)
    with open(out_filename, 'w', newline='') as out_file:
        writer = csv.writer(out_file)

        for row in reader:
            counter += 1
            frame_num = int(row[0])
            ul_x = int(row[1])
            ul_y = int(row[2])
            f_width = int(row[3])
            f_height = int(row[4])
            # columns 5, 6 x and y rates_of_change not being used

            # frame_num, ul_x, ul_y, f_width, f_height = int(row[0]), int(row[1]), int(row[2], int(row[3]), int(row[4])
            # print(frame_num, ul_x, ul_y, f_width, f_height)

            if frame_num > counter:
                # need to fill missing data
                if counter == 1:
                    # special case, don't know what initial values
                    # should be, will assume stationary
                    while counter < frame_num:
                        writer.writerow([counter, int(ul_x), int(ul_y), f_width, f_height, EST])
                        counter += 1
                else:
                    # will compute a linear interpolation to fill
                    # missing data
                    frame_dif = frame_num - counter + 1
                    # compute linear incremental movement per frame in x
                    x_dif = ul_x - last_ul_x
                    x_inc = x_dif / frame_dif
                    # compute linear incremental movement per frame in y
                    y_dif = ul_y - last_ul_y
                    y_inc = y_dif / frame_dif
                    # print("x_inc: ", x_inc, "y_inc: ", y_inc)
                    print("Gap size: ", frame_dif)


                    while counter < frame_num:
                        last_ul_x += x_inc
                        last_ul_y += y_inc
                        writer.writerow([counter, round(last_ul_x), round(last_ul_y), f_width, f_height, EST])
                        counter += 1
            if frame_num == counter:
                writer.writerow([counter, ul_x, ul_y, f_width, f_height, ACT])
                last_ul_x = ul_x
                last_ul_y = ul_y

            else:
                print("ERROR: shouldn't get here, counter cannot be higher than frame number")

print('Filled data saved as ', out_filename)
