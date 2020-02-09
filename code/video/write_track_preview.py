"""
write_track_preview.py

reads the tracked file csv and writes the bounding box to a video file

  Created by Ed on 2/1/2020
 """

import cv2
import sys
import csv
import time
import numpy as np
from trackers import set_up_tracker
from position_bbox import adjust_bbox

in_video_filename = 'MVI_9466_small.mp4'
range_start = 17520
range_end = 22023
in_frame = None
out_frame = None
out_width = 480
out_height = 270


# in_track_filename = in_video_filename[:-4] + '_p.csv'

counter = 0
started_at = None
x_offset = 35
y_offset = 20
f_width = None
f_height = None
video_out = None
fps = 30
encoding = cv2.VideoWriter_fourcc('F', 'F', 'V', 'H')


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

    # load the tracked-data array.
    in_track_filename = in_video_filename[:-4] + '_tracked-' + str(range_start) + '-' + str(range_end) + '-2.csv'
    faces = np.loadtxt(in_track_filename, delimiter=',', dtype=np.int32)
    # read the first row from the array
    frame_num, ul_x, ul_y, f_width, f_height = load_variables(faces[0])

    range_start = frame_num
    range_end = faces[-1][0]

    out_video_filename = in_video_filename[:-4] + '_preview-' + str(range_start) + '-' + str(range_end) + '-.mp4'
    size = (out_width, out_height)
    video_out = cv2.VideoWriter(
                                out_video_filename, encoding,
                                fps, size, isColor=True)

    print("Video writer is open: ", video_out.isOpened(), "\tsize: ", size)
    # get first file frame
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    for i in range(len(faces)):
        ok, frame = video.read()
        if ok:
            frame_num, ul_x, ul_y, f_width, f_height = load_variables(faces[i])
            cv2.rectangle(frame,
                          (ul_x, ul_y),
                          (ul_x+f_width,
                           ul_y+f_height),
                          (255, 0, 0), 2, 1)
        else:
            print('this should not have happened, no frame!')
        cv2.imshow("Tracking", frame)
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

        video_out.write(frame)

    cv2.destroyAllWindows()
    video_out.release()






