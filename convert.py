from importlib.resources import path
from PyQt5.QtCore import QThread, pyqtSignal
import ffmpeg
from proglog import ProgressBarLogger
from math import floor
import os
import utils

class Converter(QThread):
    finished = pyqtSignal()

    def __init__(self, save_folder, title, to_h264):
        super(QThread, self).__init__()
        self.save_folder = save_folder
        self.title = title
        self.to_h264 = to_h264

    def run(self):
        video = ffmpeg.input(self.save_folder + "/temp_" + self.title + ".mp4").video
        audio = ffmpeg.input(self.save_folder + "/temp_" + self.title + ".mp3").audio

        vcodec = "h264" if self.to_h264 else "copy"

        ffmpeg.output(
            video,
            audio,
            self.save_folder + "/" + self.title + ".mp4",
            vcodec=vcodec,
            acodec='aac'
        ).run()

        
        utils.remove_temp(self.save_folder, self.title)

        self.finished.emit()

    class MyBarLogger(ProgressBarLogger, QThread):
        percent = pyqtSignal(int)
        def bars_callback(self, bar, attr, value, old_value):  
            percentage = floor((value / self.bars[bar]['total']) * 100)
            self.percent.emit(percentage)

