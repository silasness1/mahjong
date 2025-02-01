from unittest import TestCase
<<<<<<< HEAD
from mahjong.tile import Tile
=======
from tile import Tile
>>>>>>> 18507d4 (pytest working)


class TileTests(TestCase):
    def test_equality(self):
        thisTile = Tile("Bam", 9)
        thatTile = Tile("Bam", 9)
        self.assertEqual(thisTile, thatTile)

    def test_notEquals(self):
        thisTile = Tile("Bam", 9)
        thatTile = Tile("Bam", 9)
        self.assertFalse(thisTile != thatTile)

    def test_string(self):
        thisTile = Tile("Bam", 9)  # TODO: fix test
        self.assertEqual(str(thisTile), "|Bam   9| ", msg=str(thisTile))
<<<<<<< HEAD
        self.assertEqual(
            thisTile.displayTile,
            "--------- \n|       | \n|       | \n|Bam   9| \n|       | \n|       | \n--------- ",
            msg=thisTile.displayTile,
=======
        expected_str = "--------- \n|       | \n|       | \n|Bam   9| \n|       | \n|       | \n--------- "
        self.assertEqual(
            thisTile.displayTile(),
            expected_str,
            msg=thisTile.displayTile(),
>>>>>>> 18507d4 (pytest working)
        )
