import os
import config
from pytube import Stream

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

# Get real highest video quality cuz pytube is shit
def get_highest_resolution(streams: Stream):
    highestRes = 0
    highestStream = None
    for item in streams:
        try:
            q = int(item.resolution[:-1])
            if q > highestRes:
                highestRes = q
                highestStream = item
        except:
            pass

    return highestStream