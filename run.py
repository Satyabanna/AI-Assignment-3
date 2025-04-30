import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from chess_game import play_game
from minimax_agent import minimax
from alphabeta_agent import alphabeta

if __name__ == "__main__":
    print("Running Minimax...")
    play_game(minimax, "recordings/minimax_game.mp4", depth=2)

    print("Running Alpha-Beta...")
    play_game(lambda b, d, t: alphabeta(b, d, float('-inf'), float('inf'), t), "recordings/alphabeta_game.mp4", depth=2)

