import main


def test_GameMaster_init():
    """Does it run?? Look for seed in game master?"""

    all_ai = {"Player1": "ai", "Player2": "ai", "Player3": "ai", "Player4": "ai"}
    finished_game = main.start(player_dict=all_ai, wait_on_end=False)
    assert finished_game.status == "finished"
