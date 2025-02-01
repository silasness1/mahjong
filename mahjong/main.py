"""The entry-point for the whole program. How you play the game."""

from game_master import GameMaster
import random

def start():
    print("STARTING GAME")
    random.seed(10)      #TODO: eventually remove
    game = GameMaster()
    game.deal()   
    while game.status != "finished":
        game.takeTurn() #handles discard, draw competition, check mahjong, transfers, and advancing active player
    wait = input("Game finished. Enter to clear game.")

if __name__ == "__main__":
    start()