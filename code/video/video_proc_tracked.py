"""
 video_proc_tracked class  based off video_proc_shift for using tracked file

 opens a video file, loads a list of found face centers,
 then shifts the image to place the face at the center

  Created by Ed on 2/4/2020
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



class VideoProcTracked(QObject):
    # signals
    in_display = pyqtSignal(QPixmap)
    out_display = pyqtSignal(QPixmap)

    def __init__(self, capture,
                 in_file_name,
                 preview_window_manager=None,
                 should_mirror_preview=False):
        super(VideoProcTracked, self).__init__()

        self._in_file_name = in_file_name
        self.preview_window_manager = preview_window_manager
        self.should_mirror_preview = should_mirror_preview

        self.part_range_only = True
        self.full_size = True
        name_parts = self._in_file_name.split('-')
        self.part_id = 'Tr'
        self.part_start = int(name_parts[1])
        self.part_end = int(name_parts[2])
        print('range of frames being output: ', self.part_start, '-', self.part_end)
        # may want to move to method
        if self.full_size:
            self._out_filename = self._in_file_name[:8] + '-' +\
                                 name_parts[1] + '-' + name_parts[2] + 'BigFace.mp4'
        else:
            self._out_filename = self._in_file_name[:-4] + self.part_id + '-' + \
                                 name_parts[1] + '-' + name_parts[2] + 'FaceOnly.mp4'

        self._capture = capture
        self._channel = 0
        self._entered_frame = False
        self._in_frame = None
        self._out_frame = None
        self._image_filename = None
        self._video_filename = None

        if self.full_size:
            self._faces_filename = self._in_file_name[:-4] + '.csv'
        else:
            self._faces_filename = self._in_file_name[:-4] + '.csv'
        self._front_faces_filename = None
        self._profile_faces_filename = None
        self._video_encoding = None
        self._video_writer = None
        self._faces_in = None
        self._faces = None
        self._faces_index = 0
        self._csv_reader = None

        self.out_width = None
        self.out_height = None
        self._start_time = None
        self._frames_elapsed = 0
        self._fps_estimate = None
        # self.fps = 29.971
        self.fps = 30

        self.stopped = False

        # for putting frame numbers on image
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.bottomLeftCornerOfText = (10, 80)
        self.fontScale = 1
        self.fontColor = (255, 255, 255)
        self.lineType = 2

        self.counter = 0

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
        # self.in_display.emit(QPixmap.fromImage(
        #                             QImage(
        #                                 self._in_frame.data,
        #                                 self._in_frame.shape[1],
        #                                 self._in_frame.shape[0],
        #                                 QImage.Format_RGB888)
        #                             .rgbSwapped()))
        # if self._out_frame is None:
        #     print("out frame is None")
        #     # self._out_frame = self._in_frame
        #     self._out_frame = np.ones(640, 640, 3)
        #     # self._out_frame = np.ones(self.out_width, self.out_height, 3)

        self.out_display.emit(QPixmap.fromImage(
                                    QImage(
                                        self._out_frame.data,
                                        self._out_frame.shape[1],
                                        self._out_frame.shape[0],
                                        QImage.Format_RGB888)
                                    .rgbSwapped()))

        # write to the image file, if any needed
        # write to the video file here
        # if self._faces_index >= self.part_start and self._faces_index < len(self._faces):
        # time.sleep(.8)
        self._write_video_frame()

        # release the frame
        self._in_frame = None
        self._entered_frame = False

    def write_image(self, filename):
        """ Write the next exited frame to an image file. """
        self._image_filename = filename

    def start_writing_video(self,
                            filename,
                            # encoding=cv2.VideoWriter_fourcc("I", '4', '2', '0')):
                            encoding=cv2.VideoWriter_fourcc('F', 'F', 'V', 'H')):

        """ Start writing exited frames to a video file. """
        print('setup for start writing video')
        self._video_filename = filename
        self._video_encoding = encoding
        print(self._video_filename)
        print(self._video_encoding)

    def stop_writing_video(self):
        """ Stop writing exited frames to a video file. """
        self._video_filename = None
        self. _video_encoding = None
        self._video_writer = None

    def _write_video_frame(self):
        # print('is writing videos: ', self.is_writing_video)
        if not self.is_writing_video:
            return

        if self._video_writer is None:
            fps = self._capture.get(cv2.CAP_PROP_FPS)
            print('fps from video in: ', fps)
            fps = 30.0000
            # if fps == 0.0:
            #     # The capture's FPS is unknown so use an estimate.
            #     if self._frames_elapsed < 20:
            #         # wait until more frames elapse so that estimate
            #         # is more stable.
            #         return
            #     else:
            #         fps = self._fps_estimate
            #
            # size = (int(self._capture.get(
            #             cv2.CAP_PROP_FRAME_WIDTH)),
            #         int(self._capture.get(
            #                 cv2.CAP_PROP_FRAME_HEIGHT)))
            size = (self.out_width, self.out_height)
            print("video size: ", size)
            # size = (640, 640)

            self._video_writer = cv2.VideoWriter(
                        self._video_filename, self._video_encoding,
                        fps, size, isColor=True)
            if self._video_writer.isOpened():
                print("Video writer has opened successfully: ", self._video_writer.isOpened(),
                      "size: ", size)
            else:
                print('Video Writer failed to open')
        # print('should write video here')
        self._video_writer.write(self._out_frame)
        # print(self._out_frame.shape, self._faces_index)

    def process_image(self):
        # print('processing image')
        #
        # self._out_frame = self._in_frame[:102,
        #                                  :102, 0:3].copy()
        # gray = cv2.cvtColor(self._in_frame, cv2.COLOR_BGR2GRAY)

        # row = self._csv_reader.__next__()
        # # print(row)
        # # frame_num = int(row[0])
        # ul_y = int(row[1])
        # ul_x = int(row[2])
        # f_width = int(row[3])
        # f_height = int(row[4])
        # orig = int(row[5])
        # row = self._csv_reader.__next__()
        # print(row)
        # frame_num = int(row[0])



        ul_y = self._faces[self._faces_index][1]
        ul_x = self._faces[self._faces_index][2]
        self.out_width = self._faces[self._faces_index][3]
        self.out_height = self._faces[self._faces_index][4]
        if self.full_size:
            ul_y *= 4
            ul_x *= 4
            self.out_width *= 4
            self.out_height *= 4
        # f_width = self._faces[self._faces_index][3]
        # f_height = self._faces[self._faces_index][4]
        # orig = self._faces[self._faces_index][5]
        # print('ul_y: ', ul_y, 'ul_x: ', ul_x, 'f_width: ', f_width, 'f_height: ', f_height)
        # if orig == 0:
        #     b_color = (255, 0, 0)
        b_color = (255, 0, 0)
        # else:
        #     b_color = (0, 0, 255)
        # new_ul_y = ul_y - (self.out_width//5)
        # new_ul_x = ul_x - (self.out_height//5)
        # new_lr_y = ul_y + f_height + self.margin_y - 1
        # new_lr_x = ul_x + f_width + self.margin_x - 1
        # self._out_frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        # cv2.rectangle((ul_x, ul_y), ((ul_x + f_width, ul_y + f_height)), [255, 0, 0], 2)
        # cv2.rectangle(self._out_frame, (ul_y - 50, ul_x - 25),
        #               (ul_y + f_height + self.margin_y, ul_x + f_width + self.margin_x), b_color, 2)
        # cv2.rectangle(self._out_frame, (new_ul_y, new_ul_x),
        #               (new_lr_y, new_lr_x), b_color, 2)

        # self._out_frame = self._in_frame[0:200,
        #                                  0:200, :].copy()
        # self._out_frame = self._in_frame[new_ul_x:new_ul_x+self.out_width+2,
        #                                  new_ul_y:new_ul_y + self.out_height+2, :].copy()
        # print('new_ul_x:', new_ul_x, new_ul_x + self.out_width,  'self.out_width: ', self.out_width)
        # print('new_ul_y:', new_ul_y, new_ul_y + self.out_height, 'self.out_height:,', self.out_height)

        self._out_frame = self._in_frame[ul_x: ul_x + self.out_height,
                                         ul_y: ul_y + self.out_width, :].copy()
        # print(self._out_frame.shape)
        # self._out_frame = self._in_frame[new_ul_x: new_ul_x+self.out_width,
        #                                  new_ul_y: new_ul_y + self.out_height, :].copy()
        # print(ul_x, ul_y, self.out_width, self.out_height)
        # cv2.rectangle(self._out_frame, (0, 0),
        #               (self.out_height-2, self.out_width-2), b_color, 2)
        # print('out frame shape: ', self._out_frame.shape)
        # put frame number on image
        # cv2.putText(img=self._out_frame,
        #             text=str(self._faces[self._faces_index][0]),
        #             org=self.bottomLeftCornerOfText,
        #             fontFace=self.font,
        #             fontScale=self.fontScale,
        #             color=self.fontColor,
        #             thickness=2)
        self._faces_index += 1

    @pyqtSlot()
    def start_video(self):
        local_counter = 0
        print("Thread started")
        self.stopped = False
        self._faces = np.loadtxt(self._faces_filename, delimiter=',', dtype=np.int32)
        # self.faces_filename = "front_faces_filled2.csv"
        # self._faces_in = open(self._front_faces_filename, "r")
        # self._csv_reader = csv.reader(self._faces_in)
        if self._faces is not None:
            print('face file loaded', len(self._faces))

        # Set the output width and height
        self.out_width = int(self._faces[0][3])
        self.out_height = int(self._faces[0][4])
        print(self.out_width, self.out_height, 'before scaling')
        if self.full_size:
            self.out_width *= 4
            self.out_height *= 4
        print(' width x height: ', self.out_width, self.out_height)
        # start writing output video
        self.start_writing_video(self._out_filename)

        # point to first frame in range being processed
        self._capture.set(cv2.CAP_PROP_POS_FRAMES, self.part_start)
        print("starting at frame:", self.part_start)

        # begin main loop
        print('capture open: ', self._capture.isOpened())
        print('self.stopped: ', self.stopped)
        print('faces index:', self._faces_index)
        while self._capture.isOpened() and not self.stopped and self._faces_index < (len(self._faces)):
            self.enter_frame()
            self.exit_frame()
            local_counter += 1
        print('Main Loop Finished')
        self.stop_video()

    @pyqtSlot()
    def stop_video(self):
        print("stopping in progress")
        self.stopped = True
        if self._video_writer:
            self._video_writer.release()
        # self._faces_in.close()
