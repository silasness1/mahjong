"""A collection of functions to check validity of potential moves and whether a collection 
of tiles is a valid mahjong."""

from tile import Tile
from deck import Deck

# from functools import lru_cache
from typing import List


def getCount(hand: List[Tile], match: Tile) -> int:
    """Helper function to return the number of tiles in `hand` that match the `match`."""
    matchCount = 0  # number of identical tiles in hand as discard
    for tile in hand:
        if match == tile:
            matchCount += 1
    return matchCount


def fillNone(suit: str, rank: int, adj: int) -> Tile | None:
    """Helper function to see whether tiles with `rank` + `adjustment`
    are legitimate
    """
    try:
        return Tile(suit, rank + adj)
    except ValueError:
        return None


def getChouComponents(index: int, hand: list[Tile]):
    """Returns first matches of hand index for
    tiles in the hand with ranks within +/-2 when compared to hand[index] tile"""
    discardRank = hand[index].rank
    discardSuit = hand[index].suit

    # Collection of tiles to form (5,6,7) (6,7,8) (7,8,9)
    rankAdjustments = [  # e.g 7
        +1,  # 8
        +2,  # 9
        -1,  # 6
        -2,  # 5
        -1,  # 6
        +1,  # 8
    ]

    # creates tiles from six above. > 9 or <1 not allowed.
    relevantTiles = list(
        map(
            lambda x: fillNone(suit=discardSuit, rank=discardRank, adj=x),
            rankAdjustments,
        )
    )

    # stores whether each relevantTile exists
    greedyIndex = [None] * 6
    for cnt in range(len(hand)):
        for cnt2 in range(len(relevantTiles)):
            if relevantTiles[cnt2] == hand[cnt]:
                greedyIndex[cnt2] = cnt

    return greedyIndex


def getChouIndices(index: int, hand: list[Tile]) -> list[list[int]]:
    """
    Checks for a the 3 possible chous (run of the same suit) in a collection of tiles
    given the index.

    Params:
    -------------
    `hand`: the collection of tiles in which you're looking for a chou
    `index`:the index of a tile that exists in `hand`

    Returns:
    ---------------
    A list of listed index values that form a chou in the `hand`
    First entry: 3 index values that form a "XOO" chou
    Second entry: 3 index values that form a "OOX" chou
    Third entry: 3 index values that form a "OXO" chou
    """
    if index < 0:  # to support negative index
        index = len(hand) + index  # example -1: 16 - 1 = 15
    meldIndices = [None] * 3  # -1 are placeholders -_-

    greedyIndex = getChouComponents(index, hand)

    if (greedyIndex[0] is not None) & (greedyIndex[1] is not None):  # has +1 +2
        meldIndices[0] = [index, greedyIndex[0], greedyIndex[1]]  # XOO
    if (greedyIndex[2] is not None) & (greedyIndex[3] is not None):  # has -1 -2
        meldIndices[1] = [index, greedyIndex[2], greedyIndex[3]]  # OOX
    if (greedyIndex[4] is not None) & (greedyIndex[5] is not None):  # has +1 -1
        meldIndices[2] = [index, greedyIndex[4], greedyIndex[5]]  # OXO

    return meldIndices


def getOfAKindIndices(
    index: int, hand: list[Tile], OfAKind=Deck.NUMCOPIES
) -> list[int]:
    """Given a hand and a the index of a single tile in the hand,
    returns a list of indices of the first OfAKind=n found matching tiles in the hand

    Params
    ----------
    - index: the index value for a tile in the hand that you want to find a n-of-a kind for
    - hand: the collection of tiles you're looking in
    - OfAKind: the number of matching tiles you're looking for

    Returns
    -----------
    a list of the first n tiles it finds that match hand[index].
    [None, None, None] if no chous"""
    assert OfAKind in range(2, Deck.NUMCOPIES + 1)  # for pairs - 2, pongs - 3, kongs -4
    matchIndices = []
    matchTile = hand[index]
    for cnt in range(len(hand)):
        if (hand[cnt] == matchTile) & (len(matchIndices) < OfAKind - 1):
            matchIndices.append(cnt)
    return matchIndices


def checkMahjongMelds(
    hand: list[Tile],
    recursionCounter=0,
    meldCount=0,
    pairCount=0,
) -> tuple[bool, int, int]:
    """
    Assumes 17 tiles total (aka after drawing).

    Algorithm overview:
    1) Take a tile
    2) Get all possible chou role positions associated with tile.
    3) Pop the first chou, if the sub problem doesn't work move to the next
    4) If all chou problems don't work, try popping each of the OfAKinds (4,3,2) and solving their subproblems
    5) If nothing's worked so far, no mahjong

    Debug: one of the 7 cracks got left behind maybe because overlapping index btw chous

    Adding locked-tile feature

    Params
    ----------
    - hand (should refactor to player)
    - recursionCounter
    - meldCount
    - pairCount

    Returns
    --------
    A tuple that contains....
    - a boolean indicating mahjong (if subproblem, indicates popped all tiles)
    - the number of melds (moves of 3-4 tiles)
    - the number of pairs
    """

    # Found a way to use up all the tiles
    if len(hand) == 0:
        return True, meldCount, pairCount

    for index in range(len(hand)):  # take a tile
        chouIndices = getChouIndices(index, hand)  # all possible chou role positions

        # greedy find indices for following 3 chou caes: XOO OXO or OOX
        for thrupplePosInd in [i for i in chouIndices if i is not None]:

            # pop the respective chou role
            handSmall = [hand[i] for i in range(len(hand)) if i not in thrupplePosInd]

            # try solving the subproblem
            rest_cleared, rest_melds, rest_pairs = checkMahjongMelds(
                handSmall, recursionCounter + 1
            )

            if rest_cleared:

                # too many melds
                if rest_melds + 1 > 5:  # TODO edgecase: kang split between 4 melds?
                    return False, meldCount, pairCount

                # if subproblem cleared, add a meld?!
                else:
                    meldCount = rest_melds + 1
                    pairCount = rest_pairs

                return True, meldCount, pairCount

        # none of the chous worked out, try the Of A Kind roles
        ofAKindIndices = getOfAKindIndices(index, hand)

        # No mahjongs contain tiles which aren't part of a chou and have no matches
        if len(ofAKindIndices) <= 1:
            return False, meldCount, pairCount

        else:
            for ofAKind in [
                ofAKindIndices[0:4],
                ofAKindIndices[0:3],
                ofAKindIndices[0:2],
            ]:
                # pop of a kind  TODO:  for pairs and triples is this repetative?
                handSmall = [hand[i] for i in range(len(hand)) if i not in ofAKind]

                rest_cleared, rest_melds, rest_pairs = checkMahjongMelds(
                    handSmall, recursionCounter + 1
                )

                if rest_cleared:

                    # update recursion ladder back w meld, pair counts
                    if len(ofAKind) == 2:

                        # no more than 1 pair allowed
                        if rest_pairs + 1 > 1:
                            return False, meldCount, pairCount

                        # update pair couunt
                        else:
                            pairCount = rest_pairs + 1
                            meldCount = rest_melds
                            return True, meldCount, pairCount

                    # ofAKind is a tripple or kong - both melds
                    else:

                        # too many melds
                        if rest_melds + 1 > 5:
                            return False, meldCount, pairCount

                        # otherise add it to the count
                        else:
                            meldCount += rest_melds + 1
                            pairCount = rest_pairs
                            return True, meldCount, pairCount

                # Cases where the rest is false. not sure about this one.
                # First recursion? Catches case that there's another misfit tile somewhere
                # (it's not the first one though). later recursions?
                return (
                    False,
                    meldCount,
                    pairCount,
                )


def checkMahjongPairs(
    hand: list[Tile],
    _recursionCounter=0,
    meldCount=0,
    pairCount=0,
) -> tuple[bool, int, int]:
    """Looks for the type of mahjong with 7 pairs and 1 meld

    Params:
    --------
    - `hand`: a colection of tiles to look for mahjong in
    - `_recursionCounter`: not to be used, but keeps track of how many times the method calls itself
    - `meldCount`: the number of chous kongs or pongs found so far in the recursion
    - `pairCount`: the number of pairs found so far in the recursion

    Returns:
    ----------
    A tuple with a bool about being mahjong, meldCount, and the pairCount
    """
    # pops all pairs until left with 3, confirm it's a meld
    if len(hand) == 0:
        return True, meldCount, pairCount
    for index in range(len(hand)):  # take a tile
        ofAKindIndices = getOfAKindIndices(index, hand)
        if len(ofAKindIndices) > 1:  # to filter singleton -> fail case
            for ofAKind in [
                ofAKindIndices[0:2],
                ofAKindIndices[0:3],
                ofAKindIndices[0:4],
            ]:
                handSmall = [
                    hand[index] for index in range(len(hand)) if index not in ofAKind
                ]  # pop of a kind    TODO:  for pairs and triples is this repetative?
                theRest = checkMahjongMelds(handSmall, _recursionCounter + 1)
                if theRest[0]:
                    # update recursion ladder back w meld, pair counts
                    if len(ofAKind) == 2:
                        if theRest[2] + 1 > 7:  # no more than 1 pair allowed
                            return False, meldCount, pairCount
                        else:
                            pairCount = theRest[2] + 1
                            meldCount = theRest[1]
                            return True, meldCount, pairCount
                    else:  # a meld case
                        if theRest[1] + 1 > 1:
                            return False, meldCount, pairCount
                        else:
                            meldCount += theRest[1] + 1
                            pairCount = theRest[2]
                            return True, meldCount, pairCount
                return (
                    False,
                    meldCount,
                    pairCount,
                )  # NEw: cases where theRest is false. if none of the of-a-kinds work out either
        else:  # singletons must contribute to chou
            chouIndices = getChouIndices(
                index, hand
            )  # all possible chou role positions
            for thrupplePosInd in [
                i for i in chouIndices if i is not None
            ]:  # greedy find indices for following 3 chou caes: XOO OXO or OOX
                # pop the respective chou role
                handSmall = [
                    hand[index]
                    for index in range(len(hand))
                    if index not in thrupplePosInd
                ]
                # try solving the subproblem
                theRest = checkMahjongMelds(handSmall, _recursionCounter + 1)
                if theRest[0]:
                    if theRest[1] + 1 > 1:  # not allowed more than 1 meld
                        return False, meldCount, pairCount
                    else:
                        meldCount = theRest[1] + 1
                        pairCount = theRest[2]
                        return True, meldCount, pairCount
            return False, meldCount, pairCount  # singletons with no working chous


def checkMahjong(hand: list[Tile], lockedMelds: int) -> bool:
    """Returns true or false that the `hand` contains either kind of mahjong"""
    meld = checkMahjongMelds(hand, meldCount=lockedMelds)
    pair = checkMahjongPairs(hand, meldCount=lockedMelds)
    return (meld == (True, 5, 1)) or (pair == (True, 1, 7))
