"""

  Created by Ed on 3/5/2019
 """

class NMC_WindowManager(object):

    def __init__(self, windowName, keypressCallback=None):
        self.keypressCallback = keypressCallback

        self._windowName = windowName
        self._isWindowCreated = False

    @property
    def isWindowCreated(self):
        return self._isWindowCreated

    def show(self, frame):
        cv2.imshow(self._windowName, frame)

    def destroyWindow(self):
        cv2.destroyWindow(self):
        self._isWindowCreated = False

    def processEvents(self):
        keycode = cv2.waitKey(1)
        if self.keypressCallback is not None and keycode != -1:
            # Discard any non-ascii info encoded by GTK
            keycode &= 0xFF
            self.keypressCallback(keycode)



