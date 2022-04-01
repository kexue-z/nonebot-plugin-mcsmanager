from pathlib import Path

import yaml

FILE_DIR = (Path() / "data" / "mc").absolute()


def get_yaml_file(FILE_DIR=FILE_DIR) -> dict:
    FILE = FILE_DIR / "mcsm.yaml"
    if FILE.exists():
        with FILE.open("r", encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.BaseLoader)
        return data["mcsm"]
    else:
        data = {"mcsm": {}}
        FILE_DIR.mkdir()
        with open(FILE, "w+", encoding="utf-8") as f:
            yaml.dump(data, f)
        return data


def write_yaml_file(data, FILE_DIR=FILE_DIR) -> None:
    FILE = FILE_DIR / "mc.yaml"
    with open(FILE, "w+", encoding="utf-8") as f:
        yaml.dump(data, f)
