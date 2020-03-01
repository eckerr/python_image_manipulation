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
from enum import Enum
import numpy as np
from trackers import set_up_tracker
from position_bbox import adjust_bbox
from scipy.signal import savgol_filter

global ul_x, ul_y

# tracking status constants
MISS = 0
GOOD = 1
ADJ = 2  # manual adjustment made on this frame

in_video_filename = 'MVI_9450_small.mp4'
range_start = 0
range_end = 500
find_start = (range_start + range_end)//2  # suggested starting point
# find_start = 8364  # (range_start + range_end)//2  # suggested starting point
track_type = 2  # 0-7
adjustment_requested_count = 0
forward_error_count = 0
backward_error_count = 0
total_error_count = 0
use_existing_keys = True
use_existing_tracking_array = False
bbox = None

# in_keys_filename = in_video_filename[:-10] + '_clean.csv'
in_keys_filename = in_video_filename[:-4] + '_p.csv'
out_filename = in_video_filename[:-4] + '_tracked-' +\
               str(range_start) + '-' + str(range_end) + '-' +\
               str(track_type) + '.csv'

counter = 0
started_at = None
ul_x = 180
ul_y = 75
x_offset = 0
y_offset = 0

default_x_offset = 35
default_y_offset = 20
default_track_width = 120
default_track_height = 120
track_width = default_track_width
track_height = default_track_height
frame_width = None
frame_height = None

last_valid_bbox = None
adjustment_requested = False

def create_new_array(last_frame):
    # create an array to store results, large enough to cover last frame wanted
    return np.zeros((range_end+1, 6), dtype=np.int32)


def force_bbox_in_frame_bounds(tracked_box):
    # print('tracked_box: ', tracked_box)
    # need to trim face_window_array to stay within frame window
    max_width = frame_width - tracked_box[2] - 1
    max_height = frame_height - tracked_box[3] - 1
    # print('max width/height:', max_width, max_height)

    if tracked_box[0] < 0:
        x = 0
    elif tracked_box[0] > max_width:
        x = max_width
    else:
        x = tracked_box[0]

    if tracked_box[1] < 0:
        y = 0
    elif tracked_box[1] > max_height:
        y = max_height
    else:
        y = tracked_box[1]
    return int(x), int(y), tracked_box[2], tracked_box[3]


def load_variables(d_row):
    # reads a csv record into variable names
    f_num = int(d_row[0])
    bbox_array = (int(d_row[1]), int(d_row[2]), int(d_row[3]), int(d_row[4]))
    # ul_x = int(row[1])
    # ul_y = int(row[2])
    # f_width = int(row[3])
    # f_height = int(row[4])

    # return frame_num, ul_x, ul_y, f_width, f_height
    return f_num, bbox_array


def paint_box():
    """ paints the found bounding box on the image frame """
    global k, counter, bbox
    # Tracking success - draw rectangle
    p1 = (int(bbox[0]), int(bbox[1]))
    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
    cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
    # display offsets
    offsets_text = str(frame_num) + '  ' + str(int(bbox[0])) + '  ' + str(int(bbox[1])) + '  ' + str(int(bbox[2])) +\
        '  ' + str(int(bbox[3])) + '  ' + str(track_type)
    cv2.putText(frame, offsets_text, (200, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 50, 50), 2)


def display_result():
    """ draws frame to the display """
    global k
    # Display result
    cv2.imshow("Tracking", frame)
    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    return k


def update_face_window_record(array_index, track_status):
    """ record bounding box info and frame number to array """
    # update appropriate face window record
    f_num = int(video.get(cv2.CAP_PROP_POS_FRAMES) - 1)
    # print('current frame number in track_frame: ', f_num)
    # if ok:
    #     face_window_array[array_index] = [f_num, int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]), 1]
    # else:
    #     face_window_array[array_index] = [f_num, int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]), 0]
    face_window_array[array_index] = [f_num, int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]), track_status]
    # print("Counter: ", counter, 'record: ', face_window_array[counter])


def determine_bbox(last_valid=None):
    global ul_x, ul_y, x_offset, y_offset, track_width, track_height
    if last_valid:
        ul_x = int(last_valid[0])
        ul_y = int(last_valid[1])
        x_offset = 0
        y_offset = 0
        track_width = int(last_valid[2])
        track_height = int(last_valid[3])
    else:
        print("no last_valid_bbox")

    # manually adjust the bounding box
    returned_values_list = adjust_bbox(frame, ul_x, x_offset, ul_y, y_offset, track_width, track_height)
    ul_x = returned_values_list[0]
    ul_y = returned_values_list[1]
    x_offset = returned_values_list[2]
    y_offset = returned_values_list[3]
    track_width = returned_values_list[4]
    track_height = returned_values_list[5]
    return ul_x - x_offset, ul_y - y_offset, track_width, track_height


def process_keypress():
    global adjustment_requested
    if k == 27:
        sys.exit()
    elif k == 114:
        print('readjust bbox selected')
        adjustment_requested = True
    elif k != 255:
        print('k = ', k)


def adjust_and_reset_tracker():
    global bbox, tracker, ok
    # print('last_valid_bbox', last_valid_bbox)
    bbox = determine_bbox(last_valid=last_valid_bbox)
    # re-initialize tracker after tracking adjustment
    tracker = set_up_tracker(track_type)
    return tracker.init(frame, bbox), status


if __name__ == '__main__':
    print('starting program')
    # open the files for processing

    if not use_existing_tracking_array:
        face_window_array = create_new_array(range_end)
        print('length of new face_window_array: ', len(face_window_array))

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

    # open the csv file of previously found face locations
    if use_existing_keys:
        with open(in_keys_filename, 'r') as in_file:
            reader = csv.reader(in_file)

            # pull the first face object location record
            row = reader.__next__()
            # decode record
            # frame_num, ul_x, ul_y, f_width, f_height = load_variables(row)
            frame_num, bbox = load_variables(row)

            while frame_num < find_start:
                row = reader.__next__()
                # frame_num, ul_x, ul_y, f_width, f_height = load_variables(row)
                frame_num, bbox = load_variables(row)
            # found the first located face within range
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
        print('track_height:', track_height)

    # point to video frame record
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    # get the associated frame from the video file
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')

    # get the starting bbox location
    bbox = determine_bbox(last_valid=None)

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
            print('Unable to read video frame at start of forward tracking')
            break
        counter += 1

        # check if adjustment needed
        if adjustment_requested:
            ok = adjust_and_reset_tracker()
            adjustment_requested_count += 1
            print('Frame: ', counter, 'adjustments requested: ', adjustment_requested_count)
            adjustment_requested = False
            status = ADJ
        else:
            # Update tracker
            ok, bbox = tracker.update(frame)
            # Draw bounding box
            if ok:
                print('bbox to pass:', bbox)
                bbox = force_bbox_in_frame_bounds(bbox)
                print('forced bbox: ', bbox)
                paint_box()
                last_valid_bbox = bbox
                status = GOOD
            else:
                ok = adjust_and_reset_tracker()
                if ok:
                    status = MISS
                    forward_error_count += 1
                    print('Frame: ', counter, 'forward tracking miss: ', forward_error_count)
                else:
                    print('ERROR: should not get here after manual correction of tracking')
        # print('counter: ', counter, 'status: ', status)
        update_face_window_record(counter, status)
        display_result()
        process_keypress()

    # ==========================================
    # work backward through preceding frames
    # ==========================================

    # get the record to start from
    if started_at > 0:
        print("Starting to track backward")
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
        print('ok: ', ok)
        if not ok:
            print('tracker failed to init for backtracking')

        counter = started_at - 1
        while counter >= range_start:
            video.set(cv2.CAP_PROP_POS_FRAMES, counter)
            # print('current frame: ', video.get(cv2.CAP_PROP_POS_FRAMES))
            ok, frame = video.read()
            if not ok:
                print('record was not found!')

            # check if adjustment needed
            if adjustment_requested:
                adjust_and_reset_tracker()
                adjustment_requested_count += 1
                print('Frame: ', counter, 'adjustments requested: ', adjustment_requested_count)
                adjustment_requested = False
                status = ADJ
            else:
                # Update tracker
                ok, bbox = tracker.update(frame)
                # Draw bounding box
                if ok:
                    bbox = force_bbox_in_frame_bounds(bbox)
                    paint_box()
                    last_valid_bbox = bbox
                    status = GOOD
                else:
                    adjust_and_reset_tracker()
                    if ok:
                        status = MISS
                        backward_error_count += 1
                        print('Frame: ', counter, 'back tracking miss: ', backward_error_count)

            # print('counter: ', counter, 'status: ', status)
            update_face_window_record(counter, status)
            display_result()
            process_keypress()
            counter = counter - 1

    video.release()
    print('Video released')
    """
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
    """

    # ===============================================================================
    # Save results
    # ===============================================================================


    np.savetxt(out_filename, face_window_array[range_start:range_end+1], delimiter=',')
    print('tracked data filtered and saved as ', out_filename)

    total_error_count = forward_error_count + backward_error_count

    print('Forward Error Count: ', forward_error_count)
    print('Backward Error Count: ', backward_error_count)
    print('Total Error Count: ', total_error_count)
    print('Adjustments made: ', adjustment_requested_count)


    cv2.destroyAllWindows()






