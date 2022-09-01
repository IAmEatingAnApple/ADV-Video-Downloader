from pytube import YouTube, Stream
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from videoWindow import Ui_Download
from message_window import *

import config
import utils
import math

from yt import YT_DownloadVideo

class DownloadDialog(QtWidgets.QMainWindow):
    def __init__(self, data: tuple):
        super(DownloadDialog, self).__init__()
        self.ui = Ui_Download()
        self.ui.setupUi(self)

        self.ui.browseButton.clicked.connect(self.choose_folder)
        self.ui.downloadButton.clicked.connect(self.start_download)

        self.yt, self.ytStreams, self.link, self.err = data
        self.highestRes: Stream = utils.get_highest_resolution(self.ytStreams)
        self.videosize = self.highestRes.filesize

        title = self.yt.title
        if len(title) >= 50:
            title = title[:50] + "..."

        cfg = config.get_config()
        self.save_folder = cfg['save_folder']
        
        self.ui.videoTitleLabel.setText("Title: " + title)
        self.ui.authorLabel.setText("Channel: " + self.yt.author)
        self.ui.resolutionLabel.setText("Highest resolution: " + self.highestRes.resolution)
        self.ui.fpsLabel.setText("FPS: " + str(self.highestRes.fps))

        self.ui.lineEdit.setText(self.save_folder)

    def choose_folder(self):
        self.save_folder = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.ui.lineEdit.setText(self.save_folder)

    def start_download(self):
        config.update_config("save_folder", self.ui.lineEdit.text())

        self.downloadWorker = YT_DownloadVideo(self.highestRes, self.save_folder, self.link)
        self.downloadWorker.start()
        self.downloadWorker.finished.connect(self.download_ended)
        self.downloadWorker.percent.connect(self.set_progress)

    def set_progress(self, percent):
        #print("jkshdbfkjdhzsxbf")
        self.ui.loadingBar.setValue(percent)

    def download_ended(self):
        self.downloadWorker.quit()
        create_info("Download ended!")
        self.close()