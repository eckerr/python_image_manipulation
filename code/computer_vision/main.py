"""

  Created by Ed on 11/29/2019
 """
import sys
from PyQt5 import QtWidgets

from MainWindow import MainWindow

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory().keys()[2])
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())