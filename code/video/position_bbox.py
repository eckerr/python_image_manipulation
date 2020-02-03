"""
position_bbox.py

Looks at list of found faces within a range, then locates first found face
and displays bounding box. Loops to allow repositioning of bbox.

  Created by Ed on 2/1/2020
 """

import cv2
import sys
import csv
import time
import numpy as np
from trackers import set_up_tracker

in_video_filename = 'MVI_9468_small.mp4'
range_start = 0
range_end = 300
in_keys_filename = in_video_filename[:-4] + '_p.csv'
out_filename = in_video_filename[:-4] + '_tracked-' + str(range_start) + '-' + str(range_end) + '-.csv'

counter = 0
started_at = None
x_offset = 35
y_offset = 20
track_width = 120
track_height = 120

# create an array to store results, large enough to cover last frame wanted
face_window_array = np.zeros((range_end, 5), dtype=np.int32)
print('length of face_window_array: ', len(face_window_array))
# print(face_window_array)


def load_variables(row):
    # reads a csv record into variable names
    frame_num = int(row[0])
    ul_x = int(row[1])
    ul_y = int(row[2])
    f_width = int(row[3])
    f_height = int(row[4])

    return frame_num, ul_x, ul_y, f_width, f_height


def track_frame():
    global k, counter
    # Tracking success
    p1 = (int(bbox[0]), int(bbox[1]))
    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
    cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
    # update appropriate face window record
    fnum = int(video.get(cv2.CAP_PROP_POS_FRAMES) - 1)
    # print('current frame number in track_frame: ', fnum)
    face_window_array[counter] = [fnum, int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])]
    # print("Counter: ", counter, 'record: ', face_window_array[counter])
    # Display result
    cv2.imshow("Tracking", frame)
    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    return k


if __name__ == '__main__':
    # open the files for processing
    # Open the video file
    video = cv2.VideoCapture(in_video_filename)

    # if no video, exit
    if not video.isOpened():
        print('Video file could not be opened.')
        sys.exit()

    # open the cvs files
    with open(in_keys_filename, 'r') as in_file:
        reader = csv.reader(in_file)
        # with open(out_filename, 'w', newline='') as out_file:
        #     writer = csv.writer(out_file)

        # pull the first face object location record
        row = reader.__next__()
        # counter += 1
        # decode record
        frame_num, ul_x, ul_y, f_width, f_height = load_variables(row)
        # if frame_num >= range_start:
        #     # found the first located face within the range
        #     print("location first found: ", frame_num, range_start)
        while frame_num < range_start:
            row = reader.__next__()
            frame_num, ul_x, ul_y, f_width, f_height = load_variables(row)
        # found the first located face within the range
        print("location first found: ", frame_num, 'range start: ', range_start)

    # point to video frame record
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    # get the associated frame from the video file
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
    else:
        # loop while we make positioning adjustments
        position = True
        while True:
            display_frame = frame.copy()
            # draw the found face bounding box
            cv2.rectangle(display_frame, (ul_x-x_offset, ul_y-y_offset),
                         (ul_x-x_offset+track_width, ul_y-y_offset+track_height), (0, 0, 255), 2, 1)
            if position:
                pos_text = 'Position'
            else:
                pos_text = 'Width'
            # Display tracker type on frame
            cv2.putText(display_frame, pos_text, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            # display the frame for review
            # Display result
            cv2.imshow("adjust position", display_frame)

            # Exit if ESC pressed
            k = cv2.waitKey() & 0xff
            if k == 27:
                cv2.destroyAllWindows()
                print('final values: ', x_offset, y_offset, track_width, track_height)
                break
            elif k == 97:
                print('left arrow')
                if position:
                    x_offset += 10
                else:
                    track_width += 10
            elif k == 100:
                print('right arrow')
                if position:
                    x_offset -= 10
                else:
                    track_width -= 10
            elif k == 119:
                print('up arrow')
                if position:
                    y_offset += 10
                else:
                    track_height += 10
            elif k == 120:
                print('down arrow')
                if position:
                    y_offset -= 10
                else:
                    y_offset += 10
            elif k == 115:
                print('toggle position / width')
                position = False

            elif k == 65:
                print('left arrow')
                if position:
                    x_offset += 1
                else:
                    track_width += 1
            elif k == 68:
                print('right arrow')
                if position:
                    x_offset -= 1
                else:
                    track_width -= 1
            elif k == 87:
                print('up arrow')
                if position:
                    y_offset += 1
                else:
                    track_height += 1
            elif k == 88:
                print('down arrow')
                if position:
                    y_offset -= 1
                else:
                    y_offset += 1



    # ===============================================================================
    #     # save the window bounding box as the track area
    #     bbox = (ul_x-x_offset, ul_y-y_offset, track_width, track_height)






    # video.release()
    # print('Video released')
    #
    # np.savetxt(out_filename, face_window_array[range_start:range_end], delimiter=',')
    # print('tracked data saved as ', out_filename)
    #
    # cv2.destroyAllWindows()
    #





