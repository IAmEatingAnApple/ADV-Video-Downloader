from importlib.resources import path
from PyQt5.QtCore import QThread, pyqtSignal
from better_ffmpeg_progress import FfmpegProcess
import ffmpeg
from proglog import ProgressBarLogger
from math import floor
import os
import utils

class Converter(QThread):
    finished = pyqtSignal()
    percent = pyqtSignal(int)

    def __init__(self, save_folder, title, to_h264):
        super(QThread, self).__init__()
        self.save_folder = save_folder
        self.title = title
        self.to_h264 = to_h264

    def run(self):
        video_path = self.save_folder + "/temp_" + self.title + ".mp4"
        audio_path = self.save_folder + "/temp_" + self.title + ".mp3"

        video = ffmpeg.input(self.save_folder + "/temp_" + self.title + ".mp4").video
        audio = ffmpeg.input(self.save_folder + "/temp_" + self.title + ".mp3").audio

        vcodec = "h264" if self.to_h264 else "copy"

        process = FfmpegProcess(["ffmpeg", "-i", video_path, "-i", audio_path, "-vcodec", vcodec, "-acodec", "aac", self.save_folder + "/" + self.title + ".mp4"])
        process.run(progress_handler=self.handle_progress_info)
        
        utils.remove_temp(self.save_folder, self.title)

        self.finished.emit()

    def handle_progress_info(self, percentage, speed, eta, estimated_filesize):
        self.percent.emit(floor(percentage))