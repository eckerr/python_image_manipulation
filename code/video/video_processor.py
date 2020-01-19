"""
 video_processor_thread class

 opens a video file, searches for faces, and writes a list
 of found faces to an output file.

  Created by Ed on 1/7/2020
 """
from PyQt5.QtCore import (QObject,
                          QThread,
                          pyqtSignal,
                          pyqtSlot)
from PyQt5.QtGui import QPixmap, QImage

import time
import csv
import numpy
import cv2



class VideoProcessor(QObject):
    # signals
    in_display = pyqtSignal(QPixmap)
    out_display = pyqtSignal(QPixmap)

    def __init__(self, capture, preview_window_manager=None,
                 should_mirror_preview=False):
        super(VideoProcessor, self).__init__()

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
        self._front_faces_filename2 = None
        self._profile_faces_filename = None
        self._video_encoding = None
        self._video_writer = None
        self._faces_out = None
        self._faces_out2 = None
        self._csv_writer = None
        self._csv_writer2 = None

        self._start_time = None
        self._frames_elapsed = 0
        self._fps_estimate = None

        self.stopped = False

        # for putting frame numbers on image
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.bottomLeftCornerOfText = (10, 250)
        self.fontScale = 1
        self.fontColor = (255, 255, 255)
        self.lineType = 2

        self.counter = 0

        self.face_cascade = cv2.CascadeClassifier(
            '.\\cascades\\lbpcascade_frontalface.xml')
        # self.face_cascade = cv2.CascadeClassifier(
        #     '.\\cascades\\haarcascade_frontalface_default.xml')
        self.profile_cascade = cv2.CascadeClassifier(
            '.\\cascades\\haarcascade_profileface.xml')

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
        # self._write_video_frame()

        # release the frame
        self._in_frame = None
        self._entered_frame = False

    def write_image(self, filename):
        """ Write the next exited frame to an image file. """
        self._image_filename = filename

    def start_writing_video(self,
                            filename,
                            encoding = cv2.VideoWriter_fourcc('A', 'I', 'C', '1')):
        """ Start writing exited frames to a video file. """
        self._video_filename = filename
        self._video_encoding = encoding

    def stop_writing_video(self):
        """ Stop writing exited frames to a video file. """
        self._video_filename = None
        self. _video_encoding = None
        self._video_writer = None

    def _write_video_frame(self):
        if not self.isWritingVideo:
            return

        if self._video_writer is None:
            fps = self._capture.get(cv2.CAP_PROP_FPS)
            if fps == 0.0:
                # The capture's FPS is unknown so use an estimate.
                if self._frames_elapsed < 20:
                    # wait until more frames elapse so that estimate
                    # is more stable.
                    return
                else:
                    fps = self._fps_estimate

            size = (int(self._capture.get(
                        cv2.CAP_PROP_FRAME_WIDTH)),
                    int(self._capture.get(
                            cv2.CAP_PROP_FRAME_HEIGHT)))
            self._video_writer = cv2.VideoWriter(
                        self._video_filename, self._video_encoding,
                        fps, size)

        self._video_writer.write(self._out_frame)

    def process_image(self):
        # self._out_frame = self._in_frame
        gray = cv2.cvtColor(self._in_frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) > 1:
            print('faces: ', faces, 'number: ', len(faces))

        if faces == ():
            pass
            # print("looking for Profile face")
            # profile_faces = self.profile_cascade.detectMultiScale(gray, 1.3, 5)
            # if profile_faces == ():
            #     print(self._frames_elapsed, "not found")
            # else:
            #     print(self._frames_elapsed, profile_faces, 'profile')
        else:
            # print(self._frames_elapsed, faces)
            # center_x, center_y = (2 * faces[0][0] + faces[0][2]) // 2, (2 * faces[0][1] + faces[0][3]) // 2
            # self._csv_writer.writerow([self._frames_elapsed, center_x, center_y])
            # self._csv_writer2.writerow([self._frames_elapsed, faces[0][0], faces[0][1], faces[0][2], faces[0][3]])

            self._out_frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            if not faces == ():
                for face in faces:
                    cv2.rectangle(self._out_frame, (face[0]-50, face[1]-25), (face[0]+face[2]+50,face[1]+face[3]+50), (255, 0, 0), 2)
            # else:
            #     if not profile_faces == ():
            #         for face in profile_faces:
            #             cv2.rectangle(self._out_frame, (face[0]-50, face[1]-25), (face[0]+face[2]+50,face[1]+face[3]+50), (0, 0, 255), 2)
        cv2.putText(img=self._out_frame,
                    text=str(self.counter),
                    org=self.bottomLeftCornerOfText,
                    fontFace=self.font,
                    fontScale=self.fontScale,
                    color=self.fontColor,
                    thickness=self.lineType)
        self.counter += 1

    @pyqtSlot()
    def start_video(self):
        print("Thread started")
        self.stopped = False
        self._front_faces_filename = "front_faces.csv"
        self._front_faces_filename2 = "front_faces2.csv"

        self._faces_out = open(self._front_faces_filename, "w", newline='')
        self._faces_out2 = open(self._front_faces_filename2, "w", newline='')
        self._csv_writer = csv.writer(self._faces_out)
        self._csv_writer2 = csv.writer(self._faces_out2)
        while self._capture.isOpened() and not self.stopped:
            self.enter_frame()
            self.exit_frame()


    @pyqtSlot()
    def stop_video(self):
        print("stopping in progress")
        self.stopped = True
        self._faces_out.close()
        self._faces_out2.close()






