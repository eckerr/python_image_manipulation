"""
Routine to read list of face keys and show on screen with bounding box
  Created by Ed on 2/1/2020
 """

import cv2
import sys
import csv
import time
import numpy as np

in_video_filename = 'MVI_9468_small.mp4'
in_keys_filename = in_video_filename[:-4] + '_p.csv'


def load_variables(row):

    frame_num = int(row[0])
    ul_x = int(row[1])
    ul_y = int(row[2])
    f_width = int(row[3])
    f_height = int(row[4])
    return frame_num, ul_x, ul_y, f_width, f_height

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

        for row in reader:
            # counter += 1
            # decode record
            frame_num, ul_x, ul_y, f_width, f_height = load_variables(row)
            # point to video frame record
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            # get the associated frame from the video file
            ok, frame = video.read()
            if not ok:
                print('Cannot read video file')
            # draw the found face bounding box
            cv2.rectangle(frame, (ul_x, ul_y), (ul_x + f_width, ul_y + f_height), (255, 0, 0), 2, 1)
            # draw the face window bounding box
            cv2.rectangle(frame, (ul_x-25, ul_y-25), (ul_x + 75, ul_y + 75), (0, 0, 255), 2, 1)
            # display the frame for review
            # Display result
            cv2.imshow("Tracking", frame)

            # Exit if ESC pressed
            k = cv2.waitKey(1) & 0xff
            if k == 27:
                break



