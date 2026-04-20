import json
import os

SAVE_FILE = "saved_builds.json"


def load_all_builds():
    if not os.path.exists(SAVE_FILE):
        return {}

    with open(SAVE_FILE, "r") as f:
        return json.load(f)


def save_build(name, build):
    data = load_all_builds()
    data[name] = build

    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)


def load_build(name):
    data = load_all_builds()
    return data.get(name)


def delete_build(name):
    data = load_all_builds()
    if name in data:
        del data[name]
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=4)
