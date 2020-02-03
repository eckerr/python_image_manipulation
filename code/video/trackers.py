"""
examples of trackers in OpenCV

  Created by Ed on 1/31/2020
 """

import cv2
import sys

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')


def print_video_properties():
    print('CAP_PROP_MSEC', video.get(cv2.CAP_PROP_POS_MSEC))
    print('CAP_PROP_FRAMES', video.get(cv2.CAP_PROP_POS_FRAMES))
    print('CAP_PROP_POS_AVI_RATIO', video.get(cv2.CAP_PROP_POS_AVI_RATIO))
    print('CAP_PROP_FRAME_WIDTH', video.get(cv2.CAP_PROP_FRAME_WIDTH))
    print('AP_PROP_FRAME_HEIGHT', video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print('CAP_PROP_FPS', video.get(cv2.CAP_PROP_FPS))
    print('CAP_PROP_FOURCC', video.get(cv2.CAP_PROP_FOURCC))
    print('CAP_PROP_FRAME_COUNT', video.get(cv2.CAP_PROP_FRAME_COUNT))
    print('CAP_PROP_FORMAT', video.get(cv2.CAP_PROP_FORMAT))
    print('CAP_PROP_MODE', video.get(cv2.CAP_PROP_MODE))
    print('CAP_PROP_BRIGHTNESS', video.get(cv2.CAP_PROP_BRIGHTNESS))
    print('CAP_PROP_CONTRAST', video.get(cv2.CAP_PROP_CONTRAST))
    print('CAP_PROP_SATURATION', video.get(cv2.CAP_PROP_SATURATION))
    print('CAP_PROP_HUE', video.get(cv2.CAP_PROP_HUE))
    print('CAP_PROP_GAIN', video.get(cv2.CAP_PROP_GAIN))
    print('CAP_PROP_EXPOSURE', video.get(cv2.CAP_PROP_EXPOSURE))
    print('CAP_PROP_CONVERT_RGB', video.get(cv2.CAP_PROP_CONVERT_RGB))
    print('CAP_PROP_WHITE_BALANCE_BLUE_U', video.get(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U))
    print('CAP_PROP_RECTIFICATION', video.get(cv2.CAP_PROP_RECTIFICATION))
    print('CAP_PROP_MONOCHROME', video.get(cv2.CAP_PROP_MONOCHROME))
    print('CAP_PROP_SHARPNESS', video.get(cv2.CAP_PROP_SHARPNESS))
    print('CAP_PROP_AUTO_EXPOSURE', video.get(cv2.CAP_PROP_AUTO_EXPOSURE))
    print('CAP_PROP_GAMMA', video.get(cv2.CAP_PROP_GAMMA))
    print('CAP_PROP_TEMPERATURE', video.get(cv2.CAP_PROP_TEMPERATURE))
    print('CAP_PROP_TRIGGER', video.get(cv2.CAP_PROP_TRIGGER))
    print('CAP_PROP_TRIGGER_DELAY', video.get(cv2.CAP_PROP_TRIGGER_DELAY))
    print('CAP_PROP_WHITE_BALANCE_RED_V', video.get(cv2.CAP_PROP_WHITE_BALANCE_RED_V))
    print('CAP_PROP_ZOOM', video.get(cv2.CAP_PROP_ZOOM))
    print('CAP_PROP_FOCUS', video.get(cv2.CAP_PROP_FOCUS))
    print('CAP_PROP_GUID', video.get(cv2.CAP_PROP_GUID))
    print('CAP_PROP_ISO_SPEED', video.get(cv2.CAP_PROP_ISO_SPEED))
    print('CAP_PROP_BACKLIGHT', video.get(cv2.CAP_PROP_BACKLIGHT))
    print('CAP_PROP_PAN', video.get(cv2.CAP_PROP_PAN))
    print('CAP_PROP_TILT', video.get(cv2.CAP_PROP_TILT))
    print('CAP_PROP_ROLL', video.get(cv2.CAP_PROP_ROLL))
    print('CAP_PROP_IRIS', video.get(cv2.CAP_PROP_IRIS))
    print('CAP_PROP_SETTINGS', video.get(cv2.CAP_PROP_SETTINGS))
    print('CAP_PROP_BUFFERSIZE', video.get(cv2.CAP_PROP_BUFFERSIZE))
    print('CAP_PROP_AUTOFOCUS', video.get(cv2.CAP_PROP_AUTOFOCUS))
    print('CAP_PROP_SAR_NUM', video.get(cv2.CAP_PROP_SAR_NUM))
    print('CAP_PROP_SAR_DEN', video.get(cv2.CAP_PROP_SAR_DEN))
    print('CAP_PROP_BACKEND', video.get(cv2.CAP_PROP_BACKEND))
    print('CAP_PROP_CHANNEL', video.get(cv2.CAP_PROP_CHANNEL))
    print('CAP_PROP_AUTO_WB', video.get(cv2.CAP_PROP_AUTO_WB))
    print('CAP_PROP_WB_TEMPERATURE', video.get(cv2.CAP_PROP_WB_TEMPERATURE))
    # print('CAP_PROP_CODEC_PIXEL_FORMAT', video.get(cv2.CAP_PROP_CODEC_PIXEL_FORMAT))

def print_writer_properties():
    print('VIDEOWRITER_PROP_QUALITY', video.get(cv2.VIDEOWRITER_PROP_QUALITY))
    print('VIDEOWRITER_PROP_FRAMEBYTES', video.get(cv2.VIDEOWRITER_PROP_FRAMEBYTES))
    print('VIDEOWRITER_PROP_NSTRIPES', video.get(cv2.VIDEOWRITER_PROP_NSTRIPES))


def set_up_tracker(tracker_type_num):
    global tracker_type, tracker
    # Set up tracker.
    # Instead of MIL, you can also use
    tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[tracker_type_num]  # using KCF
    if int(major_ver) < 4:
        tracker = cv2.Tracker.create(tracker_type)
    else:
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
        return tracker


if __name__ == '__main__':
    print('major version: ', major_ver)
    print('minor version: ', minor_ver)
    print('subminor version: ', subminor_ver)

    tracker = set_up_tracker(2)

    # Read video
    video = cv2.VideoCapture('MVI_9468_small.mp4')
    # video = cv2.VideoCapture('..\\code\\video\\MVI_9464_small.mp4')

    # Exit if video not opened.
    if not video.isOpened():
        print('Could not open video')
        sys.exit()



    # Read first frame
    video.set(cv2.CAP_PROP_POS_FRAMES, 25)
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')

    print_video_properties()

    # Define an initial bounding box
    bbox = (204, 55, 125, 125)

    # select a different bounding box
    bbox = cv2.selectROI(frame, False)
    print('bounding box: ', bbox)

    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)

    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break

        # Start timer
        timer = cv2.getTickCount()

        # Update tracker
        ok, bbox = tracker.update(frame)

        # Calculate Frames per second(FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        else:
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255),2)

        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255),2);

        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255),2);

        # Display result
        cv2.imshow("Tracking", frame)

        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break


