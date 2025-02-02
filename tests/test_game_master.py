"""Tests related to the game_master module"""

import pytest
from unittest.mock import patch  # ,MagicMock
from game_master import GameMaster
from deck import Deck


# Fixture for mocking Deck
# @pytest.fixture  # TODO: use/Implement
# def mock_deck():
#     mock_deck = MagicMock(spec=Deck)
#     return mock_deck


# Fixture for initializing a GameMaster object
@pytest.fixture
@patch("builtins.input", side_effect=["Mom", "Dad", "Sister", "Brother"])
def with_names(mock_input):
    return GameMaster(customNames=True)


def test_GameMaster_init(with_names):
    # Assert that the player names are correct
    assert with_names.playerList[0].name == "Mom"
    assert with_names.playerList[3].name == "Brother"


def test_peak_next_clockwise_player(with_names):
    actual = with_names._peakNextClockwisePlayer()[0].name
    next_dict = {"Mom": "Dad", "Dad": "Sister", "Sister": "Brother", "Brother": "Mom"}
    expected = next_dict[with_names.activePlayer.name]
    assert expected == actual


def test_deal():
    game_master = GameMaster(customNames=False)

    # Mock the Deck's moveNRandom method to measure call count
    with patch.object(Deck, "moveNRandom") as mock_move:
        game_master.deal()

        # Check that moveNRandom was called for each player
        assert mock_move.call_count == len(game_master.playerList) + 1


def test_advance_next_clockwise_player(with_names):
    initial_player = with_names.activePlayer

    with_names._advanceNextClockwisePlayer()

    # Check that the active player has moved to the next player
    assert with_names.activePlayer != initial_player
    assert with_names.playerList.index(with_names.activePlayer) == (
        (with_names.playerList.index(initial_player) + 1) % len(with_names.playerList)
    )


@pytest.mark.parametrize(
    "move_type, expected_result",
    [
        (5, True),  # Mahjong
        (4, True),  # Kong
        (3, True),  # Pong
        (2, True),  # Chou
        (1, True),  # Pass
    ],
)
def test_check_legal_move(game_master, move_type, expected_result):
    """TODO: Implement by checking all 5 numbers for a given hand"""
    pass
    # player = game_master.playerList[0]

    # with patch(
    #     "check_win.checkMahjong", return_value=True
    # ), patch(  # TODO: Make this more realistic
    #     "check_win.getOfAKindIndices", return_value=[1, 2, 3]
    # ):
    #     legal, index_list = game_master._checkLegalDraw(move_type, player, )
    #     assert legal == expected_result
