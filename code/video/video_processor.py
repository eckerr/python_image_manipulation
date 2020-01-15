"""
 video_processor_thread class
  Created by Ed on 1/7/2020
 """
from PyQt5.QtCore import (QObject,
                          QThread,
                          pyqtSignal)
from PyQt5.QtGui import QPixmap

import cv2


class VideoProcessor(QObject):

    def __init__(self):
        super.__init__()
        self.camera = cv2.VideoCapture(0)
        self.in_frame = None
        self.stopped = False

        # signals
        in_display = pyqtSignal(QPixmap)
        out_display = pyqtSignal(QPixmap)

    def start_video(self):
        while self.camera.isOpened() and not self.stopped:
            self.in_frame =



        pass

    def stop_video(self):
        pass


    def run(self):
        camera_capture = cv2.VideoCapture(0)
        fps = 30
        size = (int(camera_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(camera_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        video_writer = cv2.VideoWriter(
            'MyOutputVid.avi', cv2.VideoWriter_fourcc('I', '4', '2', '0'),
                                                      fps, size)

        while (camera_capture.isOpened() and not isInteruptionRequested()):
            success, frame = camera_capture.read()
        num_frames_remaining = 10 * fps -1
        while success and num_frames_remaining > 0:
            video_writer.write(frame)
            success, frame = camera_capture.read()
            num_frames_remaining -= 1
        camera_capture.release()

        )




