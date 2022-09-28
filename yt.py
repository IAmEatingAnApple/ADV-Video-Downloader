from os import link
from pytube import YouTube, Stream
from PyQt5.QtCore import QThread, pyqtSignal
from convert import Converter
import re
import config
import utils

class YT_GetData(QThread):
    data = pyqtSignal(tuple)

    def __init__(self, link: str = None):
        super(QThread, self).__init__()
        self.link = link

    def run(self):
        try:
            print("getting", self.link)
            yt = YouTube(self.link)

            streams = yt.streams.filter(progressive=None, only_video=True)
            #for i in yt.streams:
                #print(i)
            self.data.emit((yt, streams, self.link, False))

        except Exception as e:
            print(e)
            self.data.emit((None, None, None, True))

class YT_DownloadVideo(QThread):
    percent = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, itag: int = None, save_folder: str = None, link: str = None, to_h264:bool = False):
        super(QThread, self).__init__()
        self.itag = itag
        self.save_folder = save_folder
        self.link = link
        self.to_h264 = to_h264

    def run(self):
        self.status.emit("Fetching")

        yt = YouTube(self.link)
        yt.register_on_progress_callback(self.progress)

        title = re.sub('[^A-Za-z0-9]+', '_', yt.title)

        video_stream = yt.streams.get_by_itag(self.itag)
        #print(s)

        self.status.emit("Downloading")
        video_stream.download(self.save_folder, filename=f"temp_{title}.mp4", skip_existing=False)

        self.percent.emit(0)
        audio_stream = yt.streams.get_audio_only()

        self.status.emit("Audio")
        audio_stream.download(self.save_folder, filename=f"temp_{title}.mp3", skip_existing=False)

        self.status.emit("Converting")

        self.convertWorker = Converter(self.save_folder, title, self.to_h264)
        self.convertWorker.finished.connect(self.download_ended)
        self.convertWorker.start()

        #self.download_ended()

    def send_percent(self, perc):
        self.percent.emit(perc)

    def download_ended(self):
        self.finished.emit()

    def progress(self, stream, chunk, bytes_remaining):
        perc = int(100 * (stream.filesize - bytes_remaining) // stream.filesize)
        self.percent.emit(perc)