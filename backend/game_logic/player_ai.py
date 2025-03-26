from typing import TYPE_CHECKING
from tile import Tile
from player import Player
from check_win import getChouComponents, getCount, getChouIndices
import random

if TYPE_CHECKING:
    from game_master import GameMaster  # Only for type hints, prevents circular import


class PlayerAI(Player):
    """A base class for all future AI player development. First iteration super simple."""

    def __init__(self, name: str, game_master: "GameMaster") -> None:
        super().__init__(name, game_master)
        self.last_pref = (True, None)

    def get_discard_input(self):
        """Simplest AI will discard a random tile.Too simple that they never win the game.
        Gets rid of useless tiles first."""
        num_non_locked = len(self.hand)

        # Get rid of tiles with no matches & that are not part of an unlocked chou
        for i in range(num_non_locked):
            candidate = self.hand[i]
            has_matches = getCount(self.hand, candidate) >= 1
            has_chou = getChouIndices(i, self.hand) != [None, None, None]
            if not (has_matches or has_chou):
                return i + 1  # discard response expects 1 to 17

        # If none of above conditions met, check for tiles that have no neighbors (iffy, but better than rand)
        for i in range(num_non_locked):
            has_neighbors = getChouComponents(i, self.hand)
            if has_neighbors == [None] * 6:
                return i + 1

        return random.randint(1, num_non_locked)  # in case all are useful.

    def get_draw_preference(self, last_tile: Tile) -> int:
        """Systematically try moveType 5,4,3,2,1 and relies on GameMaster for legality"""
        # Try mahjong on first attempt
        if self.last_pref[0]:
            return 5
            # Presumably GameMaster calls draw_pref_feedback()

        else:
            # Try one lower
            return self.last_pref[1] - 1

    def draw_pref_feedback(self, success: int, preference: int):
        """Keeps record of last draw preference to so `get_draw_preference()` can try 5 to 1"""
        self.last_pref = (success, preference)

    def get_chou_type(self) -> int:
        return random.randint(0, 2)
