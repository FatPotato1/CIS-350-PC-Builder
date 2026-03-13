import components
import csv
import re

#load all data from our game settings csv
def load_games():
    games = []

    with open("pc_game_settings.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["min_gpu_model"] = extract_gpu_model(row["min_gpu"])
            row["rec_gpu_model"] = extract_gpu_model(row["rec_gpu"])
            games.append(row)

    return games

#used chatgpt to figure out how to do python regexes because naming is inconsistent between different csvs
def extract_gpu_model(name):
    name = name.lower()
    match = re.search(r'(rtx|gtx|rx|hd)\s?\d{3,4}', name)
    if match:
        return match.group()
    return None


#get ranking of each gpu
def load_gpu_rankings():
    rankings = {}

    with open("GPU_UserBenchmarks.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            identifier = extract_gpu_model(row["Model"])

            if identifier:
                score = int(row["Rank"])
                rankings[identifier] = score

    return rankings


print(load_gpu_rankings())
print(load_games())