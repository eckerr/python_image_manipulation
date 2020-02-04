"""
main window to test thread reading of video files
  Created by Ed on 1/9/2020
 """


import cv2
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QMainWindow
from ui_main_window import Ui_MainWindow
from video_proc_find_face import VideoProcFindFace

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._thread = QThread()
        self._input_filename = None
        self._p_threaded = None

        self.get_input_filename()
        self.start_thread()

    def get_input_filename(self):
        self._input_filename = 'MVI_9381_small.mp4'
        # self._input_filename = 'Sara BuchhornOneQuarter.avi'

    def start_thread(self):
        self._p_threaded = VideoProcFindFace(
                        cv2.VideoCapture(self._input_filename),
                        in_file_name=self._input_filename,
                        preview_window_manager=None,
                        should_mirror_preview=True)
        self._thread.started.connect(self._p_threaded.start_video)
        # pthread.finished.connect(self.deleteLater())
        self._p_threaded.in_display.connect(self.ui.in_video.setPixmap)
        self._p_threaded.out_display.connect(self.ui.out_video.setPixmap)
        self._p_threaded.moveToThread(self._thread)

        self._thread.start()

    def closeEvent(self, event):
        print("closing out thread before closing window")
        self._p_threaded.stop_video()
        self._thread.quit()
        self._thread.wait()
        print("done waiting for thread to close")
        event.accept()





