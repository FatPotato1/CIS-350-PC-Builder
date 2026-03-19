#TODO: save build functionality (local database?)
#TODO: log area in gui that displays what the errors are, if any
#TODO: check current selected parts compatibility with min/recommended specs for selected game
#TODO: costs of each part
#TODO: implementation and more functions in the compatibility file
#TODO: testing data loading since it is kind of messy
#TODO: error handling for a lot of stuff

#TODO: possible dropdown of preset pc builds if people don't want to build their own
#TODO: possible settings for GUI that can change theme and scaling
#TODO: possible optimization algorithm that can take budget and maximize performace, get minimum current hardware to play game, etc

#main file: Launch UI, control flow, handle starting everything
from data_loading import load_games, load_gpu_rankings, load_cpu_rankings
from ui import UI

def main():
    games = load_games()
    gpu_rankings = load_gpu_rankings()
    cpu_rankings = load_cpu_rankings()
    UI(games, cpu_rankings, gpu_rankings).run()



if __name__ == "__main__":
    main()
