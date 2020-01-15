"""
 video_proc_shift class

 opens a video file, loads a list of found face centers,
 then shifts the image to place the face at the center

  Created by Ed on 1/7/2020
 """
from PyQt5.QtCore import (QObject,
                          QThread,
                          pyqtSignal,
                          pyqtSlot)
from PyQt5.QtGui import QPixmap, QImage

import time
import csv
import numpy as np
import cv2



class VideoProcShift(QObject):
    # signals
    in_display = pyqtSignal(QPixmap)
    out_display = pyqtSignal(QPixmap)

    def __init__(self, capture, preview_window_manager=None,
                 should_mirror_preview=False):
        super(VideoProcShift, self).__init__()

        self.preview_window_manager = preview_window_manager
        self.should_mirror_preview = should_mirror_preview

        self._capture = capture
        self._channel = 0
        self._entered_frame = False
        self._in_frame = None
        self._out_frame = None
        self._image_filename = None
        self._video_filename = None
        self._front_faces_filename = None
        self._profile_faces_filename = None
        self._video_encoding = None
        self._video_writer = None
        self._faces_in = None
        self._csv_reader = None

        self._start_time = None
        self._frames_elapsed = 0
        self._fps_estimate = None
        self.fps = 29.97

        self.out_height = 100
        self.out_width = 100

        self.stopped = False

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, value):
        if self._channel != value:
            self._channel = value
            self._in_frame = None

    @property
    def frame(self):
        if self._entered_frame and self._in_frame is None:
            _, self._in_frame = self._capture.retrieve()
        return self._in_frame

    @property
    def is_writing_video(self):
        return self._video_filename is not None

    def enter_frame(self):
        """ Capture the next frame, if any. """

        # first check that previous frame has exited.
        assert not self._entered_frame, \
            'previous enter_frame() has no matching exit_frame()'

        if self._capture is not None:
            self._entered_frame = self._capture.grab()

    def exit_frame(self):
        """ update viewport, write if necessary and release the frame """

        # Check whether any grabbed frame is retrievable.
        # The getter may retrieve and cache the frame.
        if self.frame is None:
            self._entered_frame = False
            return

        # Update the FPS estimate and related variables.
        if self._frames_elapsed == 0:
            self._start_time = time.time()
        else:
            time_elapsed = time.time() - self._start_time
            self._fps_estimate = self._frames_elapsed / time_elapsed
        self._frames_elapsed += 1

        self.process_image()

        # Draw to the window
        self.in_display.emit(QPixmap.fromImage(
                                    QImage(
                                        self._in_frame.data,
                                        self._in_frame.shape[1],
                                        self._in_frame.shape[0],
                                        QImage.Format_RGB888)
                                    .rgbSwapped()))
        if self._out_frame is None:
            self._out_frame = self._in_frame

        self.out_display.emit(QPixmap.fromImage(
                                    QImage(
                                        self._out_frame.data,
                                        self._out_frame.shape[1],
                                        self._out_frame.shape[0],
                                        QImage.Format_RGB888)
                                    .rgbSwapped()))

        # write to the image file, if any needed
        # write to the video file here
        self._write_video_frame()

        # release the frame
        self._in_frame = None
        self._entered_frame = False

    def write_image(self, filename):
        """ Write the next exited frame to an image file. """
        self._image_filename = filename

    def start_writing_video(self,
                            filename,
                            encoding=cv2.VideoWriter_fourcc("I", '4', '2', '0')):
        """ Start writing exited frames to a video file. """
        self._video_filename = filename
        self._video_encoding = encoding

    def stop_writing_video(self):
        """ Stop writing exited frames to a video file. """
        self._video_filename = None
        self. _video_encoding = None
        self._video_writer = None

    def _write_video_frame(self):
        if not self.is_writing_video:
            return

        if self._video_writer is None:
            fps = self._capture.get(cv2.CAP_PROP_FPS)
            print('fps from video in: ', fps)
            if fps == 0.0:
                # The capture's FPS is unknown so use an estimate.
                if self._frames_elapsed < 20:
                    # wait until more frames elapse so that estimate
                    # is more stable.
                    return
                else:
                    fps = self._fps_estimate

            # size = (int(self._capture.get(
            #             cv2.CAP_PROP_FRAME_WIDTH)),
            #         int(self._capture.get(
            #                 cv2.CAP_PROP_FRAME_HEIGHT)))
            size = (self.out_width, self.out_height)
            self._video_writer = cv2.VideoWriter(
                        self._video_filename, self._video_encoding,
                        self.fps, size)

        self._video_writer.write(self._out_frame)

    def process_image(self):
        #
        # self._out_frame = self._in_frame.copy()
        # gray = cv2.cvtColor(self._in_frame, cv2.COLOR_BGR2GRAY)

        row = self._csv_reader.__next__()
        # print(row)
        # frame_num = int(row[0])
        ul_y = int(row[1])
        ul_x = int(row[2])
        f_width = int(row[3])
        f_height = int(row[4])
        orig = int(row[5])
        # print('ul_y: ', ul_y, 'ul_x: ', ul_x, 'f_width: ', f_width, 'f_height: ', f_height)
        if orig == 0:
            b_color = (255, 0, 0)
        else:
            b_color = (0, 0, 255)
        new_ul_y = ul_y - 20
        new_ul_x = ul_x - 15
        # new_lr_y = ul_y + f_height + self.margin_y - 1
        # new_lr_x = ul_x + f_width + self.margin_x - 1
        # self._out_frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        # cv2.rectangle((ul_x, ul_y), ((ul_x + f_width, ul_y + f_height)), [255, 0, 0], 2)
        # cv2.rectangle(self._out_frame, (ul_y - 50, ul_x - 25),
        #               (ul_y + f_height + self.margin_y, ul_x + f_width + self.margin_x), b_color, 2)
        # cv2.rectangle(self._out_frame, (new_ul_y, new_ul_x),
        #               (new_lr_y, new_lr_x), b_color, 2)

        self._out_frame = self._in_frame[new_ul_x:new_ul_x+self.out_width,
                                         new_ul_y:new_ul_y + self.out_height, :].copy()
        cv2.rectangle(self._out_frame, (0, 0),
                      (100, 100), b_color, 2)

    @pyqtSlot()
    def start_video(self):
        print("Thread started")
        self.stopped = False
        self._front_faces_filename = "front_faces_filled2.csv"
        self._faces_in = open(self._front_faces_filename, "r")
        self._csv_reader = csv.reader(self._faces_in)
        # start writing output video
        self.start_writing_video('SarahFaceOnly.avi')
        # begin main loop
        while self._capture.isOpened() and not self.stopped:
            self.enter_frame()
            self.exit_frame()

    @pyqtSlot()
    def stop_video(self):
        print("stopping in progress")
        self.stopped = True
        self._faces_in.close()
