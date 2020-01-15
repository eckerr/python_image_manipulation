"""
MainWindow class
  Created by Ed on 11/29/2019
 """

import os
import os.path
import sys
import platform
from ui_cvmainwindow import Ui_MainWindow
import sys
import cv2 as cv
from PyQt5.QtGui import (
                         QPixmap,
                         QDragEnterEvent,
                         QDropEvent,
                         QResizeEvent,
                         QImage
                         )


from PyQt5.QtCore import (
                          QFileInfo,
                          QMimeData,
                          QStringListModel,
                          QSettings,
                          QDir,
                          QFile,
                          QTextStream,
                          QObject
                          )

from PyQt5.QtCore import (Qt,
                          pyqtSignal
                          )

from PyQt5.QtWidgets import (
                             QApplication,
                             QMainWindow,
                             QMessageBox,
                             QGraphicsScene,
                             QGraphicsPixmapItem,
                             QGraphicsView,
                             QFileDialog,
                             QAction,
                             QWidget,
                             QMenu,
                             QStyle,
                             QStyleFactory
                             )
from qenhancedgraphicsview import QEnhancedGraphicsView

__version__ = "1.0.0"
PLUGINS_SUBFOLDER = "cvplugins."
LANGUAGES_SUBFOLDER = "./languages/"
THEMES_SUBFOLDER = "./themes/"
FILE_ON_DISK_DYNAMIC_PROPERTY = "absolute_file_path"
FILE_ON_DISK_BASENAME_PROPERTY = "base_name"

settings = QSettings("EdKerr", "Computer_Vision")
current_theme_file = ""
current_language_file = ""
current_plugin_file = ""

# available styles['windowsvista', 'Windows', 'Fusion']

class MainWindow(QMainWindow):
    """ drag and drop computer vision """
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.setAcceptDrops(True)
        self.scene = QGraphicsScene()

        self.originalImage = QImage()
        self.originalPixmap = QGraphicsPixmapItem()
        self.originalMat = None
        self.processedPixmap = QGraphicsPixmapItem()
        self.processedMat = None
        self.processedImage = QImage()

        self.filename = ""
        self.current_plugin_file = ""
        self.currentPlugin = None
        self.currentPluginGui = None

        self.load_settings()

        self.populate_plugin_menu()
        self.populate_languages_menu()
        self.populate_themes_menu()

        self.ui.graphicsView.setScene(self.scene)
        self.scene.addItem(self.originalPixmap)
        self.scene.addItem(self.processedPixmap)

        self.ui.graphicsView.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        QApplication.instance().setStyle(QStyleFactory().keys()[2])

    #
    # def destroy_main_window(self):
    #     delete currentPlugin
    #     delete ui


    def load_settings(self):
        print("load settings - to be implemented")
        current_theme_file = settings.value("currentThemeFile", "")
        current_language_file = settings.value("currentLanguageFile", "")
        current_Plugin_file = settings.value("currentPluginFile", "")

    def save_settings(self):
        settings.setValue("currentThemeFile", current_theme_file)
        settings.setValue("currentLanguageFile", current_language_file)
        settings.setValue("currentPluginFile", current_plugin_file)
        print("processed save settings")

    # def changeEvent(self, event):
    #     pass
        # print('changeEvent')
        # print(type(event))
        # if (event.type() == QEvent::LanguageChange):
        #     self.ui.retranslateUi(self)
        # else:
        #     self.ui.changeEvent(event)
        # self.ui.graphicsView.changeEvent(event)

    def closeEvent(self, event):
        result = QMessageBox.warning(self, "Exit",
                                     "Are you sure you want to exit?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if result == QMessageBox.Yes:
            self.save_settings()
            event.accept()
        else:
            event.ignore()
        # self.show()


    def populate_plugin_menu(self):
        print("populate plugins - to be implemented")
        print(QDir.current())
        print(PLUGINS_SUBFOLDER)
        plugins_dir = (QDir(PLUGINS_SUBFOLDER))
        plugin_files = plugins_dir.entryInfoList(QDir.NoDotAndDotDot | QDir.Files, QDir.Name)
        for plugin in plugin_files:
            print(plugin.fileName())
            if plugin.fileName().startswith("pi_"):
                pi_fileName = plugin.fileName()[3:]
                print(pi_fileName)
                # exec("import " + PLUGINS_SUBFOLDER + plugin.baseName() + " as pi")
                # from cvplugins.copymakeborder_plugin import CopyMakeBorder_Plugin
                # self.currentPluginGui = CopyMakeBorder_Plugin()
                # self.currentPluginGui = QWidget()
                pluginAction = QAction(pi_fileName[0:-3], self)
                pluginAction.setProperty(FILE_ON_DISK_BASENAME_PROPERTY, plugin.baseName())
                # pluginAction.triggered.connect(self.on_PluginActionTriggered)
                slot_string = "pluginAction." + "triggered" + ".connect(" + "self.on_PluginActionTriggered" + ")"
                print(slot_string)
                exec(slot_string)
                self.ui.menu_Plugins.addAction(pluginAction)
            # slot_string = "action." + signal + ".connect(" + slot + ")"
        print("plugin actions:", self.ui.menu_Plugins.actions().count(pluginAction))
        if self.ui.menu_Plugins.actions().count(pluginAction) <= 0:
            text_string = f"This application cannot work without plugins!"\
             "\nMake sure that '" + f"{PLUGINS_SUBFOLDER}" + \
             "' folder exists in the\n same folder as the application and that "\
             "there\n are some filter plugins inside it"
            QMessageBox.critical(self, "No Plugins", text_string)
            self.setEnabled(False)

    def populate_languages_menu(self):
        print("populate languages - to be implemented")
        pass

    def populate_themes_menu(self):
        themesMenu = QMenu(self)
        defaultThemeAction = QAction("Default",self)
        defaultThemeAction.setProperty(FILE_ON_DISK_DYNAMIC_PROPERTY, "")
        slot_string = "defaultThemeAction." + "triggered" + ".connect(" + "self.on_ThemeActionTriggered" + ")"
        exec(slot_string)
        themesMenu.addAction(defaultThemeAction)
        themes_dir = (QDir(THEMES_SUBFOLDER))
        theme_files = themes_dir.entryInfoList(QDir.NoDotAndDotDot | QDir.Files, QDir.Name)
        for theme in theme_files:
            theme_filename = theme.fileName()
            themeAction = QAction(theme_filename, self)
            themeAction.setProperty(FILE_ON_DISK_DYNAMIC_PROPERTY, theme.absoluteFilePath())
            # QStyle.SP_DriveDVDIcon
            slot_string = "themeAction." + "triggered" + ".connect(" + "self.on_ThemeActionTriggered" + ")"
            exec(slot_string)
            themesMenu.addAction(themeAction)
            if current_theme_file == theme.absoluteFilePath():
                print("themeAction self-trigger")
                themeAction.trigger()
        self.ui.actionTheme.setMenu(themesMenu)


    def on_actionAboutQt_triggered(self):
        QApplication.instance().aboutQt()
        QMessageBox.about(self, "About Computer Vision",
                          """<b>Computer Vision</b> v %s
                          <p>Copyright &copy; 2019.
                          All rights reserved.
                          <p>This application can be used to perform
                          image manipulations.
                          <p>Python %s - Qt %s
                          - PyQt %s on %s """ % (__version__,
                                                 platform.python_version(),
                                                 QApplication.instance().QT_VERSION_STR,
                                                 QApplication.instance().PYQT_VERSION_STR,
                                                 platform.system()))
        # print("about not yet implemented")
        # return

    def on_actionExit_triggered(self):
        self.close()

    def on_PluginActionTriggered(self):
        print("on_PluginActionTriggered")

        if not self.current_plugin_file == "":
            print("self.current_plugin_file: ", "x" + self.current_plugin_file + 'x')
            self.current_plugin_file = ""
            print("before count: ", self.ui.pluginLayout.count())
            while self.ui.pluginLayout.count():
                print("while loop was run")
                item = self.ui.pluginLayout.takeAt(0)
                item.widget().deleteLater()
            # self.ui.pluginLayout.deletelater  addWidget(self.currentPluginGui)
            print("after count: ", self.ui.pluginLayout.count())
            # self.current_PluginGui.delete()
            # print("current_pluginGui was deleted")
            print("old current_plugin_file: ", self.current_plugin_file)


        self.current_plugin_file = self.sender().property(FILE_ON_DISK_BASENAME_PROPERTY)
        print("new current_plugin_file: ", self.current_plugin_file)
        import_string = "import " + PLUGINS_SUBFOLDER + self.current_plugin_file + " as PI"
        print(import_string)
        exec(import_string, globals())
        # import cvplugins.copymakeborder_plugin as PI
        # import cvplugins.pi_copy_make_border as PI
        # import cvplugins.pi_copy_make_border
        print("import plugin statement run")

        # self.currentPlugin = pi.CopyMakeBorder_Plugin

        self.currentPluginGui = PI.Plugin()
        self.ui.pluginLayout.addWidget(self.currentPluginGui)
        self.currentPluginGui.setupUi(self.currentPluginGui)
        self.currentPluginGui.updateNeeded.connect(self.on_current_plugin_update_needed)
        self.currentPluginGui.infoMessage[str].connect(self.on_current_plugin_info_message)
        self.currentPluginGui.errorMessage[str].connect(self.on_current_plugin_error_message)

    def on_LanguageActionTriggered(self):
        print("on_LanguageAction_triggered")

    def on_ThemeActionTriggered(self):
        print("on_ThemeActionTriggered")
        current_theme_file = self.sender().property(FILE_ON_DISK_DYNAMIC_PROPERTY)
        print('current_theme_file:', current_theme_file)
        if current_theme_file == "":
            QApplication.instance().setStyleSheet("")

        else:
            theme_file = QFile(current_theme_file)
            theme_file.open(QFile.ReadOnly | QFile.Text)
            stream = QTextStream(theme_file)
            QApplication.instance().setStyleSheet(stream.readAll())
            theme_file.close()

    def on_actionOpenImage_triggered(self):
        print('on_actionOpenImage_triggered')

        # dirname = os.path.dirname(self.filename) \
        #     if self.filename is not None else "../images"
        dirname = "../images"
        formats = ["Images PNG (*.png);;Jpeg (*.jpg *.jpeg);;Targa (*.tga);;SVG (*.svg)"]
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.filename, e_filter = QFileDialog.getOpenFileName(self, caption="Choose image file to open",
                                                   directory=dirname,
                                                   filter=formats[0], options=options)
        if self.filename:
            print(self.filename)
            print(e_filter)
            self.originalMat = cv.imread(self.filename)

        if self.originalMat is None:
            QMessageBox.critical(self,
                                 "Error",
                                 "Make sure the image file exists "
                                 "and it is accessible!")
        else:
            self.on_current_plugin_update_needed()

    def on_viewOriginalCheck_toggled(self, checked):
        print("on_view_original_check_toggled -- called")
        if self.ui.viewOriginalCheck == True:
            print(checked)
        else:
            print(checked)

        self.originalPixmap.setVisible(checked)
        self.processedPixmap.setVisible(not checked)

    def on_current_plugin_update_needed(self):
        print("on_current_plugin_update_needed called")
        if not (self.originalMat is None):
            print("originalMat exists")
            self.processedMat = self.originalMat.copy()
        # else:
        if not self.currentPluginGui is None:
            print("starting to time process")
            print(type(self.currentPlugin))
            meter = cv.TickMeter()
            meter.start()
            self.processedMat = self.currentPluginGui.process_image(self.originalMat, self.processedMat)
            meter.stop()
            print("The process took ", meter.getTimeMilli(), " milliseconds")
            # cv.imshow("processed:", self.processedMat)
            # cv.imshow("original:", self.originalMat)
            # cv.waitKey(0); cv.destroyAllWindows()
        self.originalImage = QImage(self.originalMat.data,
                                    self.originalMat.shape[1],
                                    self.originalMat.shape[0],
                                    QImage.Format_RGB888)
        temp_original_pixmap = QPixmap.fromImage(self.originalImage.rgbSwapped())
        self.originalPixmap.setPixmap(temp_original_pixmap)
        # self.originalPixmap.fromImage(self.originalImage.rgbSwapped())
        print(type(self.originalPixmap))
        self.processedImage = QImage(self.processedMat.data,
                                     self.processedMat.shape[1],
                                     self.processedMat.shape[0],
                                     QImage.Format_RGB888)
        temp_processed_pixmap = QPixmap.fromImage(self.processedImage.rgbSwapped())
        self.processedPixmap.setPixmap(temp_processed_pixmap)
        print("last line completed")
        return

    def on_actionSaveImage_triggered(self):
        print('on_action_SaveImage_triggered')
        fname = self.get_save_filename()
        print("filename to save to: ", fname)
        if (fname != "") and (fname != "."):
            print("original not checked", not self.ui.viewOriginalCheck.isChecked())
            print("processedMat exists", self.processedMat is not None)
            if (not self.ui.viewOriginalCheck.isChecked()) and self.processedMat is not None:
                cv.imwrite(fname, self.processedMat)
                print("wrote processed to file:", fname)
            else:
                print("view original is checked", self.ui.viewOriginalCheck.isChecked())
                print("original exists", not(self.originalMat is None))
                if (self.ui.viewOriginalCheck.isChecked()) and (self.originalMat is not None):
                    print("fname:", fname)
                    status = cv.imwrite(fname, self.originalMat)
                    print("Wrote original to file:", fname)
                    print(status)

            self.filename = fname
        else:
            result = QMessageBox.warning(self,
                                "Warning",
                                "There is nothing to be saved!",
                                QMessageBox.Ok,
                                         QMessageBox.Ok)
            print("result:", result)
            if result == QMessageBox.Ok:
                return

            #     return

    def get_save_filename(self):
        fname = self.filename if self.filename is not None else "."

        formats = ["Images PNG (*.png);;Jpeg (*.jpg *.jpeg);;Targa (*.tga);;SVG (*.svg)"]
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fname, mask = QFileDialog.getSaveFileName(None, caption="Choose name to save as",
                                                  directory=fname,
                                                  filter=formats[0], options=options)
        print(fname)
        print(mask)
        if fname:
            if "." not in fname:
                fname += ".png"
                # self.add_recent_file(fname)
            return fname
        else:
            return ""

    def on_current_plugin_error_message(self, msg):
        print("Plugin Error Message: ", msg)

    def on_current_plugin_info_message(self, msg):
        print("Plugin Info Message: ", msg)

    def on_action_Camera_triggered(self):
        print("on_action_camera_triggered - not implemented")




