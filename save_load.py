"""
This module provides functions for saving, loading, and deleting
PC build configurations using a JSON file for storage.

Data is stored in a dictionary format where their keys are build names (strings),
and values are build configurations (dictionaries)

Functions in this module handle file creation, reading, updating,
and deletion of saved builds.
"""

import json
import os

SAVE_FILE = "saved_builds.json"


def load_all_builds():
    """
    Load all saved builds from the JSON file.

    If the save file doesn't exist, an empty dictionary is returned.

    Returns:
        dict: A dictionary containing all saved builds.
    """

    if not os.path.exists(SAVE_FILE):
        return {}

    with open(SAVE_FILE, "r") as f:
        return json.load(f)


def save_build(name, build):
    """
    Save a build configuration under a given name.
    If a build with the same name already exists, it will be overwritten.

    Args:
        name (str): The name of the build.
        build (dict): The build configuration to save.

    Returns:
        None
    """
    data = load_all_builds()
    data[name] = build

    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)


def load_build(name):
    """
    Retrieve a specific build by name.

    Args:
        name (str): The name of the build we want to load.

    Returns:
        dict or None: The build configuration if found, otherwise None.
    """
    data = load_all_builds()
    return data.get(name)


def delete_build(name):
    """
    Delete a saved build by name.

    If the build exists, it is removed from storage and the file is updated.
    If the build does not exist, no action is taken.

    Args:
        name (str): The name of the build to delete.

    Returns:
        None
    """
    data = load_all_builds()
    if name in data:
        del data[name]
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=4)
