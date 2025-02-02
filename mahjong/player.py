"""TODO: use inheritance to define two subclasses human and AI players"""

from tile import Tile


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

    def __init__(self, name) -> None:
        self.hand = []
        self.lockedTiles = (
            []
        )  # for drawing from graveyard or kongs, prevents reorganizing in checking for mahjong
        self.name = name

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

    def get_discard_input(self):
        """For human players enter a number to indicate which part of your hand to get rid of."""
        while True:
            print(self.displayHand())
            try:
                discardChoice = int(
                    input(f"Enter 1 to {len(self.hand)} of which card to discard: ")
                )
            except ValueError:
                print("Not an integer.")
                continue
            if not ((discardChoice >= 1) and (discardChoice <= len(self.hand))):
                print("Not in proper range. ")
                continue
            else:
                break
        return discardChoice
