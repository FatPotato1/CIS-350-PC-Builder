import components
from data_loading import load_games, load_gpu_rankings

#generate a list of parts for pc based on selected game and either min or recommended specs
def generate_pc(game_name, target_performance, game_list, rankings):
    selected_gpu = None
    selected_score = None
    #list of gpus from components
    gpus = components.hardware.get("NVIDIA GPUs", [])
    game = None
    required_gpu_model = ""

    #find the game in list
    for x in game_list:
        if x["game_name"] == game_name:
            game = x
            break
    if target_performance == "rec":
        required_gpu_model = game["rec_gpu_model"]

    else:
        required_gpu_model = game["min_gpu_model"]

    #the ranking from GPU_UserBenchmarks that the picked GPU must beat
    required_score = rankings.get(required_gpu_model)

    #TODO: some gpus either are not in list or not formatted right, probably should be fixed sometime
    #one of them is minecraft on min settings
    if required_score is None:
        print("GPU not in parts list")
        return None

    #logic to cheapest gpu that meets recs
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


#print(generate_pc("Fortnite","min",load_games(),load_gpu_rankings()))
#print(generate_pc("Escape from Tarkov","rec",load_games(),load_gpu_rankings()))