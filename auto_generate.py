import components
from data_loading import load_games, load_gpu_rankings

# generate a list of parts for pc based on selected game and either min or recommended specs
# this should be able to be modified somewhat easily to include amd gpus, all cpus, etc


def generate_pc(game_name, target_performance, game_list, cpu_rankings, gpu_rankings, cpu_brand, gpu_brand):

    return (generate_gpu(game_name, target_performance, game_list, gpu_rankings, gpu_brand),
            generate_cpu(game_name, target_performance, game_list, cpu_rankings, cpu_brand))


def generate_cpu(game_name, target_performance, game_list, rankings, cpu_brand):

    selected_cpu = None
    selected_score = None
    # list of cpus from components
    if cpu_brand == "Intel":

def generate_ram():
    pass

def generate_storage():
    pass

# needs to be modified to include amd gpus, currently data loader regex only does nvidia cards
def generate_gpu(game_name, target_performance, game_list, rankings, gpu_brand):

    selected_gpu = None
    selected_score = None
    # list of gpus from components
    if gpu_brand == "NVIDIA":

        gpus = components.hardware.get("NVIDIA GPUs", [])
    else:
        gpus = components.hardware.get("AMD GPUs", [])

    game = None

    # find the game in list
    for x in game_list:
        if x["game_name"] == game_name:
            game = x
            break
    if target_performance == "rec":
        required_gpu_model = game["rec_gpu_model"]

    else:
        required_gpu_model = game["min_gpu_model"]

    # the ranking from GPU_UserBenchmarks that the picked GPU must beat
    required_score = rankings.get(required_gpu_model)

    #TODO: some gpus either are not in list or not formatted right, probably should be fixed sometime
    # one of them is minecraft on min settings
    if required_score is None:
        print("GPU not in parts list")
        return None

    # logic to cheapest gpu that meets recs
    for gpu in gpus:
        gpu_name = gpu.lower()
        gpu_score = rankings.get(gpu_name)
        if gpu_score is None:
            continue
        if gpu_score <= required_score:
            if selected_score is None or gpu_score > selected_score:
                selected_gpu = gpu
                selected_score = gpu_score

    return selected_gpu
