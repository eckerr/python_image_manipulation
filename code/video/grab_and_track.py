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
        print('frame number to start tracking from: ', frame_num)
        # draw the found face bounding box
        # cv2.rectangle(frame, (ul_x, ul_y), (ul_x + f_width, ul_y + f_height), (255, 0, 0), 2, 1)
        # draw the face window bounding box
        cv2.rectangle(frame, (ul_x-x_offset, ul_y-y_offset),
                     (ul_x-x_offset+track_width, ul_y-y_offset+track_height), (0, 0, 255), 2, 1)
        # save the window bounding box as the track area
        bbox = (ul_x-x_offset, ul_y-y_offset, track_width, track_height)

        # display the frame for review
        # Display result
        cv2.imshow("info", frame)

        # Exit if ESC pressed
        k = cv2.waitKey() & 0xff
        if k == 27:
            cv2.destroyAllWindows()
            sys.exit()

    # ===============================================================================
    # Perform the tracking
    print('Onto the tracking phase')

    # set up tracker
    tracker = set_up_tracker(2)
    # ready to start tracking

    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)

    # Store the initial object location values
    started_at = frame_num
    print('starting at: ', started_at)
    face_window_array[started_at] = \
            [int(frame_num), int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])]
    print('starting record: ', frame_num, face_window_array[frame_num-range_start])

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
            k = track_frame()
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
        # re-initialize tracker for going backward
        ok = tracker.init(frame, bbox)

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
                k = track_frame()
                if k == 27:
                    # break
                    print('k: ', k)
            else:
                print('something wrong here bbox not ok')
            counter -= 1
            # else:
            #     break





    video.release()
    print('Video released')

    np.savetxt(out_filename, face_window_array[range_start:range_end], delimiter=',')
    print('tracked data saved as ', out_filename)

    cv2.destroyAllWindows()






