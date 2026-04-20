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


def _get_price(category, name):
    """
    Look up the price for a component by category key and name.

    Args:
        category (str): Top-level key in components.prices (e.g. "NVIDIA GPUs").
        name (str): Component name as it appears in components.hardware.

    Returns:
        int or None: Price in dollars, or None if not found.
    """
    return components.prices.get(category, {}).get(name)


def generate_pc_budget(game_name, game_list, cpu_rankings, gpu_rankings,
                       cpu_brand, gpu_brand, budget):
    """
    Generate a balanced PC build based on budget.

    Storage, PSU, motherboard and case are removed from budget first. remaining goes to ram, gpu, and cpu.

    Args:
        game_name (str): The name of the game to build a PC for (unused, kept for consistency).
        game_list (list[dict]): List of game dictionaries (unused, kept for consistency).
        cpu_rankings (dict): CPU benchmark rankings (unused, kept for consistency).
        gpu_rankings (dict): GPU benchmark rankings (unused, kept for consistency).
        cpu_brand (str): Preferred CPU brand; "Intel" or "AMD".
        gpu_brand (str): Preferred GPU brand; "NVIDIA" or "AMD".
        budget (float): Total maximum spend in dollars across all components.

    Returns:
        tuple: (gpu, cpu, ram) — each is a component name string, or None if no
        combination fits within the budget after fixed costs are deducted.
    """
    gpu_category = "NVIDIA GPUs" if gpu_brand == "NVIDIA" else "AMD GPUs"
    cpu_category = "Intel CPUs" if cpu_brand == "Intel" else "AMD CPUs"

    gpus = components.hardware.get(gpu_category, [])
    cpus = components.hardware.get(cpu_category, [])

    # create lists for prices
    gpu_prices = [(g, _get_price(gpu_category, g)) for g in gpus]
    gpu_prices = [(g, p) for g, p in gpu_prices if p is not None]

    cpu_prices = [(c, _get_price(cpu_category, c)) for c in cpus]
    cpu_prices = [(c, p) for c, p in cpu_prices if p is not None]

    # remove fixed costs (case, etc)
    fixed_cost = _fixed_component_cost(cpu_brand)
    flexible_budget = budget - fixed_cost

    if flexible_budget <= 0:
        print("Budget too low to cover fixed components (Storage, PSU, Motherboard, Case)")
        return None, None, None

    # pick the best RAM that still leaves room for at least the cheapest GPU+CPU
    ram = _pick_budget_ram(flexible_budget, gpu_prices, cpu_prices)
    ram_price = _ram_price(ram)

    # budget remaining after reserving RAM cost
    remaining = flexible_budget - ram_price

    # find the best balanced GPU/CPU combo within the remaining budget
    best_gpu = None
    best_cpu = None
    best_combined = -1

    for gpu_name, gpu_price in gpu_prices:
        cpu_budget = remaining - gpu_price
        if cpu_budget < 0:
            continue
        # most expensive CPU that fits the remaining budget
        affordable = [(c, p) for c, p in cpu_prices if p <= cpu_budget]
        if not affordable:
            continue
        best_cpu_name, best_cpu_price = max(affordable, key=lambda x: x[1])
        combined = gpu_price + best_cpu_price
        if combined > best_combined:
            best_combined = combined
            best_gpu = gpu_name
            best_cpu = best_cpu_name

    return best_gpu, best_cpu, ram


def _fixed_component_cost(cpu_brand):
    """
    Return the total price of components that are fixed in auto-generation:
    Storage, PSU, Motherboard (matched to CPU brand), and the cheapest Case.

    These costs are subtracted from the user budget before allocating the
    remainder to GPU, CPU, and RAM.

    Args:
        cpu_brand (str): "Intel" or "AMD", used to select the correct motherboard.

    Returns:
        int: Combined price in dollars of all fixed components.
    """
    storage_prices = components.prices.get("Storage", {})
    psu_prices = components.prices.get("PSU", {})
    mobo_prices = components.prices.get("Motherboards", {})
    case_prices = components.prices.get("Cases", {})

    # pick the single storage drive (only one in the list)
    storage_cost = next(iter(storage_prices.values()), 0)

    # pick the single PSU (only one in the list)
    psu_cost = next(iter(psu_prices.values()), 0)

    # pick motherboard matched to CPU brand
    mobo_list = components.hardware.get("Motherboards", {}).get(cpu_brand, [])
    mobo_cost = mobo_prices.get(mobo_list[0], 0) if mobo_list else 0

    # pick the cheapest case
    case_cost = min(case_prices.values()) if case_prices else 0

    return storage_cost + psu_cost + mobo_cost + case_cost


def get_build_price(build):
    """
    Calculate the total price of a build

    Looks up the price for each component in the build using components.prices.

    Args:
        build (dict): Build dictionary with keys like "GPU", "CPU", "RAM", etc.
            and values that are component name strings or None.

    Returns:
        int: Total price in dollars of all priced components in the build.
    """
    category_map = {
        "GPU":         lambda b: (
                           "NVIDIA GPUs" if b.get("GPU_Brand") == "NVIDIA" else "AMD GPUs"
                       ),
        "CPU":         lambda b: (
                           "Intel CPUs" if b.get("CPU_Brand") == "Intel" else "AMD CPUs"
                       ),
        "Motherboard": lambda b: "Motherboards",
        "Case":        lambda b: "Cases",
        "Storage":     lambda b: "Storage",
        "PSU":         lambda b: "PSU",
    }

    total = 0

    for key, category_fn in category_map.items():
        part = build.get(key)
        if not part:
            continue
        category = category_fn(build)
        price = components.prices.get(category, {}).get(part)
        if price is not None:
            total += price

    ram = build.get("RAM")
    if ram:
        ram_prices = components.prices.get("RAM", {})
        for key, price in ram_prices.items():
            if key in ram:
                total += price
                break

    return total


def _pick_budget_ram(budget, gpu_prices, cpu_prices):
    """
    Choose the most expensive RAM tier whose price still leaves enough budget
    for at least the cheapest available GPU and CPU.

    Args:
        budget (float): Total user budget in dollars.
        gpu_prices (list[tuple]): List of (name, price) for candidate GPUs.
        cpu_prices (list[tuple]): List of (name, price) for candidate CPUs.

    Returns:
        str or None: Name of the selected RAM stick, or None if even the cheapest
        RAM leaves no room for any GPU+CPU pair.
    """
    ram_prices = components.prices.get("RAM", {})
    ram_list = components.hardware.get("RAM", [])

    if not ram_prices or not gpu_prices or not cpu_prices:
        return None

    min_gpu_cost = min(p for _, p in gpu_prices)
    min_cpu_cost = min(p for _, p in cpu_prices)
    min_component_cost = min_gpu_cost + min_cpu_cost

    # sort by most expensive first
    sorted_ram = sorted(ram_prices.items(), key=lambda x: x[1], reverse=True)

    for ram_key, ram_cost in sorted_ram:
        if budget - ram_cost >= min_component_cost:
            # find the full stick name in the hardware list
            for stick in ram_list:
                if ram_key in stick:
                    return stick
    return None


def _ram_price(ram_name):
    """
    Return the price of a ram stick

    Args:
        ram_name (str or None): Full RAM stick name (e.g. "CORSAIR VENGEANCE RGB 32GB DDR5").

    Returns:
        int: Price in dollars, or 0 if the stick is None or not found.
    """
    if ram_name is None:
        return 0
    ram_prices = components.prices.get("RAM", {})
    for key, price in ram_prices.items():
        if key in ram_name:
            return price
    return 0