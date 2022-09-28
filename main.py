from PyQt5 import QtCore, QtGui, QtWidgets
from pytube import YouTube
from window import Ui_ADV
from yt import *

import config
from downloader import *
from message_window import *

import os
import sys
import pyperclip

os.system("pyuic5 design.ui -o window.py")
os.system("pyuic5 video.ui -o videoWindow.py")

class Window(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(Window, self).__init__()
        self.ui = Ui_ADV()
        self.ui.setupUi(self)

        self.ui.pasteLinkButton.clicked.connect(self.paste_link)
        config.setup_config()

        self.ui.debugField.setText(utils.get_videos_list())

    def paste_link(self):
        link = pyperclip.paste()

        if link.startswith("https://youtu.be") or link.startswith("https://www.youtube.com/"):
            self.ui.linkText.setText(f"Link: {link}")
            self.ui.pasteLinkButton.setEnabled(False)
            self.ui.progressBar.setMaximum(0)

            self.streamsworker = YT_GetData(link)
            self.streamsworker.start()
            self.streamsworker.data.connect(self.download)
            self.streamsworker.finished.connect(self.download_ended)

        else:
            create_error("Invalid link")

    def download(self, data: tuple):
        yt, ytStreams, link, err = data
        #print(data)
        if err:
            self.ui.progressBar.setMaximum(1)
            self.ui.pasteLinkButton.setEnabled(True)
            create_error("Something went wrong...")

        else:
            self.downloadDialog = DownloadDialog(data)
            self.downloadDialog.show()
            pass

    def download_ended(self):
        self.streamsworker.quit()
        self.ui.progressBar.setMaximum(1)
        self.ui.pasteLinkButton.setEnabled(True)

        self.ui.linkText.setText("")
        self.ui.debugField.setText(utils.get_videos_list())

app = QtWidgets.QApplication([])
application = Window()
application.show()
sys.exit(app.exec())


#subprocess.run(f"ffmpeg -i {FILENAME} -vcodec libx264 -acodec aac -t 30 {file}.mp4")
