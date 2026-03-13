import components
import csv
import re

#load all data from game settings csv
def load_games():
    games = []

    with open("pc_game_settings.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # new rows are created in list in order to make sure names match the fields in the other CSV
            row["min_gpu_model"] = extract_gpu_model(row["min_gpu"])
            row["rec_gpu_model"] = extract_gpu_model(row["rec_gpu"])
            games.append(row)

    return games

#used chatgpt to figure out how to do python regexes because naming is inconsistent between different csvs
#regex is used to make sure data is comparable and normalized
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
            #only get entries that line up with regex
            identifier = extract_gpu_model(row["Model"])

            if identifier:
                score = int(row["Rank"])
                rankings[identifier] = score

    return rankings


print(load_gpu_rankings())
print(load_games())