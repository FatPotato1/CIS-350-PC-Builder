"""
The purpose of this module is to load information regarding loading games, extracting gpu models, loading and extracting
GPU and CPU models.

Authors: Dorian Lawton, Justin Hanko, Landon Jurmo and Jaykin Hang
Date: April 24, 2026
Version: Python 3.12
"""
import components
import csv
import re

# load all data from game settings csv


def load_games():
    """
    Loads game requirement data from a CSV that reads information for CPU and GPU models.

    Returns:
        games (list[dict]): A list of dictionaries where each dictionary outputs a game and its CPU and GPU models.
    """
    games = []

    with open("pc_game_settings.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # new rows are created in list in order to make sure names match the fields in the other CSV
            row["min_gpu_model"] = extract_gpu_model(row["min_gpu"].strip())
            row["rec_gpu_model"] = extract_gpu_model(row["rec_gpu"].strip())
            row["min_cpu_model"] = extract_cpu_model(row["min_cpu"].strip())
            row["rec_cpu_model"] = extract_cpu_model(row["rec_cpu"].strip())
            games.append(row)

    return games

# used chatgpt to generate python regexes because data is pretty inconsistent between different csvs
# regex is used to make sure data is comparable and normalized


def extract_gpu_model(name):
    """
    Extracts the GPU model name.

    Args:
        name (str): GPU name
    Returns:
        str or None: GPU model or None if GPU model string is not found
    """
    name = name.lower().strip().replace("-", " ").replace("ti", " ti")
    match = re.search(r'(rtx|gtx|rx|hd|gt)\s?\d{3,4}\s?(ti)?', name)
    if match:
        return match.group().replace("  ", " ").strip()
    return None


# get ranking of each gpu


def load_gpu_rankings():
    """
    Loads GPU performance rankings from a CSV file.

    Returns:
        dict[str, int]: A dictionary mapping GPUs to their rank
    """
    rankings = {}

    with open("GPU_UserBenchmarks.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            #only get entries that line up with regex
            identifier = extract_gpu_model(row["Model"].strip())

            if identifier:
                score = int(row["Rank"])
                rankings[identifier] = score

    return rankings


def extract_cpu_model(name):
    """
    Extracts the CPU model name.

    Args:
        name (str): CPU name
    Returns:
        str: CPU model
        None: returned if CPU model string is not found
    """
    name = name.lower().strip().replace("-", " ")

    match = re.search(
        r'(i[3579]\s?\d{4,5}[a-z]*|ryzen\s?[3579]\s?\d{3,5}[a-z]*|fx\s?\d{4}|athlon\s?\d{3,4})',
        name
    )

    if match:
        return match.group().replace("  ", " ").strip()
    return None

def load_cpu_rankings():
    """
    Loads CPU performance rankings from a CSV file.

    Returns:
        dict[str, int]: A dictionary mapping CPUs to their rank
    """
    rankings = {}

    with open("CPU_UserBenchmarks.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            identifier = extract_cpu_model(row["Model"].strip())

            if identifier:
                score = int(row["Rank"])
                rankings[identifier] = score
    return rankings
