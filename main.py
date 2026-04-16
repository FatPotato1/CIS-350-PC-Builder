
"""
features to add:
more generation options, min cost, etc (me)
more target options, fps, etc (also me)
Ui tweaks (make it scale bigger, etc)
add motherboards, probably just 1 for each cpu brand
ability to save build, access and load it from something
compatibility (maybe just add check to make sure motherboard matches set parts)
error log somewhere in ui
Testing, both manual and unittest
"""
# main file: Launch UI, control flow, handle starting everything
from data_loading import load_games, load_gpu_rankings, load_cpu_rankings
from ui import UI

def main():
    games = load_games()
    gpu_rankings = load_gpu_rankings()
    cpu_rankings = load_cpu_rankings()
    UI(games, cpu_rankings, gpu_rankings).run()



if __name__ == "__main__":
    main()
