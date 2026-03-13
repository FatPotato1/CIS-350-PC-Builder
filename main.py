#main file: Launch UI, control flow, handle starting everything
from data_loading import load_games, load_gpu_rankings
from ui import UI

def main():
    games = load_games()
    rankings = load_gpu_rankings()
    UI(games, rankings).run()



if __name__ == "__main__":
    main()
