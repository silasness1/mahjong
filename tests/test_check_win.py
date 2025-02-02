import check_win
from hand_data import *  # noqa: F403


def test_getChouIndices(hand_meldwise_mahjong_unordered):
    """Illustrates how `getChouIndices()` returns 5,6,7 Ball over 6,7,8 Ball"""
    hand = hand_meldwise_mahjong_unordered
    convenienceMeld = check_win.getChouIndices(4, hand)  # index 4 is |Ball 6|

    # (6,7,8) None (5,6,7)
    expected = [[4, 14, 8], None, [4, 12, 14]]

    for i in range(3):
        thrupplePosInd = convenienceMeld[i]
        if thrupplePosInd is None:
            continue
        hand_length = len(hand)
        handString = "\n".join([str(x) + str(hand[x]) for x in range(hand_length)])
        meldString = "\n".join([str(x) + str(hand[x]) for x in thrupplePosInd])
        msg = (
            "\nTarget: "
            + str(hand[4])
            + "\nHand:\n"
            + handString
            + "\nMeld:\n"
            + meldString
        )

        assert thrupplePosInd == expected[i], msg


def test_check_win_melds(
    hand_meldwise_mahjong_unordered_true,
    hand_meldwise_mahjong_ordered_true,
    hand_meldwise_mahjong_true_wrongturn,
):
    """Assumes first word is false or true, then checks for mahjong."""
    param_dict = locals()
    fixtures = list(param_dict.values())
    fixture_names = list(param_dict.keys())

    for i in range(len(fixtures)):
        result = check_win.checkMahjong(fixtures[i])
        if "false" in fixture_names[i]:
            assert result[0] is False
        if "true" in fixture_names[i]:
            assert result is True


def test_checkWinMelds_fourPairs():  # TODO: TEST restriction on number of pairs (or kongs?), already restricted.
    pass


def test_check_chou(
    hand_chou_draw_issue,
):
    """A false case for detecting a chou"""
    res = check_win.getChouIndices(-1, hand_chou_draw_issue)  # last card is 9 Ball
    assert res == [None, None, None]
