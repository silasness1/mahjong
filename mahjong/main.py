"""The entry-point for the whole program. How you play the game."""

from game_master import GameMaster
import random

NUMPLAYERS = 4


def survey_player_settings(NUMPLAYERS=4) -> dict:
    custom_names = input("Want custom player names? Enter 0 for false 1 for true.")
    assert custom_names in ["0", "1"]

    num_ai = input("Want any AI Players? Enter 0 to 4.")
    assert num_ai in ["0", "1", "2", "3", "4"]

    player_types = ["ai"] * int(num_ai) + (NUMPLAYERS - int(num_ai)) * ["human"]

    if custom_names == "0":
        player_names = ["PlayerN", "PlayerE", "PlayerS", "PlayerW"]
    else:
        player_names = []
        for i in range(NUMPLAYERS):
            queryNameString = "Enter name for player {num}:".format(num=i)
            thisName = input(queryNameString)
            assert thisName not in player_names  # avoids duplication
            player_names.append(thisName)
    return dict(zip(player_types, player_names))


default_player_dict = {
    "Silas": "human",
    "Player2": "ai",
    "Player3": "ai",
    "Player4": "ai",
}


def start(input_settings=False):
    print("STARTING GAME")
    random.seed(15)  # was 10
    if input_settings:
        game = GameMaster(survey_player_settings())
    else:
        game = GameMaster(default_player_dict)
    game.deal()
    while game.status != "finished":
        game.takeTurn()  # handles discard, draw competition, check mahjong, transfers, and advancing active player
    input("Game finished. Enter to clear game.")


if __name__ == "__main__":
    start()
