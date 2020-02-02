"""
track_missing_faces.py
  fills blanks in front_faces.csv file
  by tracking between known positions

  Created by Ed on 1/10/2020
 """

import sys
import csv
import cv2

counter = 0
last_ul_x = 0
last_ul_y = 0
ACT = 0
EST = 1

in_filename = 'MVI_9464_clean.csv'
video_filename = in_filename[:-9] + 'small.mp4'
out_filename = in_filename[:-9] + 'tracked.csv'

# prepare the Tracker
# Set up tracker.
# Instead of MIL, you can also use

tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
tracker_type = tracker_types[2]

if tracker_type == 'BOOSTING':
    tracker = cv2.TrackerBoosting.create()
if tracker_type == 'MIL':
    tracker = cv2.TrackerMIL.create()
if tracker_type == 'KCF':
    tracker = cv2.TrackerKCF.create()
if tracker_type == 'TLD':
    tracker = cv2.TrackerTLD.create()
if tracker_type == 'MEDIANFLOW':
    tracker = cv2.TrackerMedianFlow.create()
if tracker_type == 'GOTURN':
    tracker = cv2.TrackerGOTURN.create()
if tracker_type == 'MOSSE':
    tracker = cv2.TrackerMOSSE.create()
if tracker_type == 'CSRT':
    tracker = cv2.TrackerCSRT.create()

# open the files for processing

# Open the video file
video = cv2.VideoCapture(video_filename)

# if no video, exit
if not video.isOpened():
    print('Video file could not be opened.')
    sys.exit()


def load_variables(row):

    frame_num = int(row[0])
    ul_x = int(row[1])
    ul_y = int(row[2])
    f_width = int(row[3])
    f_height = int(row[4])
    return frame_num, ul_x, ul_y, f_width, f_height


# open the cvs files
with open(in_filename, 'r') as in_file:
    reader = csv.reader(in_file)
    with open(out_filename, 'w', newline='') as out_file:
        writer = csv.writer(out_file)

        for row in reader:
            counter += 1
            frame_num, ul_x, ul_y, f_width, f_height = load_variables(row)

            if frame_num > counter:
                # need to track missing frames
                if counter == 1: # ToDo need to come back to this
                    # special case, don't know what initial values
                    # should be, will assume stationary
                    while counter < frame_num:
                        writer.writerow([counter, int(ul_x), int(ul_y), f_width, f_height, EST])
                        counter += 1
                else:
                    # will track over the missing frames to fill any missing data
                    frame_dif = frame_num - counter + 1
                    print('Frames to track: ', frame_dif, counter+1, '-', frame_num)

                    # Retrieve starting frame to fill
                    video.set(cv2.CAP_PROP_POS_FRAMES, counter)
                    ok, frame = video.read()
                    if not ok:
                        print('Cannot read video file')

                    # draw a rectangle around (single) face found on this frame
                    cv2.rectangle(frame,
                                  (ul_x - 50, ul_y - 25),
                                  (ul_x + f_width + 50,
                                   ul_y + f_height + 50),
                                  (255, 0, 0), 2)

                    # select a token/different bounding box just to put an image on screen for testing
                    bbox = cv2.selectROI(frame, False)
                    print('bounding box: ', bbox)

                    # Set starting bounding box
                    bbox = (ul_x - 50, ul_y - 25, ul_x + f_width + 50, ul_y + f_height + 50)
                    # Retrieve the first frame to track

                    # Initialize tracker with first frame and bounding box
                    ok = tracker.init(frame, bbox)

                    while counter < frame_num:
                        # Read a new frame
                        ok, frame = video.read()
                        if not ok:
                            print('Failed to retrieve frame')
                            break
                        # Update tracker
                        ok, bbox = tracker.update(frame)
                        writer.writerow([counter, int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]), EST])
                        counter += 1

                        # Draw bounding box
                        if ok:
                            # Tracking success
                            p1 = (int(bbox[0]), int(bbox[1]))
                            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                            cv2.rectangle(frame, p1, p2, (0, 0, 255), 2, 1)
                        else:
                            # Tracking failure
                            cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                                        (0, 0, 255), 2)

                        # Display tracker type on frame
                        cv2.putText(frame, tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                                    (0, 0, 255), 2);

                        # Display result
                        cv2.imshow("Tracking", frame)

                        # Exit if ESC pressed
                        k = cv2.waitKey(1) & 0xff
                        if k == 27:
                            break

            if frame_num == counter:
                writer.writerow([counter, ul_x, ul_y, f_width, f_height, ACT])
                last_ul_x = ul_x
                last_ul_y = ul_y

            else:
                print("ERROR: shouldn't get here, counter cannot be higher than frame number")

print('Tracked data saved as ', out_filename)
