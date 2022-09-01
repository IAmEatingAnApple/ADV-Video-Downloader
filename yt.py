from os import link
from pytube import YouTube, Stream
from PyQt5.QtCore import QThread, pyqtSignal
import config

class YT_GetData(QThread):
    percent = pyqtSignal(int)
    data = pyqtSignal(tuple)

    def __init__(self, link: str = None):
        super(QThread, self).__init__()
        self.link = link

    def run(self):
        try:
            print("getting", self.link)
            yt = YouTube(self.link)

            streams = yt.streams

            self.data.emit((yt, yt.streams, self.link, False))

        except Exception as e:
            print(e)
            self.data.emit((None, None, None, True))

class YT_DownloadVideo(QThread):
    percent = pyqtSignal(int)

    def __init__(self, stream: Stream = None, save_folder: str = None, link: str = None):
        super(QThread, self).__init__()
        self.stream = stream
        self.save_folder = save_folder
        self.link = link
        print(self.__dict__)

    def run(self):
        yt = YouTube(self.link)
        yt.register_on_progress_callback(self.progress)

        itag = self.stream.itag
        s = yt.streams.get_by_itag(itag)
        s.download(self.save_folder, skip_existing=False)

    def progress(self, stream, chunk, bytes_remaining):
        perc = int(100 * (stream.filesize - bytes_remaining) // stream.filesize)
        print(perc)
        self.percent.emit(perc)