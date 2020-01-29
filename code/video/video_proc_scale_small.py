"""
 video_processor_thread class

 opens a video file, scales it to 1/8th size, saves file.

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


class VideoProcScaleSmall(QObject):
    # signals
    in_display = pyqtSignal(QPixmap)
    out_display = pyqtSignal(QPixmap)

    def __init__(self, capture,
                 in_file_name,
                 preview_window_manager=None,
                 should_mirror_preview=False):
        super(VideoProcScaleSmall, self).__init__()

        self.in_file_name = in_file_name
        self.preview_window_manager = preview_window_manager
        self.should_mirror_preview = should_mirror_preview

        self._out_filename = self.in_file_name[:-4] + '_small.mp4'
        self._capture = capture
        self._channel = 0
        self._entered_frame = False
        self._in_frame = None
        self._out_frame = None
        self._image_filename = None
        self._video_filename = None
        self._front_faces_filename = None
        self._front_faces_filename2 = None
        self._profile_faces_filename = None
        self._video_encoding = None
        self._video_writer = None


        self._start_time = None
        self._frames_elapsed = 0
        self._fps_estimate = None
        self.fps = 29.971

        self.out_width = 480
        self.out_height = 270

        self.counter = 0

        self.stopped = False

        # for putting frame numbers on image
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.bottomLeftCornerOfText = (20, self.out_height-10)
        self.fontScale = 1
        self.fontColor = (255, 255, 255)
        self.lineType = 2

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
            print('out frame is not set up')
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
                            # encoding=cv2.VideoWriter_fourcc('I', '4', '2', '0')):
                            encoding=cv2.VideoWriter_fourcc('F', 'F', 'V', 'H')):
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
            # print('no video writer')
            # fps = self._capture.get(cv2.CAP_PROP_FPS)
            # print('fps: ', fps)
            # if fps == 0.0:
            #     # The capture's FPS is unknown so use an estimate.
            #     if self._frames_elapsed < 20:
            #         # wait until more frames elapse so that estimate
            #         # is more stable.
            #         return
            #     else:
            #         fps = self._fps_estimate

            fps = 30.0000
            size = (self.out_width, self.out_height)
            self._video_writer = cv2.VideoWriter(
                        self._video_filename, self._video_encoding,
                        fps, size, isColor=True)
            print("Video writer has opened successfully: ", self._video_writer.isOpened(),
                  "size: ", size)

        self._video_writer.write(self._out_frame)


    def process_image(self):
        self._out_frame = cv2.resize(src=self._in_frame,
                   dsize=(self.out_width, self.out_height),
                   dst=self._out_frame,
                   fx=0,
                   fy=0,
                   interpolation=cv2.INTER_AREA)
        # self._out_frame = self._in_frame.copy()
        # print(self._out_frame.shape)
        cv2.putText(img=self._out_frame,
                    text=str(self.counter),
                    org=self.bottomLeftCornerOfText,
                    fontFace=self.font,
                    fontScale=self.fontScale,
                    color=self.fontColor,
                    thickness=2)
        self.counter += 1

    @pyqtSlot()
    def start_video(self):
        print("Thread started")
        self.stopped = False
        # start writing output video
        self.start_writing_video(self._out_filename)
        # begin main loop
        while self._capture.isOpened() and not self.stopped:
            self.enter_frame()
            self.exit_frame()


    @pyqtSlot()
    def stop_video(self):
        print("stopping in progress")
        self.stopped = True
        self._video_writer.release()







