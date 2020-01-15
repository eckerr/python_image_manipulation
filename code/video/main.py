"""

  Created by Ed on 01/09/2020
 """
import sys
from PyQt5 import QtWidgets

from main_window import MainWindow

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory().keys()[2])
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())