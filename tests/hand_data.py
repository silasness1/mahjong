"""Various hands used to test the functions which return and check pairs, melds, mahjongs etc"""

from tile import Tile
import pytest

hand_pairwise_mahjong = [
    Tile("Ball", 1),
    Tile("Ball", 1),  # Pair 1
    Tile("Ball", 2),
    Tile("Ball", 2),  # Pair 2
    Tile("Ball", 3),
    Tile("Ball", 3),  # Pair 3
    Tile("Bam", 4),
    Tile("Bam", 4),  # Pair 4
    Tile("Bam", 5),
    Tile("Bam", 5),  # Pair 5
    Tile("Bam", 6),
    Tile("Bam", 6),  # Pair 6
    Tile("Crack", 7),
    Tile("Crack", 7),  # Pair 7
    Tile("Crack", 3),
    Tile("Crack", 3),
    Tile("Crack", 3),  # Meld part of a Pong
]

seed_20 = [
    Tile("Bam", 3),
    Tile("Ball", 3),
    Tile("Bam", 8),
    Tile("Bam", 3),
    Tile("Crack", 5),
    Tile("Ball", 6),
    Tile("Crack", 5),
    Tile("Bam", 7),
    Tile("Crack", 7),
    Tile("Bam", 3),
    Tile("Crack", 8),
    Tile("Ball", 7),
    Tile("Ball", 7),
    Tile("Ball", 5),
    Tile("Bam", 7),
    Tile("Ball", 7),
    Tile("Crack", 7),
    Tile("Ball", 6),
]


# Fixture for initializing a GameMaster object
@pytest.fixture
def hand_meldwise_mahjong_unordered_true():
    hand = [
        Tile("Ball", 3),
        Tile("Ball", 3),
        Tile("Bam", 6),
        Tile("Crack", 7),
        Tile("Ball", 6),
        Tile("Crack", 5),
        Tile("Bam", 7),
        Tile("Crack", 7),
        Tile("Ball", 8),
        Tile("Crack", 7),
        Tile("Bam", 8),
        Tile("Ball", 7),
        Tile("Ball", 5),
        Tile("Crack", 6),
        Tile("Ball", 7),
        Tile("Crack", 7),
        Tile("Ball", 6),
    ]
    return hand


@pytest.fixture
def hand_meldwise_mahjong_ordered_true():
    hand = [
        Tile("Ball", 3),
        Tile("Ball", 3),
        Tile("Bam", 6),
        Tile("Bam", 7),
        Tile("Bam", 8),
        Tile("Crack", 5),
        Tile("Crack", 6),
        Tile("Crack", 7),
        Tile("Crack", 7),
        Tile("Crack", 7),
        Tile("Crack", 7),
        Tile("Ball", 5),
        Tile("Ball", 6),
        Tile("Ball", 7),
        Tile("Ball", 6),
        Tile("Ball", 7),
        Tile("Ball", 8),
    ]
    return hand


@pytest.fixture
def hand_meldwise_mahjong_true_wrongturn():
    """A trap. If you make the first three tiles a meld, you can't make a mahjong. It's to step through
    many layers of recursion."""

    hand = [
        Tile("Ball", 1),
        Tile("Ball", 2),
        Tile("Ball", 3),
        Tile("Ball", 4),  # Ball 3 pair, Ball 678, Ball 567
        Tile("Ball", 1),
        Tile("Crack", 5),
        Tile("Bam", 8),
        Tile("Crack", 2),  # Crack 7 * 3, Crack 567
        Tile("Ball", 8),
        Tile("Crack", 7),
        Tile("Bam", 8),
        Tile("Ball", 7),  # Bam 678
        Tile("Ball", 9),
        Tile("Crack", 2),
        Tile("Bam", 8),
        Tile("Crack", 6),
        Tile("Crack", 2),  # Crack 567
    ]
    return hand


@pytest.fixture
def hand_chou_draw_issue():
    """A hand I was playing and noticed something wrong with the locked tiles"""
    hand = [
        Tile("Bam", 7),  # Bam 7
        Tile("Crack", 1),  # Crack 1
        Tile("Bam", 8),  # Bam 8
        Tile("Crack", 2),  # Crack 2
        Tile("Crack", 3),  # Crack 3
        Tile("Ball", 6),  # Ball 6
        Tile("Ball", 3),  # Ball 3
        Tile("Ball", 3),  # Ball 3 (pair)
        Tile("Crack", 3),  # Crack 3
        Tile("Ball", 4),  # Ball 4
        Tile("Bam", 7),  # Bam 7 (meld part)
        Tile("Ball", 4),  # Ball 4 (meld part)
        Tile("Ball", 4),  # Ball 4 (meld part)
        Tile("Ball", 9),  # Ball 9
    ]
    return hand


@pytest.fixture
def false_mahjong_identification():
    """Check Mahjong wasn't respecting the locked tiles."""
    hand = [
        Tile("Bam", 8),  # 1
        Tile("Bam", 9),  # 2
        Tile("Crack", 3),  # 3
        Tile("Ball", 5),  # 4
        Tile("Ball", 4),  # 5
        Tile("Ball", 6),  # 6
        Tile("Crack", 1),  # 7
        Tile("Ball", 2),  # 8
        Tile("Ball", 2),  # 9
        Tile("Ball", 2),  # 10
        Tile("Crack", 5),  # 11
        Tile("Crack", 5),  # 12
        Tile("Crack", 5),  # 13
        Tile("Crack", 2),  # 14
        Tile("Crack", 3),  # 15
        Tile("Crack", 4),  # 16
        Tile("Bam", 7),  # 17
    ]
    return hand


"Player3:|Crack 5| |Crack 5| |Crack 5| |Crack 2| |Crack 3| |Crack 4| "
