from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap

from videoWidget import Ui_Widget

import subprocess

class VideoWidget(QWidget):
    def __init__(self, video_title, video_id, video_path):
        super(VideoWidget, self).__init__()
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        self.video_path = video_path.replace("/", "\\")

        self.ui.titleLabel.setText(video_title)
        self.ui.pushButton.clicked.connect(self.show_file)
        self.ui.thumbnailLabel.setPixmap(QPixmap(f"thumbs/{video_id}.jpg"))

    def show_file(self):
        subprocess.Popen(f"explorer.exe /select, \"{self.video_path}\"")