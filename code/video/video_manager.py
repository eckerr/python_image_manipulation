"""
video_manager.py

manages reading and writing of video frames

  Created by Ed on 1/27/2020
 """
import cv2
import numpy as np
import time
from PyQt5.QtCore import (pyqtSlot,
                          pyqtSignal)

from PyQt5.QtCore import (QObject)
from PyQt5.QtGui import (QPixmap,
                         QImage)


class VideoManager(QObject):
    """ manages reading and writing video frames """
    # signals
    in_display = pyqtSignal(QPixmap)
    out_display = pyqtSignal(QPixmap)

    def __init__(self, capture,
                 in_file_name,
                 preview_window_manager=None,
                 should_mirror_preview=False):
        super(VideoManager, self).__init__()

        self._capture = capture
        self._in_file_name = in_file_name
        self.preview_window_manager = preview_window_manager
        self.should_mirror_preview = should_mirror_preview

        self.part_range_only = False
        self.full_size = False
        self.part_id = ''
        self.part_start = 0
        self.part_end = 0

        self._video_filename = None
        self._image_filename = None
        self._out_filename = "a_test.mp4"

        self._entered_frame = False
        self._in_frame = None
        self._out_frame = None
        self.not_at_end = True

        # if recording from camera set channel
        self._channel = 0

        self._video_encoding = None
        self._video_writer = None

        self.out_width = 480
        self.out_height = 270
        self._is_color = 1

        self._start_time = None
        self._frames_elapsed = 0
        self._frame_not_ready_count = 0
        self._fps_estimate = None
        self._elapsed_time = 0
        # fudge on 29.971
        self.fps = 30

    @property
    def in_image(self):
        return self._in_frame

    @property
    def out_image(self):
        return self._out_frame

    @out_image.setter
    def out_image(self, image):
        self._out_frame = image

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
            self.not_at_end, self._in_frame = self._capture.retrieve()
            return self.not_at_end, self._in_frame

    @property
    def is_writing_video(self):
        return self._video_filename is not None

    def enter_frame(self):
        """ locate next frame and grab, if any. """

        # only do it if previous frame has been released
        assert not self._entered_frame, \
            'previous enter_frame() has not been exited'

        # Grab next frame preparing to retrieve
        if self._capture is not None:
            self._entered_frame = self._capture.grab()

    def retrieve_frame(self):
        """ processes input image updates viewport, and
            writes the frame if necessary """

        # make sure grabbed frame is retrievable
        # getter may retrieve and cache the frame.
        if self.frame is None:
            self._entered_frame = False
            self._frame_not_ready_count += 1
            return False
        else:
            return True

    def update_elapsed_time_frames(self):
        # update frames elapsed and elapsed time
        if self._frames_elapsed == 0:
            self._start_time = time.time()
        else:
            self._elapsed_time = time.time() - self._start_time
            self._frames_elapsed += 1


        # process image

        # Draw to the window
        self.in_display.emit(QPixmap.fromImage(
                                    QImage(
                                        self._in_frame.data,
                                        self._in_frame.shape[1],
                                        self._in_frame.shape[0],
                                        QImage.Format_RGB888)
                                    .rgbSwapped()))

        self._out_frame = self._in_frame.copy()

        # self.out_display.emit(QPixmap.fromImage(
        #                             QImage(
        #                                 self._out_frame.data,
        #                                 self._out_frame.shape[1],
        #                                 self._out_frame.shape[0],
        #                                 QImage.Format_RGB888)
        #                             .rgbSwapped()))
        #


        # write to the image file, if needed

        # write to the video file
        # if self._frames_elapsed > self.part_start and self.not_at_end:
        #     self._write_video_frame()
        self._write_video_frame()

        # release the frame
        self._in_frame = None
        self._entered_frame = False

    # def exit_frame(self):
    #     """ processes input image updates viewport, and
    #         writes the frame if necessary """
    #
    #     # make sure grabbed frame is retrievable
    #     # getter may retrieve and cache the frame.
    #     if self.frame is None:
    #         self._entered_frame = False
    #         self._frame_not_ready_count += 1
    #         return
    #
    #     # update frames elapsed and elapsed time
    #     if self._frames_elapsed == 0:
    #         self._start_time = time.time()
    #     else:
    #         self._frames_elapsed += 1
    #
    #
    #     # process image
    #
    #     # Draw to the window
    #     self.in_display.emit(QPixmap.fromImage(
    #                                 QImage(
    #                                     self._in_frame.data,
    #                                     self._in_frame.shape[1],
    #                                     self._in_frame.shape[0],
    #                                     QImage.Format_RGB888)
    #                                 .rgbSwapped()))
    #
    #     self._out_frame = self._in_frame
    #
    #     self.out_display.emit(QPixmap.fromImage(
    #                                 QImage(
    #                                     self._out_frame.data,
    #                                     self._out_frame.shape[1],
    #                                     self._out_frame.shape[0],
    #                                     QImage.Format_RGB888)
    #                                 .rgbSwapped()))
    #
    #
    #
    #     # write to the image file, if needed
    #
    #     # write to the video file
    #     if self._frames_elapsed > self.part_start and self.not_at_end:
    #         self._write_video_frame()
    #
    #     # release the frame
    #     self._in_frame = None
    #     self._entered_frame = False
    #
    def write_image(self, filename):
        """ write the next exited frame to an image file """
        self._image_filename = filename

    def start_writing_video(self,
                            filename,
                            encoding=cv2.VideoWriter_fourcc('F', 'F', 'V', 'H')):

        """ Start writing exited frames to video file. """
        self._video_filename = filename
        self._video_encoding = encoding
        print("video writer name:", self._video_filename, self._video_encoding)

    def stop_writing_video(self):
        """ Stop writing exited frames to a video file. """
        self._video_filename = None
        self._video_encoding = None
        self._video_writer = None

    def _write_video_frame(self):
        if not self.is_writing_video:
            return

        if self._video_writer is None:
            """ create the writer if needed """
            print(self._video_writer)
            print(self._video_encoding)
            print(self.fps)
            print(self.out_height)
            print(self.out_width)

            self._video_writer = cv2.VideoWriter(
                self._video_filename,
                self._video_encoding,
                self.fps,
                (self.out_width, self.out_height),
                isColor=True)
            if self._video_writer.isOpened():
                print('Video writer has opened successfully')
                print('output size; ', self.out_height, self.out_width)
        self._video_writer.write(self._out_frame)

    @pyqtSlot()
    def start_video(self):
        print("Thread started")
        self.stopped = False

        # get needed stuff

        self.start_writing_video(self._out_filename)

        self.enter_frame()
        self.exit_frame()

        #  when done
        self.stop_writing_video()

    @pyqtSlot()
    def stop_video(self):
        print("stopping video manager")
        self.stopped = True
        if self._video_writer is not None:
            if self.video_writer.isOpened():
                self._video_writer.release()
                print('video output file closed')


