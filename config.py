import yaml
import utils

def setup_config():
    utils.create_file_if_not_exists("config.yml")

    if utils.is_empty('config.yml'):
        videos_folder = utils.get_videos_folder()
        with open('config.yml', "w") as f:
            yaml.dump(
                {
                    "save_folder": videos_folder
                }, f)

def get_config():
    with open('config.yml', 'r') as f:
        return yaml.safe_load(f)

def update_config(key, content):
    parsed = get_config()
    parsed[key] = content

    with open('config.yml', "w") as f:
        yaml.dump(parsed, f)