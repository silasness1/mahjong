import random
from mahjong.tile import Tile


class Deck:  # todo: finish docstring
    """The collection of tiles on the board. There are 4 of each.

    attrib
    ------
    -stock: a list of tiles before they're drawn

    methods
    --------
    - shuffle
    - moveNRandom

    """

    NUMCOPIES = 4

    def __init__(self):
        self.stock = []
        for suit in ["Ball", "Bam", "Crack"]:
            for rank in range(1, 10):
                for copy in range(self.NUMCOPIES):
                    self.stock.append(Tile(suit, rank))

    def shuffle(self, test=False):
        """Mixes the order of the deck"""
        if test:
            random.seed(20)
        random.shuffle(self.stock)

    def moveNRandom(self, n: int, target: list[Tile], test=False) -> None:
        """moves `n` tiles from the deck to the target"""
        if test:
            random.seed(10)
        nSample = random.sample(self.stock, n)
        for Tile in nSample:
            tileIndex = self.stock.index(Tile)
            target.append(self.stock.pop(tileIndex))
