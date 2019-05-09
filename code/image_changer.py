"""
Image Changer
  Created by Ed on 4/10/2019
 """

import os
import sys
import platform

import numpy as np

from PyQt5.QtCore import (Qt,
                          QSettings,
                          QVariant,
                          QSize,
                          QPoint,
                          QByteArray,
                          QTimer,
                          QFile,
                          QFileInfo,
                          QT_VERSION_STR,
                          PYQT_VERSION_STR)

from PyQt5.QtGui import (QImage,
                         QIcon,
                         QKeySequence,
                         QColor,
                         QPixmap,
                         QImageReader,
                         QImageWriter)

from PyQt5.QtWidgets import (QLabel,
                             QApplication,
                             QDockWidget,
                             QListWidget,
                             QMainWindow,
                             QFrame,
                             QAction,
                             QActionGroup,
                             QMenu,
                             QSpinBox,
                             QMessageBox,
                             QDialog,
                             QInputDialog,
                             QColorDialog,
                             QFileDialog)

import cv2

from histograms import hist_lines, hist_lines_split
from newimagedlg import Ui_new_image_dlg
import qrc_resources
# from my_open_cv import MyCVImage, MyCVHist

__version__ = "1.0.0"

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        # self.image = QImage()
        self.dirty = True
        self.filename = None
        self.recentFiles = []
        self.image = None
        self.cvimg = None
        self.cvimg_gray = None
        self.blur0 = None
        self.blur1 = None
        self.blur2 = None
        self.blur3 = None
        self.HF = None
        self.MHF = None
        self.MF = None
        self.LF = None

        self.mirroredvertically = False
        self.mirroredhorizontally = False

        self.image_label = QLabel()
        self.image_label.setMinimumSize(200, 200)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setCentralWidget(self.image_label)

        hist_dock_widget = QDockWidget("Histogram", self)
        hist_dock_widget.setObjectName("histDockWidget")
        hist_dock_widget.setAllowedAreas(Qt.LeftDockWidgetArea |
                                        Qt.RightDockWidgetArea)
        self.hist_label = QLabel()
        hist_dock_widget.setWidget(self.hist_label)
        self.addDockWidget(Qt.RightDockWidgetArea, hist_dock_widget)

        self.printer = None

        self.size_label = QLabel()
        self.size_label.setFrameStyle(QFrame.StyledPanel |
                                      QFrame.Sunken)
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.size_label)
        status.showMessage("Ready", 5000)

        # file menu
        actionNew = self.createAction("&New", "self.file_new", QKeySequence.New, "filenew", "Create a new image")
        actionOpen = self.createAction("&Open", "self.file_open", QKeySequence.Open, "fileopen",
                                       "Open an existing image")
        actionSave = self.createAction("&Save", "self.file_save", QKeySequence.Save, "filesave",
                                       "Open an existing image")
        actionSaveAs = self.createAction("Save &As", "self.file_save_as", "Ctrl+Shift+S", "filesaveas",
                                         "Save image under a different name")
        actionPrint = self.createAction("&Print", "self.file_print", QKeySequence.Print, "fileprint", "Print the image")
        actionExit = self.createAction("&Exit", "self.close", "Ctrl+Q", "filequit", "Exit the program")

        # edit menu

        actionInvert = self.createAction("&Invert", "self.edit_invert", "Ctrl+I", "editinvert", "Invert the image",
                                         True, "toggled")
        actionSwap = self.createAction("&Swap", "self.edit_swap", "Ctrl+A", "editswap", "Swap Red and Blue",
                                       True, "toggled")
        actionZoom = self.createAction("&Zoom", "self.edit_zoom", "Alt+Z", "editzoom", "zoom image")
        actionUnmirror = self.createAction("&UnMirror", "self.edit_un_mirror", "Ctrl+U", "editunmirror",
                                           "Un-mirror the image", True, "toggled")
        actionUnmirror.setChecked(True)
        actionMirrorH = self.createAction("Mirror &Horizontally", "self.edit_mirror_h", "Ctrl+H", "editmirrorhoriz",
                                          "Mirror the image horizontally", True, "toggled")
        actionMirrorV = self.createAction("Mirror &Vertically", "self.edit_mirror_v", "Ctrl+V", "editmirrorvert",
                                          "Mirror the image vertically", True, "toggled")

        actionBlur = self.createAction("Blur Image", "self.edit_blur", "Ctrl+B", "editblur",
                                       "Create four levels of frequency", False)

        # Help menu
        actionAbout = self.createAction("&About", "self.help_about", None, None, "About this program")
        actionHelp = self.createAction("&Help", "self.help_help", None, None, "About editing commands")

        # setup menus
        self.menuFile = self.menuBar().addMenu("&File")
        self.menuFileActions = (actionNew,
                                actionOpen,
                                actionSave,
                                actionSaveAs,
                                None,
                                actionPrint,
                                None,
                                actionExit)
        self.addActions(self.menuFile, self.menuFileActions)

        menuEdit = self.menuBar().addMenu("&Edit")
        self.addActions(menuEdit, (actionInvert,
                                   actionSwap,
                                   actionZoom))

        mirror_group = QActionGroup(self)
        mirror_group.addAction(actionUnmirror)
        mirror_group.addAction(actionMirrorH)
        mirror_group.addAction(actionMirrorV)

        mirrorMenu = menuEdit.addMenu(QIcon(":/editmirror.png"), "&Mirror")
        self.addActions(mirrorMenu, (actionUnmirror, actionMirrorH, actionMirrorV))

        # Help menu
        menuHelp = self.menuBar().addMenu("&Help")
        self.addActions(menuHelp, (actionAbout, actionHelp))

        # toolbars
        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        self.addActions(fileToolbar, (actionNew, actionOpen, actionSaveAs))

        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolBar")
        self.addActions(editToolbar, (actionInvert,
                                      actionSwap,
                                      None,
                                      actionUnmirror,
                                      actionMirrorH,
                                      actionMirrorV))
        self.zoomSpinBox = QSpinBox()
        self.zoomSpinBox.setRange(1, 400)
        self.zoomSpinBox.setSuffix(" %")
        self.zoomSpinBox.setValue(100)
        self.zoomSpinBox.setToolTip("Zoom the image")
        self.zoomSpinBox.setStatusTip(self.zoomSpinBox.toolTip())
        self.zoomSpinBox.setFocusPolicy(Qt.NoFocus)
        self.zoomSpinBox.valueChanged.connect(self.show_image)
        editToolbar.addWidget(self.zoomSpinBox)

        # setup context menu for image
        separator = QAction(self)
        separator.setSeparator(True)
        self.addActions(self.image_label, (actionInvert,
                                          actionSwap,
                                          separator,
                                          actionUnmirror,
                                          actionMirrorH,
                                          actionMirrorV))

        # setup resetable actions
        self.resetableActions = ((actionInvert, False),
                                 (actionSwap, False),
                                 (actionUnmirror, True))

        self.settings = QSettings("Kerr & Associates", "Image Changer")
        self.restoreGeometry(self.settings.value("geometry", ""))
        self.restoreState(self.settings.value("windowState", ""))
        self.recentFiles = self.settings.value("RecentFiles", [])
        print(self.recentFiles)
        self.setWindowTitle("Image Changer")

        self.update_file_menu()
        QTimer.singleShot(0, self.load_initial_file)

    # -------------------------------------------------------------------

    def createAction(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, signal="triggered"):
        print("inside createAction")
        """ Helper method to create actions """
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            slot_string = "action." + signal + ".connect(" + slot + ")"
            exec(slot_string)
        if checkable:
            action.setCheckable(True)
        return action

    def addActions(self, target, actions):
        """ Helper method to add list of actions to menus """
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def update_file_menu(self):
        print("inside update_file_menu")
        self.menuFile.clear()
        self.addActions(self.menuFile, self.menuFileActions[:-1])
        current = self.filename if self.filename is not None else None
        recent_files = []
        print("self.recentFiles: ", self.recentFiles, "\ncurrent:", current)
        for fname in self.recentFiles:
            if fname != current and QFile.exists(fname):
                recent_files.append(fname)
        if recent_files:
            self.menuFile.addSeparator()
            for i, fname in enumerate(recent_files):
                action = QAction(QIcon(":/icon.png"), "&%s %s" % (str(i+1), QFileInfo(fname).fileName()), self)
                action.setData(fname)
                action.triggered.connect(self.load_file)
                self.menuFile.addAction(action)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menuFileActions[-1])

    def file_new(self):
        print("inside file new")
        if not self.ok_continue():
            return
        dialog = QDialog()
        dialog_ui = Ui_new_image_dlg()


        dialog_ui.setupUi(dialog)
        col = QColor(64, 64, 64)
        dialog_ui.color_label_pic.pixmap = QImage().fill(col)
        dialog_ui.color_pushButton.clicked.connect(self.show_color_dlg)
        dialog.show()
        dialog.exec_()

        if dialog.exec_():
            print("we got here!!!")
            self.add_recent_file(self.filename)
            self.image = QImage()
            for action, check in self.resetableActions:
                action.setChecked(check)
                dialog_ui.color_label_pic = QImage()
                dialog_ui.color_label_pic.fill(QColor(255, 15, 15))
                self.image = dialog_ui.color_label_pic
                self.filename = None
                self.dirty = True
                self.show_image()
                self.size_label.setText("%d x %d" % (self.image.width(),
                                                     self.image.height()))
                self.update_status("Created new image")

    def file_open(self):
        """ Select the file name to be opened """
        if not self.ok_continue():
            return
        dir = os.path.dirname(self.filename)\
            if self.filename is not None else "../images"
        formats = ["Images PNG (*.png);;Jpeg (*.jpg *.jpeg);;Targa (*.tga);;SVG (*.svg)"]
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fname, mask = QFileDialog.getOpenFileName(self, caption="Choose image file to open",
                                                       directory=dir,
                                                       filter=formats[0], options=options)
        if fname:
            self.load_file(fname=fname)

    def file_save(self):
        """ if named, save the file, otherwise get a name then save """
        if self.image.isNull():
            return
        if self.filename is None:
            self.file_save_as()
        else:
            if self.image.save(self.filename, None):
                self.update_status(f"Saved as {self.filename}")
                self.dirty = False
            else:
                self.update_status(f"Failed to save {self.filename}")
        return

    def file_save_as(self):
        """ assign a new filename to save under. """
        if self.image.isNull():
            return
        fname = self.filename if self.filename is not None else "."
        # formats = ['*.bmp', '*.cur', '*.icns', '*.ico', '*.jpeg', '*.jpg', '*.pbm', '*.pgm',
        #            '*.png', '*.ppm', '*.tif', '*.tiff', '*.wbmp', '*.webp', '*.xbm', '*.xpm']

        formats = ["Images PNG (*.png);;Jpeg (*.jpg *.jpeg);;Targa (*.tga);;SVG (*.svg)"]
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fname, mask = QFileDialog.getSaveFileName(None, caption="Choose name to save as",
                                                  directory=fname,
                                                  filter=formats[0], options=options)
        print(fname, mask)
        if fname:
            if "." not in fname:
                fname += ".png"
            self.add_recent_file(fname)
            self.filename = fname
            self.file_save()

    def file_print(self):
        print("filePrint - Not Implemented yet")
        return

    def edit_invert(self, on):
        """ inverts the image channels"""
        if self.image.isNull():
            return
        self.image.invertPixels()
        self.show_image()
        self.dirty = True
        self.update_status("Inverted" if on else "Un-inverted")
        print("Invert image")

    def edit_swap(self, swapped):
        """ swaps red and blue channels"""
        if self.image.isNull():
            return
        self.image = self.image.rgbSwapped()
        self.show_image()
        self.dirty = True
        self.update_status("Blue, Green, Red" if swapped else "Red, Green, Blue")
        print("editSwap not implemented")

    def edit_zoom(self):
        if self.image.isNull():
            return
        percent, ok = QInputDialog.getInt(self, "Image Changer - Zoom",
                                              "Percent: ",
                                              self.zoomSpinBox.value(), 1, 400)
        if ok:
            self.zoomSpinBox.setValue(percent)
        print("OK: ", ok)
        return

    def edit_un_mirror(self, on):
        print(on, "On")
        print("edit_un_mirror called")
        print(self.mirroredhorizontally)
        print('vertically', self.mirroredvertically)
        return
        # if self.image.isNull():
        #     return
        # if self.mirroredhorizontally:
        #     self.edit_mirror_h(False)
        # if self.mirroredvertically:
        #     self.edit_mirror_v(False)

    def edit_mirror_h(self, on):
        if self.image.isNull():
            return
        self.image = self.image.mirrored(True, False)
        self.show_image()
        self.mirroredhorizontally = not self.mirroredhorizontally
        print("h", self.mirroredhorizontally)
        self.dirty = True
        self.update_status("Mirrored Horizontally"
                           if on else "Un-mirrored Horizontally")

    def edit_mirror_v(self, on):
        if self.image.isNull():
            return
        self.image = self.image.mirrored(False, True)
        self.show_image()
        self.mirroredvertically = not self.mirroredvertically
        print("v", self.mirroredvertically)
        self.dirty = True
        self.update_status("Mirrored Vertically"
                           if on else "Un-mirrored Vertically")

    def edit_blur(self):
        pass

    def help_about(self):
        QMessageBox.about(self, "About Image Changer",
                          """<b>Image Changer</b> v %s
                          <p>Copyright &copy; 2019.
                          All rights reserved.
                          <p>This application can be used to perform
                          simple image manipulations.
                          <p>Python %s - Qt %s
                          - PyQt %s on %s """ % (__version__,
                          platform.python_version(), QT_VERSION_STR, PYQT_VERSION_STR, platform.system()))
        print("about not yet implemented")
        return

    def help_help(self):
        print("Help not yet implemented")
        return

    def load_initial_file(self):
        print("inside loadInitialFile")
        settings = QSettings("Kerr & Associates", "Image Changer")
        files = settings.value('RecentFiles', [])
        fname = ''
        if files:
            fname = files[0]
        if fname and QFile.exists(fname):
            self.load_file(fname)
        print("fname: ", fname)
        print("loadInitialFile implemented")

    def load_file(self, fname=None):
        """ method to actually load the file """
        if fname is None:
            # coming from a recent file action - need to get full file name
            action = self.sender()
            print("filename is None - action: ", action, action.data())
            if isinstance(action, QAction):
                fname = action.data()
                if not self.ok_continue():
                    return
            else:
                return
        if fname:
            self.filename = None
            print(fname)
            image = QImage(fname)
            if image.isNull():
                print("image is null")
                message = "Failed to read %s" % fname
            else:
                self.add_recent_file(fname)
                self.image = QImage()
                for action, check in self.resetableActions:
                    action.setChecked(check)
                    print(action, check)
                self.image = image
                self.filename = fname
                print("calling show_image")
                self.show_image()
                print("returned from show_image")
                self.dirty = False
                self.size_label.setText("%d x %d" % (image.width(), image.height()))
                print("%d x %d" % (image.width(), image.height()), self.dirty)
                message = "Loaded %s" % os.path.basename(fname)
            self.update_status(message)
            self.cvimg = cv2.imread(fname)
            self.cvimg_gray = cv2.imread(fname, 0)
            cv2.imshow('cv image', self.cvimg_gray)
            self.create_histogram()
            cv2.waitKey()
            cv2.destroyAllWindows()
        print("exiting loadFile")

    def create_histogram(self):
        hist_pics = hist_lines_split(self.cvimg)
        hist_pics[3] = hist_lines(self.cvimg_gray)
        res = np.vstack((hist_pics[0], hist_pics[1], hist_pics[2], hist_pics[3]))
        cv2.imshow('histogram', res)
        cv2.imshow('image', self.cvimg)



    def add_recent_file(self, fname):
        if fname is None:
            print("no filename - returning")
            return
        print("self.recentFiles: ", self.recentFiles)
        print("\n\nfname: ", fname)
        if fname not in self.recentFiles:
            self.recentFiles.insert(0, fname)
            # don't allow list to contain more than 9 file names
            while len(self.recentFiles) > 9:
                self.recentFiles.pop(-1)
            print("final list of recent files: ", self.recentFiles)

    def update_status(self, message):
        print("inside update_status")
        #return
        self.statusBar().showMessage(message, 5000)
        self.hist_label.setText(message)
        if self.filename is not None:
            self.setWindowTitle("Image Changer - %s[*]" %
                                os.path.basename(self.filename))
        elif not self.image.isNull():
            self.setWindowTitle("Image Changer - Unnamed[*]")
        else:
            self.setWindowTitle("Image Changer[*]")
        self.setWindowModified(self.dirty)

    def show_color_dlg(self):
        print("inside show_color_dlg")
        col = QColorDialog.getColor()
        if col.isValid():
            self.dialog.setStyleSheet("QWidget | background-color: %s"
                                         % col.name())
            self.dialog.color_label_pic.pixmap = QImage().fill(col)

            print("color is valid")

    def show_image(self, percent=None):
        print("inside show_image")
        if self.image.isNull():
            print(self.image)
            return
        if percent is None:
            percent = self.zoomSpinBox.value()
            print("percent: ", percent)
        factor = percent/100
        print("factor: ", factor)
        width = self.image.width() * factor
        height = self.image.height() * factor
        image = self.image.scaled(width, height, Qt.KeepAspectRatio)
        self.image_label.setPixmap(QPixmap.fromImage(image))

    def closeEvent(self, event):
        print("inside closeEvent")
        if self.ok_continue():
            self.settings = QSettings("Kerr & Associates", "Image Changer")
            self.settings.setValue("geometry", self.saveGeometry())
            self.settings.setValue("windowState", self.saveState())
            self.settings.setValue("RecentFiles", self.recentFiles)
            QMainWindow.closeEvent(self, event)
        else:
            event.ignore()

    def ok_continue(self):
        print("inside ok_continue")
        if self.dirty:
            reply = QMessageBox.question(self,
                                         "Image Changer - Unsaved Changes",
                                         "Save unsaved changes?",
                                         QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                self.file_save()
        print("Dirty: ", self.dirty)
        new_image = self.image.convertToFormat(4)
        return True

# ---------------------------------------------------------------


if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setOrganizationName("Kerr & Associates")
    app.setOrganizationDomain("edkerrassociates.com")
    app.setApplicationName("Image Changer")
    app.setWindowIcon(QIcon(":/icon"))
    form = MainWindow()
    form.show()
    app.exec_()

