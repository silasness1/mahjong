from unittest import TestCase
from tile import Tile


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
        expected_str = "--------- \n|       | \n|       | \n|Bam   9| \n|       | \n|       | \n--------- "
        self.assertEqual(
            thisTile.displayTile(),
            expected_str,
            msg=thisTile.displayTile(),
        )
