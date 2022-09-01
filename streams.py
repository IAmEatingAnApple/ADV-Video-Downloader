from PyQt5.QtCore import QThread, pyqtSignal
from pytube import YouTube

class Worker(QThread):
    data = pyqtSignal(tuple)

    def __init__(self, link):
        super(QThread, self).__init__()
        
        self.link = link

    def run(self):
        print("getting", self.link)
        try:
            yt = YouTube(self.link)

            self.data.emit((yt, yt.streams, False)) #yt, streams, err
        except:
            self.data.emit((None, None, True))