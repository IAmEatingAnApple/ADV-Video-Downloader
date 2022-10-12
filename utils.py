import os

from matplotlib.streamplot import StreamplotSet
import config
import subprocess
import requests
import json

from image_process import crop_thumbnail
from pytube import Stream, StreamQuery
from math import floor

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

def create_dir_if_not_exists(path):
    if not exists(path):
        os.mkdir(path)

def create_history_file():
    create_file_if_not_exists("history.json")

    with open("history.json", "w", encoding="utf-8") as f:
        data = """
[
    
]"""
        f.write(data)

def get_videos_list():
    res = ""
    counter = 1

    for item in os.listdir(config.get_config()['save_folder']):
        res += f"{counter}. {item}\n"
        counter += 1
    
    return res

def get_codec_streams(streams: Stream, codec: str):
    streamslist = []
    for item in streams:
        if codec.lower() in item.codecs[0]:
            streamslist.append([f"{item.resolution}{item.fps} | {codec}", item.itag])

    return streamslist

def get_streams_list(streams: Stream):
    streamslist = []
    for item in streams:
        codec = ""

        if "avc1" in item.codecs[0]:
            codec = "AVC"
        elif "av01" in item.codecs[0]:
            codec = "AV01"
        else:
            codec = "VP9"
        
        streamslist.append([f"{item.resolution}{item.fps} | {codec}", item.itag])

    #for item in streamslist:
        #print(item)

    return streamslist

def get_codecs_list(streams: Stream):
    codeclist = []

    for item in streams:
        codec = ""

        if "avc1" in item.codecs[0]:
            codec = "AVC"
        elif "av01" in item.codecs[0]:
            codec = "AV01"
        else:
            codec = "VP9"

        if codec not in codeclist:
            codeclist.append(codec)

    return codeclist

def calculate_video_size(bitrate: int, length: float):
    print(bitrate)
    print(length)
    return floor(bitrate * length * 0.005)

def remove_if_exists(path: str):
    if exists(path):
        os.remove(path)

def remove_temp(save_folder: str, filename: str):
    remove_if_exists(f"{save_folder}/temp_{filename}.mp4")
    remove_if_exists(f"{save_folder}/temp_{filename}.mp3")

def download_thumbnail(thumbnail_url: str):
    r = requests.get(thumbnail_url)
    video_id = get_video_id(thumbnail_url)

    create_dir_if_not_exists("thumbs")
    with open(f"thumbs/{video_id}.jpg", "wb") as f:
        f.write(r.content)

    crop_thumbnail(f"thumbs/{video_id}.jpg")

def get_video_id(url: str):
    return url.split("/")[-2]

def add_to_history(video_title, video_id, video_path):
    if not exists("history.json"):
        create_history_file()

    with open("history.json", "r+", encoding="utf-8") as f:
        file_data = json.load(f)

        data = {
            "video_title":video_title,
            "video_id":video_id,
            "video_path":video_path
        }

        file_data.insert(0, data)
        f.seek(0)

        json.dump(file_data, f, indent=2)

def get_history():
    with open("history.json", "r", encoding="utf-8") as f:
        j = json.load(f)

    return j