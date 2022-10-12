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
    finished = pyqtSignal()

    def __init__(self, data: tuple):
        super(DownloadDialog, self).__init__()
        self.ui = Ui_Download()
        self.ui.setupUi(self)

        self.ui.browseButton.clicked.connect(self.choose_folder)
        self.ui.downloadButton.clicked.connect(self.start_download)

        self.yt, self.ytStreams, self.link, self.err = data
        #self.highestRes: Stream = utils.get_highest_resolution(self.ytStreams)
        #self.streams = utils.get_extension_streams(self.ytStreams, "mp4")
        self.streams = self.ytStreams
        self.streamslist = utils.get_streams_list(self.streams)

        for item in self.streamslist:
            self.ui.resolutionBox.addItem(item[0], item[1])

        #print("\n", self.streams)
        #print(self.highestRes)
        #self.videosize = self.highestRes.filesize

        title = self.yt.title
        if len(title) >= 50:
            title = title[:50] + "..."

        cfg = config.get_config()
        self.save_folder = cfg['save_folder']
        
        self.ui.videoTitleLabel.setText("Title: " + title)
        self.ui.authorLabel.setText("Channel: " + self.yt.author)
        #self.ui.sizeLabel.setText("Size: " + str(self.highestRes.filesize_approx//1024//1024) + " MB")

        self.ui.lineEdit.setText(self.save_folder)

    def choose_folder(self):
        self.save_folder = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.ui.lineEdit.setText(self.save_folder)

    def start_download(self):
        config.update_config("save_folder", self.ui.lineEdit.text())

        self.ui.downloadButton.setEnabled(False)
        self.ui.browseButton.setEnabled(False)
        self.ui.convertBox.setEnabled(False)
        
        index = self.ui.resolutionBox.currentIndex()
        itag = self.ui.resolutionBox.itemData(index)

        to_h264 = self.ui.convertBox.isChecked()

        self.downloadWorker = YT_DownloadVideo(itag, self.save_folder, self.link, to_h264)
        self.downloadWorker.start()
        self.downloadWorker.finished.connect(self.download_ended)
        self.downloadWorker.percent.connect(self.set_progress)
        self.downloadWorker.status.connect(self.set_status)

    def set_progress(self, percent):
        #print("jkshdbfkjdhzsxbf")
        self.ui.loadingBar.setValue(percent)

    def set_status(self, status):
        self.ui.browseButton.setText(status)

    def download_ended(self):
        self.downloadWorker.quit()
        create_info("Download ended!")
        self.finished.emit()
        self.close()