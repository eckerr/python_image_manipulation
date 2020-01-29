"""
 video_proc_resize class for resizing video files

  Created by Ed on 1/28/2020
 """

import cv2
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QMainWindow
from ui_main_window import Ui_MainWindow
from video_manager import VideoManager


from PyQt5.QtCore import (QObject,
                          QThread,
                          pyqtSignal,
                          pyqtSlot)
from PyQt5.QtGui import QPixmap, QImage

import time
import csv
import numpy as np
import cv2

class VideoProc(QObject):
    # signals
    in_display = pyqtSignal(QPixmap)
    out_display = pyqtSignal(QPixmap)

    def __init__(self, capture,
                 in_file_name,
                 preview_window_manager=None,
                 should_mirror_preview=False):
        super(VideoProc, self).__init__()

        # initialize variables
        self.vm = VideoManager(capture, in_file_name)

        self.in_file_name = in_file_name
        self.preview_window_manager = preview_window_manager


        self._out_filename = None
        self._capture = capture
        self.channel = 0

        self.stopped = True

        self.build_out_filename()
        self._in_frame = None
        self._out_frame = None

        self.out_width = 480
        self.out_height = 270

        # for numbering frames
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.bottom_left_text = 10, self.out_height - 10
        self.font_scale = 1
        self.font_color = (255, 128, 128)
        self.thickness = 2



        self.counter = 0


    def build_out_filename(self):
        self._out_filename = self.in_file_name[:-4] + "_small.mp4"
        print('built out_file_name:', self._out_filename)

    def process_image(self):
        # resize the image
        self._in_frame = np.ones((1920, 1080, 3))
        print('entered:', self.vm._entered_frame, 'in_frame: ', type(self.vm._in_frame))
        # self._in_frame = self.vm._in_frame
        print('type frame: ', self.vm.frame)
        print('type:', type(self._in_frame))
        print(self._in_frame.shape)
        print(self.out_width, self.out_height)

        self._out_frame = np.zeros((self.out_width, self.out_height, 3))
        self._out_frame = cv2.resize(src=self._in_frame,
                                     dsize=(self.out_width, self.out_height),
                                     dst=self._out_frame,
                                     fx=0,
                                     fy=0,
                                     interpolation=cv2.INTER_AREA)
        # number the frames
        cv2.putText(img=self._out_frame,
                    text=str(self.counter),
                    org=self.bottom_left_text,
                    fontFace=self.font,
                    fontScale=self.font_scale,
                    color=self.font_color,
                    thickness=self.thickness)
        self.counter += 1

    @pyqtSlot()
    def start_video(self):
        print("Thread started")
        self.stopped = False
        # start writing output video
        self.vm.start_writing_video(self._out_filename)
        print('name sent to video manager:',self._out_filename, 'end_of_line')
        print('video filename:', self.vm._video_filename)
        # begin main loop
        while self._capture.isOpened() and not self.stopped:
            print('VM open: ',self.vm._capture.isOpened())
            print('local is open: ', self._capture.isOpened())
            retrieved = self.vm.enter_frame()
            if retrieved:
                print("entered frame", 'elapsed: ', self.vm._frames_elapsed, 'NR:', self.vm._frame_not_ready_count)
                self.process_image()
            self.vm.exit_frame()
            print('exited frame', self.vm._frames_elapsed)
            self.counter += 1

    @pyqtSlot()
    def stop_video(self):
        print("stopping in progress")
        self.stopped = True
        self.vm.stop_video()
