import os
import json

CONFIG_PATH = 'configs/'


def get_cameras():
    with open(os.path.join(CONFIG_PATH, 'location_config.json'), 'r') as f:
        cameras = json.load(f)
    return cameras