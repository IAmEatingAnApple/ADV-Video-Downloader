import os
import config
from pytube import Stream, StreamQuery

def get_videos_folder():
    return os.getenv("SYSTEMDRIVE") + os.getenv("HOMEPATH") + "\Videos"

def is_empty(file):
    if os.stat(file).st_size == 0:
        return True
    else:
        return False

def exists(file):
    if os.path.exists(file):
        return True
    return False

def create_file_if_not_exists(file):
    if not exists(file):
        open(file, "w").close()

def get_videos_list():
    res = ""
    counter = 1

    for item in os.listdir(config.get_config()['save_folder']):
        res += f"{counter}. {item}\n"
        counter += 1
    
    return res

def get_extension_streams(streams: Stream, ext: str):
    streamslist = []
    for item in streams:
        if ext in item.mime_type:
            streamslist.append(item)

    return streamslist

def get_streams_list(streams: Stream):
    streamslist = []
    for item in streams:
        streamslist.append([f"{item.resolution}{item.fps} | {item.codecs[0]}", item.itag])

    #for item in streamslist:
        #print(item)

    return streamslist

def remove_temp(path: str, filename: str):
    os.remove(f"{path}/temp_{filename}.mp4")
    os.remove(f"{path}/temp_{filename}.mp3")