import components
from data_loading import (load_games, load_gpu_rankings,
                          load_cpu_rankings, extract_cpu_model)

# generate a list of parts for pc based on selected game and either min or recommended specs
# this should be able to be modified somewhat easily to include amd gpus, all cpus, etc


def generate_pc(game_name, target_performance, game_list, cpu_rankings, gpu_rankings, cpu_brand, gpu_brand, algorithm):
    """
    Generate a recommended PC parts list GPU and CPU for a given game and performance target.

    Args:
        game_name (str): The name of the game to maximize PC performance for
        target_performance (str): Performance tier to target; "rec" for recommended specs or "min" for minimum specs.
        game_list (list[dict]): List of game dictionaries containing spec requirements.
        cpu_rankings (dict): Mapping of CPU model names to benchmark scores.
        gpu_rankings (dict): Mapping of GPU model names to benchmark scores.
        cpu_brand (str): Preferred CPU brand; "Intel" or "AMD".
        gpu_brand (str): Preferred GPU brand; "NVIDIA" or "AMD".
        algorithm: Selection algorithm to use for part picking

    Returns:
        tuple: A tuple of (gpu, cpu) where each element is a part name string or None if no match was found.
    """

    return (generate_gpu(game_name, target_performance, game_list, gpu_rankings, gpu_brand, algorithm),
            generate_cpu(game_name, target_performance, game_list, cpu_rankings, cpu_brand, algorithm),
            generate_ram(game_name, target_performance, game_list, algorithm))


def generate_cpu(game_name, target_performance, game_list, rankings, cpu_brand, algorithm):
    """
    Select the most capable CPU that is compatible at or below the required benchmark score for a game's spec tier.

    Looks up the required CPU benchmark score for the given game and performance target, then it
    selects the highest-scoring CPU from the components list that still meets but does not
    exceed that score

    Args:
        game_name (str): The name of the game to build a PC for.
        target_performance (str): Performance tier to target; rec for recommended specs or min for minimum specs.
        game_list (list[dict]): List of game dictionaries containing spec requirements.
        rankings (dict): Mapping of CPU model names to benchmark scores.
        cpu_brand (str): Preferred CPU brand; "Intel" or "AMD".
        algorithm: Selection algorithm to use for part picking (reserved for future use).

    Returns:
        str or None: The name of the selected CPU component, or None if the required CPU model
        is not found in the rankings.
    """

    selected_cpu = None
    selected_score = None
    # list of cpus from components
    if cpu_brand == "Intel":

        cpus = components.hardware.get("Intel CPUs", [])
    else:
        cpus = components.hardware.get("AMD CPUs", [])

    game = None

    # find the game in list
    for x in game_list:
        if x["game_name"] == game_name:
            game = x
            break
    if target_performance == "rec":
        required_cpu_model = game["rec_cpu_model"]

    else:
        required_cpu_model = game["min_cpu_model"]

    # the ranking from CPU_UserBenchmarks that the picked CPU must beat
    required_score = rankings.get(required_cpu_model)
    if required_score is None:
        print("CPU not in parts list")
        return None

    # logic to cheapest cpu that meets recs
    for cpu in cpus:
        cpu_name = extract_cpu_model(cpu)

        if cpu_name is None:
            continue

        cpu_score = rankings.get(cpu_name)

        if cpu_score is None:
            continue
        if cpu_score <= required_score:
            if selected_score is None or cpu_score > selected_score:
                selected_cpu = cpu
                selected_score = cpu_score
    return selected_cpu


def generate_ram(game_name, target_performance, game_list, algorithm):
    """
    Select the appropriate RAM stick for a game's minimum or recommended spec tier.

    RAM is returned directly from the game's spec entry rather than being selected by benchmark score comparison.

    Args:
        game_name (str): The name of the game to build a PC for.
        target_performance (str): Performance tier to target; rec for recommended specs or min for minimum specs.
        game_list (list[dict]): List of game dictionaries containing spec requirements.
        algorithm: Selection algorithm to use for part picking (reserved for future use).

    Returns:
        str: The RAM stick identifier from the game's spec entry.
    """
    # find the game in list
    for x in game_list:
        if x["game_name"] == game_name:
            game = x
            break
    if target_performance == "rec":
        return game["rec_ram_stick"]

    else:
        return game["min_ram_stick"]


# needs to be modified to include amd gpus, currently data loader regex only does nvidia cards
def generate_gpu(game_name, target_performance, game_list, rankings, gpu_brand, algorithm):
    """
    Select the most capable GPU at or below the required benchmark score for a game's spec tier.

    Looks up the required GPU benchmark score for the given game and performance target, then
    selects the highest-scoring GPU from the components list that still meets but does not
    exceed that score

    Args:
        game_name (str): The name of the game to build a PC for.
        target_performance (str): Performance tier to target; "rec" for recommended specs or "min" for minimum specs.
        game_list (list[dict]): List of game dictionaries containing spec requirements.
        rankings (dict): Mapping of GPU model names to benchmark scores.
        gpu_brand (str): Preferred GPU brand; "NVIDIA" or "AMD".
        algorithm: Selection algorithm to use for part picking (reserved for future use).

    Returns:
        str or None: The name of the selected GPU component, or None if the required GPU model
        is not found in the rankings.
    """

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
