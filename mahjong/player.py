"""TODO: use inheritance to define two subclasses human and AI players"""

from tile import Tile
from abc import abstractmethod

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_master import GameMaster  # Only for type hints, prevents circular import


class Player:  # maybe deck and players inherit from tile collections
    """
    methods
    ---------
    - getEffectiveHand:shows the tiles in hand and locked tiles together
    - displayHand: returns a pretty string version of effective hand
    - __str__: prints the player's name and their hand

    attributes
    -----------
    - `hand`: a list of tiles
    - `lockedTiles`: cards drawn from graveyard/kongs prevents reorganizing
    - `name`: the player's name
    """

    def __init__(self, name: str, game_master: "GameMaster") -> None:

        self.hand: list[Tile] = []

        # for drawing from graveyard or kongs, prevents reorganizing in checking for mahjong
        self.lockedTiles = []

        # player name
        self.name: str = name

        # Careful not to use self.game_master before GameMaster finishes init
        self.game_master = game_master

    def __str__(self):
        printString = f"{self.name}: "
        for tile in self.hand:
            printString += str(tile)

    def getEffectiveHand(self) -> list[Tile]:
        """Returns the tiels in both `hand` and `lockedTiles`"""
        effective = self.hand + self.lockedTiles
        return effective

    def displayHand(self, simple=True) -> str:  # TODO: FIX SIMPLE = F
        """Each str(tile) is "|Bam   9| " 9 wide (+ 1 space after)."""

        suitList = list(enumerate([tile.suit + str(tile.rank) for tile in self.hand]))
        suitList.sort(key=lambda x: x[1])
        suitSortedIndex = [x[0] for x in suitList]
        sortedHand = [self.hand[i] for i in suitSortedIndex]
        lockedString = "".join([str(i) for i in self.lockedTiles])
        horiz = "--------- "
        vert = "|       | "
        lockedHoriz = len(self.lockedTiles) * horiz
        lockedVert = len(self.lockedTiles) * vert
        handString = "".join([str(i) for i in sortedHand])
        handHoriz = len(self.hand) * horiz
        handVert = len(self.hand) * vert
        lockedDisplay = "\n".join(
            [
                lockedHoriz,
                lockedVert,
                lockedVert,
                lockedString,
                lockedVert,
                lockedVert,
                lockedHoriz,
            ]
        )
        handDisplay = "\n".join(
            [handHoriz, handVert, handVert, handString, handVert, handVert, handHoriz]
        )
        if simple:
            return (
                "Hand \n"
                + "\n".join(
                    [
                        f"{str(suitSortedIndex[i] + 1):>2} " + str(sortedHand[i])
                        for i in range(len(sortedHand))
                    ]
                )
                + "\nLocked \n"
                + "\n".join([str(i) for i in self.lockedTiles])
            )
        else:
            return (
                f"{str.upper(self.name)}'s HAND:\nLocked: \n"
                + lockedDisplay
                + "\nHand:   \n"
                + handDisplay
            )

    @abstractmethod
    def get_discard_input(self):
        """Note the only parameter is self because Players can get access to game state through `self.game_master`
        Human and AI players have to implement this method."""
        pass

    @abstractmethod
    def get_draw_preference(self, last_tile: Tile) -> int:
        """Note the only parameter is self because Players can get access to game state through `self.game_master`
        Human and AI players have to implement this method."""
        pass

    @abstractmethod
    def draw_pref_feedback(self, success: bool, preference: int):
        """Things to do when GameMaster indicates preference was illegal.

        Param
        -------
        - success: last submitted preference was legal
        - preference: the last submitted preference
        """
        pass
