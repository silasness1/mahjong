"""Tests related to the game_master module"""

import pytest
from unittest.mock import patch
from mahjong.game_master import GameMaster


# Test function (no need for classes with pytest)
@patch("builtins.input", side_effect=["Mom", "Dad", "Sister", "Brother"])
def test_GameMaster_init(mock_input):
    # Create the GameMaster instance with custom names
    with_names = GameMaster(customNames=True)

    # Assert that the player names are correct
    assert with_names.playerList[0].name == "Mom"
    assert with_names.playerList[3].name == "Brother"


# class ExampleTests(TestCase):


#     # def setUp(self):
#         # self.game = GameMaster()

#     @patch('mahjong.example.input', create=True)
#     def test_example(self, mock_input):
#         mock_input.side_effect = ['Mom', 'Dad', 'Sister', 'Brother']
#         res = function2()
#         print(res)
#         self.assertTrue(res[1]=='Mom')

#     if __name__ == '__main__':
#         unittest.main(verbosity=True)

#     def test_lockTiles(self):
#         #TODO: Fix/figure out how/what happened.
#         """
#     PlayerE's Hand:
# Hand
#  1 |Ball  4|
#  2 |Ball  6|
#  3 |Ball  6|
#  4 |Ball  7|
#  5 |Ball  7|
#  6 |Ball  8|
#  7 |Bam   3|
#  8 |Bam   3|
#  9 |Crack 4|
# 10 |Crack 5|
# 11 |Crack 6|
# 12 |Crack 6|
# 13 |Crack 7|
# 14 |Crack 8|
# 15 |Crack 8|
# 16 |Crack 9|
# Locked

# Which chou do you want? 0 for XOO, 1 for OOX, 2 for OXO0

#         I got multiple index choices for possible chou and picked 0
#         PlayerE got |Crack 9|  from graveyard.
# Hand
#  1 |Ball  4|
#  2 |Ball  6|
#  3 |Ball  6|
#  4 |Ball  7|
#  5 |Ball  7|
#  6 |Ball  8|
#  7 |Bam   3|
#  8 |Bam   3|
#  9 |Crack 4|
# 10 |Crack 5|
# 11 |Crack 6|
# 12 |Crack 8|
# 13 |Crack 9|
# 14 |Crack 9|
# Locked
# |Crack 8|
# |Crack 7|
# |Crack 6|"""
