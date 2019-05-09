"""
Image Changer
  Created by Ed on 4/10/2019
 """

import os
import platform
import sys

from PyQt5.QtCore import (Qt,
                         QSettings,
                         QVariant,
                         QSize,
                         QPoint,
                         QByteArray,
                         QTimer,
                         QFile,
                         QFileInfo)

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
                             QColorDialog,
                             QFileDialog)

from debug_dec import debug

# import helpform
from newimagedlg import Ui_new_image_dlg
import qrc_resources

__version__ = "1.0.0"

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.image = QImage()
        self.dirty = False
        self.filename = None
        self.recentFiles = []
        self.mirroredvertically = False
        self.mirroredhorizontally = False

        self.image_label = QLabel()
        self.image_label.setMinimumSize(200, 200)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setCentralWidget(self.image_label)

        log_dock_widget = QDockWidget("Log", self)
        log_dock_widget.setObjectName("LogDockWidget")
        log_dock_widget.setAllowedAreas(Qt.LeftDockWidgetArea |
                                        Qt.RightDockWidgetArea)
        self.list_widget = QListWidget()
        log_dock_widget.setWidget(self.list_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, log_dock_widget)

        self.printer = None

        self.size_label = QLabel()
        self.size_label.setFrameStyle(QFrame.StyledPanel |
                                      QFrame.Sunken)
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.size_label)
        status.showMessage("Ready", 5000)

        # file menu
        # actionNew = QAction("&New", self, shortcut=QKeySequence.New, toolTip="Create a new image", statusTip="Create a new image",
        #                     icon=QIcon(":/filenew.png"), triggered=self.fileNew)
        actionNew = self.createAction("&New", "self.fileNew", QKeySequence.New, "filenew", "Create a new image")
        actionOpen = self.createAction("&Open", "self.file_open", QKeySequence.Open, "fileopen", "Open an existing image")
        actionSave = self.createAction("&Save", "self.fileSave", QKeySequence.Save, "filesave", "Open an existing image")
        actionSaveAs = self.createAction("Save &As", "self.fileSaveAs", "Ctrl+Shift+S", "filesaveas",
                                         "Save image under a different name")
        actionPrint = self.createAction("&Print", "self.filePrint", QKeySequence.Print, "fileprint", "Print the image")
        actionExit = self.createAction("&Exit", "self.close", "Ctrl+Q", "filequit", "Exit the program")

        # edit menu
        actionInvert = self.createAction("&Invert", "self.editInvert", "Ctrl+I", "editinvert", "Invert the image",
                                         True, "toggled")
        actionSwap = self.createAction("&Swap", "self.editSwap", "Ctrl+A", "editswap", "Swap Red and Blue")
        actionZoom = self.createAction("&Zoom", "self.editZoom", "Alt+Z", "editzoom", "zoom image")
        actionUnmirror = self.createAction("&UnMirror", "self.editUnmirror", "Ctrl+U", "editunmirror",
                                           "Unmirror the image", True, "toggled")
        actionUnmirror.setChecked(True)
        actionMirrorH = self.createAction("Mirror &Horizontally", "self.editMirrorH", "Ctrl+H", "editmirrorhoriz",
                                          "Mirror the image horizontally")
        actionMirrorV = self.createAction("Mirror &Vertically", "self.editMirrorV", "Ctrl+V", "editmirrorvert",
                                          "Mirror the image vertically")

        # Help menu
        actionAbout = self.createAction("&About", "self.helpAbout", None, None, "About this program")
        actionHelp = self.createAction("&Help", "self.helpHelp", None, None, "About editing commands")

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

        # size = settings.value("MainWindow/Size",
        #                       QVariant(QSize(600, 500)))
        # self.resize(size)
        # position = settings.value("MainWindow/Position",
        #                           QVariant(QPoint(0, 0)))
        # self.move(position)
        ba = QByteArray()
        #self.restoreGeometry(settings.value("Geometry"), ba)
        # self.restoreState(settings.value("MainWindow/State"))
        self.setWindowTitle("Image Changer")

        # self.update_file_menu()
        #QTimer.singleShot(0, self.loadInitialFile)



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
        return

    def update_file_menu(self):
        return
        print("inside update_file_menu")
        self.menuFile.clear()
        self.addActions(self.menuFile, self.menuFileActions[:-1])
        current = self.filename if self.filename is not None else None
        recentFiles= []
        print("self.recentFiles: ", self.recentFiles, "\ncurrent:", current)
        for fname in self.recentFiles:
            if fname != current and QFile.exists(fname):
                recentFiles.append(fname)
            if recentFiles:
                self.menuFile.addSeparator()
                for i, fname in enumerate(recentFiles):
                    action = QAction(QIcon(":/icon.png", "&%s %s" % (
                        i +1, QFileInfo(fname).fileName()), self))
                    action.setData(QVariant(fname))
                    action.triggered.connect(self.load_file)
                    self.menuFile.addAction(action)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menuFileActions[-1])
        return
    def fileNew(self):
        print("inside file new")
        if not self.okToContinue():
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
            return

    def file_open(self):
        print("inside file_open")
        if not self.okToContinue():
            return
        dir = os.path.dirname(self.filename)\
            if self.filename is not None else "../images"
        s_formats = ["*.%s" % str(format) for format in QImageReader.supportedImageFormats()]
        s_f_list = []
        for format in s_formats:
            s_f_list.append(format.replace("b'", "").replace("'", ""))
        print('supported file formats: ', s_f_list)
        # formats = ["Images PNG (*.png)\nJpeg (*.jpg *.jpeg)\nTarga (*.tga)"]
        # print(formats)
        fname, filter = QFileDialog.getOpenFileName(self,
                                            "Image Changer - Choose Image", dir,
                                            "Image files (%s)" % ' '.join(s_f_list))
        if fname:
            self.loadFile(fname)
        print("returned from loadFile")
        return

    def fileSave(self):
        print("inside fileSave")
        if self.image.isNull():
            return
        if self.filename is None:
            self.fileSaveAs()
        else:
            if self.image.save(self.filename, None):
                self.update_status(f"Saved as {self.filename}")
                self.dirty = False
            else:
                self.update_status(f"Failed to save {self.filename}")
        print("file save")
        return

    def fileSaveAs(self):
        print("file save as ...")
        if self.image.isNull():
            return
        fname = self.filename if self.filename is not None else "."
        # formats = ["Images PNG (*.png)\nJpeg (*.jpg *.jpeg)\nTarga (*.tga)"]
        # for format in formats:
        #     format.replace("b'", "*.").replace("'", "")
        formats = ['*.bmp', '*.cur', '*.icns', '*.ico', '*.jpeg', '*.jpg', '*.pbm', '*.pgm',
                   '*.png', '*.ppm', '*.tif', '*.tiff', '*.wbmp', '*.webp', '*.xbm', '*.xpm']

        fname, mask = QFileDialog.getSaveFileName(self,
                                            "Image Changer - Save Image", fname,
                                            "Image files(%s" % " ".join(formats))
        print(fname, mask)
        if fname:
            if "." not in fname:
                fname += ".png"
            self.add_recent_file(fname)
            self.filename = fname
            self.fileSave()
        return

    def filePrint(self):
        print("filePrint - Not Implemented yet")
        return

    def editInvert(self):
        print("Invert image")
        return

    def editSwap(self):
        print("editSwap not implemented")
        return

    def editZoom(self):
        print("editZoom not implemented")
        return

    def editUnmirror(self):
        print("editUnmirror - not implemented")
        return

    def editMirrorH(self):
        print("editMirrorH - not implemented")
        return

    def editMirrorV(self):
        print("editMirrorV - not implemented")
        return

    def helpAbout(self):
        print("about not yet implemented")
        return

    def helpHelp(self):
        print("Help not yet implemented")
        return

    def loadInitialFile(self):
        print("inside loadInitialFile")
        settings = QSettings("Kerr & Associates", "Image Changer")
        files = settings.value('RecentFiles', [])
        fname = ''
        if files:
            fname = files[0]
        if fname and QFile.exists(fname):
            self.loadFile(fname)
        print("fname: ", fname)
        print("loadInitialFile - not fully implemented")
        return

    def loadFile(self, fname=None):
        print("inside loadFile", fname)
        if fname is None:
            # coming from a recent file action - need to get full file name
            action = self.sender()
            print("filename is None - action: ", action, action.data())
            if isinstance(action, QAction):
                fname = action.data()
                if not self.okTContinue():
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
                print("%d x %d" % (image.width(), image.height()))
                message = "Loaded %s" % os.path.basename(fname)
            self.update_status(message)
        print("exiting loadFile")
        return

    def add_recent_file(self, fname):
        pass
        # print("inside add_recent_file")
        # if fname is None:
        #     print("no filename - returning")
        #     return
        # print(self.recentFiles)
        # print("\n\nfname: ", fname)
        # if fname not in self.recentFiles:
        #     self.recentFiles.insert(0, fname)
        #     # don't allow list to contain more than 9 file names
        #     while len(self.recentFiles) > 9:
        #         self.recentFiles.pop(-1)
        #     print("final list of recent files: ", self.recentFiles)

    def update_status(self, message):
        print("inside update_status")
        #return
        self.statusBar().showMessage(message, 5000)
        self.list_widget.addItem(message)
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
        pass

    def show_image(self, percent=None):
        print("inside show_image")
        if self.image.isNull():
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
        if self.okToContinue():
            self.settings = QSettings("Kerr & Associates", "Image Changer")
            self.settings.setValue("geometry", self.saveGeometry())
            self.settings.setValue("windowState", self.saveState())
            self.settings.setValue("RecentFiles", self.recentFiles)
            QMainWindow.closeEvent(self, event)

    def okToContinue(self):
        print("inside okToContinue")
        if self.dirty:
            reply = QMessageBox.question(self,
                                         "Image Changer - Unsaved Changes",
                                         "Save unsaved changes?",
                                         QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                self.fileSave()
        print("Dirty: ", self.dirty)
        return True

            # filename = QVariant(QString(self.filename)) if self.filename is not None else QVariant()


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("Kerr & Associates")
    app.setOrganizationDomain("edkerrassociates.com")
    app.setApplicationName("Image Changer")
    app.setWindowIcon(QIcon(":/icon"))
    form = MainWindow()
    form.show()
    app.exec_()

# ---------------------------------------------------------------
if __name__ == "__main__":

    main()
