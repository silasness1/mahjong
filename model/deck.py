from multiprocessing import Value
import random
from tile import Tile


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

    def shuffle(self, test=False, test_seed=20):
        """Mixes the order of the deck"""
        if test:
            random.seed(test_seed)
        random.shuffle(self.stock)

    def moveNRandom(self, n: int, target: list[Tile], test=False) -> bool:
        """moves `n` tiles from the deck to the target
        Returns success or fail.
        """
        if test:
            random.seed(10)

        try:
            nSample = random.sample(self.stock, n)
        except ValueError:
            print("Stock ran out of tiles. No one wins.")
            return False
        for this_tile in nSample:
            tileIndex = self.stock.index(this_tile)
            target.append(self.stock.pop(tileIndex))
        return True
