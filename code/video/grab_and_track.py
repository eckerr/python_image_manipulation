"""
grab_and_track.py

Looks at list of found faces within a range, then tracks forward (and backward)
from the identified face and saving the tracked locations to file.

  Created by Ed on 2/1/2020
 """

import cv2
import sys
import csv
import time
import numpy as np
from trackers import set_up_tracker
from position_bbox import adjust_bbox
from scipy.signal import savgol_filter

in_video_filename = 'MVI_9429_small.mp4'
range_start = 21718
range_end = 21722
find_start = (range_start + range_end)//2  # suggested starting point
# find_start = 8364  # (range_start + range_end)//2  # suggested starting point
track_type = 2  # 0-7
forward_error_count = 0
backward_error_count = 0
total_error_count = 0
use_existing_keys = False

# in_keys_filename = in_video_filename[:-10] + '_clean.csv'
in_keys_filename = in_video_filename[:-4] + '_p.csv'
out_filename = in_video_filename[:-4] + '_tracked-' +\
               str(range_start) + '-' + str(range_end) + '-' +\
               str(track_type) + '.csv'

counter = 0
started_at = None
ul_x = 0
ul_y = 0
x_offset = 35  # default value before adjustment
y_offset = 20  # default value before adjustment
track_width = 120  # default value before adjustment
track_height = 120  # default value before adjustment
frame_width = None
frame_height = None

# create an array to store results, large enough to cover last frame wanted
face_window_array = np.zeros((range_end+1, 6), dtype=np.int32)
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


def paint_box():
    global k, counter
    # Tracking success - draw rectangle
    p1 = (int(bbox[0]), int(bbox[1]))
    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
    cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
    # display offsets
    offsets_text = str(frame_num) + '  ' + str(int(bbox[0])) + '  ' + str(int(bbox[1])) + '  ' + str(int(bbox[2])) +\
        '  ' + str(int(bbox[3])) + '  ' + str(track_type)
    cv2.putText(frame, offsets_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)


def display_result():
    global k
    # Display result
    cv2.imshow("Tracking", frame)
    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    return k


def update_face_window_record(array_index):
    # update appropriate face window record
    f_num = int(video.get(cv2.CAP_PROP_POS_FRAMES) - 1)
    # print('current frame number in track_frame: ', f_num)
    if ok:
        face_window_array[array_index] = [f_num, int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]), 1]
    else:
        face_window_array[array_index] = [f_num, int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]), 0]
    # print("Counter: ", counter, 'record: ', face_window_array[counter])


if __name__ == '__main__':
    # open the files for processing
    # Open the video file
    video = cv2.VideoCapture(in_video_filename)

    # if no video, exit
    if not video.isOpened():
        print('Video file could not be opened.')
        sys.exit()
    # Get input video frame size
    frame_width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print('frame width: ', frame_width, 'frame height: ', frame_height)


    # open the cvs files if use_existing_keys is True
    if use_existing_keys:
        with open(in_keys_filename, 'r') as in_file:
            reader = csv.reader(in_file)

            # with open(out_filename, 'w', newline='') as out_file:
            #     writer = csv.writer(out_file)

            # pull the first face object location record
            row = reader.__next__()
            # decode record
            frame_num, ul_x, ul_y, f_width, f_height = load_variables(row)
            while frame_num < find_start:
                row = reader.__next__()
                frame_num, ul_x, ul_y, f_width, f_height = load_variables(row)
            # found the first located face within the range
            print("location first found: ", frame_num, 'range start: ', range_start)
    else:
        # start directly from the starting point, not nearest-key
        frame_num = find_start
        ul_x = int(frame_width // 2)
        ul_y = int(frame_width // 2)
        f_width = 140
        f_height = 140
        track_width = 140
        track_height = 140
        print('frame_num:', frame_num)
        print('ul_x:', ul_x)
        print('ul_y:', ul_y)
        print('f_width:', f_width)
        print('f_height:', f_height)
        print('track_width:', track_width)
        print('track_hieght:', track_height)

    # point to video frame record
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    # get the associated frame from the video file
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
    else:
        returned_values_list = adjust_bbox(frame, ul_x, x_offset, ul_y, y_offset, track_width, track_height)
        ul_x = returned_values_list[0]
        ul_y = returned_values_list[1]
        x_offset = returned_values_list[2]
        y_offset = returned_values_list[3]
        track_width = returned_values_list[4]
        track_height = returned_values_list[5]

        # print('frame number to start tracking from: ', frame_num)
        # # draw the found face bounding box
        # # cv2.rectangle(frame, (ul_x, ul_y), (ul_x + f_width, ul_y + f_height), (255, 0, 0), 2, 1)
        # # draw the face window bounding box
        # cv2.rectangle(frame, (ul_x-x_offset, ul_y-y_offset),
        #              (ul_x-x_offset+track_width, ul_y-y_offset+track_height), (0, 0, 255), 2, 1)
        # save the window bounding box as the track area
        bbox = (ul_x-x_offset, ul_y-y_offset, track_width, track_height)

        print('bounding box we decided on: ', bbox)
    # ===============================================================================
    # Perform the tracking
    # ===============================================================================

    print('Onto the tracking phase')

    # set up tracker
    tracker = set_up_tracker(track_type)
    # ready to start tracking

    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)
    if not ok:
        print('Tracker did not initialize')

    # Store the initial object location values
    started_at = frame_num
    print('starting at: ', started_at)
    face_window_array[started_at] = \
        [int(frame_num), int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]), 1]
    print('starting record: ', frame_num, face_window_array[frame_num])

    # Loop through all following frames
    counter = started_at
    while counter < len(face_window_array)-1:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
        counter += 1

        # Update tracker
        ok, bbox = tracker.update(frame)
        # Draw bounding box
        if ok:
            paint_box()
        else:
            forward_error_count += 1
            print('Frame: ', counter, 'tracking miss: ', forward_error_count)

        update_face_window_record(counter)
        display_result()
        if k == 27:
            sys.exit()

    # ==========================================
    # work backward through preceding frames
    # ==========================================
    # get the record to start from
    if started_at > 0:
        start_rec = face_window_array[started_at]
        print('starting record for tracking backward: ', start_rec)
        # get the frame we need to initialize tacker
        # point to video frame record
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        # get the associated frame from the video file
        ok, frame = video.read()
        if not ok:
            print('Cannot read video file for backtracking')
        # set up bounding box
        bbox = (start_rec[1], start_rec[2], start_rec[3], start_rec[4])
        print('bbox: ', bbox)

        # set up tracker
        tracker = set_up_tracker(track_type)

        # re-initialize tracker for going backward
        ok = tracker.init(frame, bbox)
        if not ok:
            print('tracker failed to init for backtracking')

        counter = started_at - 1
        while counter >= range_start:
            video.set(cv2.CAP_PROP_POS_FRAMES, counter)
            # print('current frame: ', video.get(cv2.CAP_PROP_POS_FRAMES))
            ok, frame = video.read()
            if not ok:
                print('record was not found!')
            # Update tracker
            ok, bbox = tracker.update(frame)
            # Draw bounding box
            if ok:
                paint_box()
            else:
                backward_error_count += 1
                print('Frame: ', counter, 'tracking miss: ', backward_error_count)

            update_face_window_record(counter)
            display_result()
            if k == 27:
                sys.exit()
            counter -= 1
            # else:
            #     break

    video.release()
    print('Video released')

    # ------------------------------------------------------
    #  Done tracking, filter results and keep within frame
    # ------------------------------------------------------
    # filter the face data with a moving average window of 5
    x_vals = savgol_filter(face_window_array[:, 1], 5, 3)
    y_vals = savgol_filter(face_window_array[:, 2], 5, 3)

    for i in range(len(face_window_array)):
        face_window_array[i][1] = round(x_vals[i])
        face_window_array[i][2] = round(y_vals[i])

    # filter the face data again with a moving average window of 11
    x_vals = savgol_filter(face_window_array[:, 1], 11, 3)
    y_vals = savgol_filter(face_window_array[:, 2], 11, 3)

    for i in range(len(face_window_array)):
        face_window_array[i][1] = round(x_vals[i])
        face_window_array[i][2] = round(y_vals[i])

    # need to trim face_window_array to stay within frame window
    max_width = frame_width - face_window_array[range_start][3] - 1
    max_height = frame_height - face_window_array[range_start][4] - 1
    print('frame width: ', frame_width, 'frame height: ', frame_height)
    print('face 0 3: ', face_window_array[range_start][3])
    print('face 0 4: ', face_window_array[range_start][4])
    print('max_width: ', max_width, 'max_height:', max_height)
    for i in range(len(face_window_array)):
        if face_window_array[i][1] < 0:
            face_window_array[i][1] = 0
        elif face_window_array[i][1] > max_width:
            face_window_array[i][1] = max_width

        if face_window_array[i][2] < 0:
            face_window_array[i][2] = 0
        elif face_window_array[i][2] > max_height:
            face_window_array[i][2] = max_height


    # ===============================================================================
    # Save results
    # ===============================================================================


    np.savetxt(out_filename, face_window_array[range_start:range_end+1], delimiter=',')
    print('tracked data filtered and saved as ', out_filename)

    total_error_count = forward_error_count + backward_error_count

    print('Forward Error Count: ', forward_error_count)
    print('Backward Error Count: ', backward_error_count)
    print('Total Error Count: ', total_error_count)


    cv2.destroyAllWindows()






