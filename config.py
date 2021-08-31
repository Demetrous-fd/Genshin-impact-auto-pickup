from pathlib import Path
import json


PATH_CONFIG = Path(Path(__file__).parent.absolute(), "config.json")
DEFAULT_CONFIG = {
    "Target": "CPU",
    "FPS": 5,
    "Click rate": "Normal",
    "Key": "F"
}


def default_config():
    write_config(DEFAULT_CONFIG)


def read_config():
    with open(PATH_CONFIG) as file:
        return json.loads(file.read())


def write_config(config):
    with open(PATH_CONFIG, "w") as file:
        file.write(json.dumps(config, indent=4))


def update_config(key, value):
    config = read_config()
    config[key] = value

    write_config(config)


if not PATH_CONFIG.exists():
    default_config()
    print("Create config")


if __name__ == '__main__':
    print("Default config:", read_config())

    update_config("Target", "CUDA")
    update_config("FPS", 0)
    update_config("Click rate", "Fast")
    print("Config after update: ", read_config())
