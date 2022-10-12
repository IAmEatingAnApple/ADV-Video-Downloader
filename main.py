from PyQt5 import QtCore, QtGui, QtWidgets
from pytube import YouTube
from window import Ui_ADV
from widget import VideoWidget
from yt import *

import config
from downloader import *
from message_window import *

import os
import sys
import pyperclip

if utils.exists("design2.ui"):
    os.system("pyuic5 design2.ui -o window.py")
    os.system("pyuic5 video.ui -o videoWindow.py")
    os.system("pyuic5 videoWidget.ui -o videoWidget.py")

class Window(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(Window, self).__init__()
        self.ui = Ui_ADV()
        self.ui.setupUi(self)

        self.ui.pasteLinkButton.clicked.connect(self.paste_link)

        self.update_history()

        config.setup_config()

    def update_history(self):
        if utils.exists("history.json"):
            history = utils.get_history()

            while self.ui.widget_layout.count() > 0:
                self.ui.widget_layout.takeAt(0).widget().deleteLater()

            for item in history:
                self.ui.widget_layout.addWidget(VideoWidget(
                    video_title=item['video_title'],
                    video_id=item['video_id'],
                    video_path=item['video_path']
                ))

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
            self.downloadDialog.finished.connect(lambda: self.update_history())
            self.downloadDialog.show()

    def download_ended(self):
        self.streamsworker.quit()
        self.ui.progressBar.setMaximum(1)
        self.ui.pasteLinkButton.setEnabled(True)

        self.ui.linkText.setText("")
        #self.ui.debugField.setText(utils.get_videos_list())

app = QtWidgets.QApplication([])
application = Window()
application.show()
sys.exit(app.exec())
