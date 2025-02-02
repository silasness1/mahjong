"""GameMaster manages the main game loop."""

from deck import Deck
from player import Player
import check_win as check_win
import random


class GameMaster:
    """The main game loop

    attributes
    -----------
    - `status`
    - `test`
    - `gameDeck`
    - `graveyard`
    - `playerList`
    - `activePlayer`

    methods
    ----------
    - `deal`
    - `_peakNextClockwisePlayer`
    - `_advanceNextClockwisePlayer`
    - `endgame`
    - `takeTurn`
    - `_discardFromPlayer`
    - `_checkLegalMove`
    - `_callForDiscard`
    - `_advanceToNextMove`

    """

    def __init__(self, customNames=False) -> None:

        self.status = "playing"
        self.test = True

        # Initiate Deck & TODO: Figure out the context for why I wrote this Tiles
        self.gameDeck = Deck()
        self.gameDeck.shuffle()
        self.graveyard = []  # For discarded tiles, behaves like stack

        # Initiate Players
        self.playerList = []
        NUMPLAYERS = 4
        if customNames:
            for i in range(NUMPLAYERS):
                queryNameString = "Enter name for player {num}:".format(num=i)
                thisName = input(
                    queryNameString
                )  # TODO: make sure no duplicate names to spoof chou privledges
                self.playerList.append(Player(thisName))
        else:
            defaultNames = ["PlayerN", "PlayerE", "PlayerS", "PlayerW"]
            for i in range(NUMPLAYERS):
                self.playerList.append(Player(defaultNames[i]))

        # Decide who goes first
        self.activePlayer = random.sample(self.playerList, 1)[0]

    def _peakNextClockwisePlayer(self) -> tuple[Player, int]:
        """Get the next player without switching activePlayer.
        In other words, a function to keep track of who's next.

        Returns
        ----------
        The player themselves and the index in the playerlist they represent"""
        nextPlayerIndex = (self.playerList.index(self.activePlayer) + 1) % len(
            self.playerList
        )
        return self.playerList[nextPlayerIndex], nextPlayerIndex

    def _advanceNextClockwisePlayer(
        self,
    ) -> None:  # active player can change elsewhere in the discard claim.
        """A method to switch active player to next in the player list"""
        nextPlayerIndex = (self.playerList.index(self.activePlayer) + 1) % len(
            self.playerList
        )
        self.activePlayer = self.playerList[nextPlayerIndex]

    def endgame(self, winner: Player) -> None:
        """Right before ending the game, show the winning hand and player's name"""
        print(winner.name)
        print("Winning Hand", winner.displayHand())
        self.status = "finished"
        input()  # wait for input before clearing

    def deal(self):
        """Gives each player DEALSIZE tiles and the active player (assume to be first player) one extra"""
        DEALSIZE = 16
        for player in self.playerList:
            self.gameDeck.moveNRandom(DEALSIZE, player.hand)
        self.gameDeck.moveNRandom(1, self.activePlayer.hand)  # starting player gets 17

    def _discardFromPlayer(self) -> None:
        """Gets input from active player and moves the selected tile to the graveyard."""
        while True:
            print(self.activePlayer.displayHand())
            try:
                discardChoice = int(
                    input(
                        f"Enter 1 to {len(self.activePlayer.hand)} of which card to discard: "
                    )
                )
            except ValueError:
                print("Not an int.")
                continue
            if not ((discardChoice >= 1) and (discardChoice <= 17)):
                print("not in proper range. ")
                continue
            else:
                break
        self.graveyard.append(self.activePlayer.hand.pop(discardChoice - 1))

    def _checkLegalMove(
        self, moveType: int, player: Player, indexList: list[int]
    ) -> tuple[bool, list[int]]:
        """Function checks whether each is legal given an integer from 1 to 5 which corresponse to the following
        - 5: Mahjong
        - 4: Kong
        - 3: Pong
        - 2: Chou
        - 1: Pass

        DONT be tempted to make this a static method. Requires knowledge of game state (Player order and graveyard)

        Params:
        -----------

        - moveType: 1-5 corresponding to preference
        - player : who we're checking for
        - indexList : If there's a legal move, what tiles is it using so
        we can potentially move it to player.lockedTiles`

        Returns:
        -----------

        A tuple containing whether move is legal and a modified indexList

        """
        # check legal move
        ofAKind = check_win.getOfAKindIndices(
            -1, player.hand + [self.graveyard[-1]]
        )  # done so that if ultimately appended indices correct
        matchCount = len(ofAKind)

        if moveType == 5:  # Mahjong
            legal = check_win.checkMahjong(
                player.getEffectiveHand() + [self.graveyard[-1]]
            )  # TODO: player.getEffectiveHand isn't returninga s expected
            if not legal:
                # TODO: no appended to indexList, how are transfers handled. WE wanted to transfer before endgame so that...
                print("No legal mahjong.")
        elif moveType == 4:  # Kong
            if matchCount == 4:
                indexList.append(ofAKind)  # queue kong to remove to locked
                legal = True  # TODO: somehow kong got passed even though not legal.
            else:
                print("No legal kongs.")
        elif moveType == 3:  # Pong
            if matchCount > 2:
                indexList.append(ofAKind[0:3])
                legal = True
            else:
                print("No legal pongs.")
        elif moveType == 2:  # Chou
            chouIndices = check_win.getChouIndices(
                -1, player.hand + [self.graveyard[-1]]
            )  # TODO: ensure inability to throw something you just needed to pick up (newly locked tiles)
            if not (chouIndices == [None] * 3):
                if self._peakNextClockwisePlayer()[0].name == player.name:
                    fakes = [
                        i is None for i in chouIndices
                    ]  # seems wrong during debug?
                    if sum(fakes) < 2:  # two or three options
                        chouPref = int(
                            input(
                                "Which chou do you want? 0 for XOO, 1 for OOX, 2 for OXO"
                            )
                        )  # TODO: validate input; also appears to be broken. It locked tiles that weren't even one of the options.
                        while not isinstance(
                            chouIndices[chouPref], list
                        ):  # prevents illegal options being none
                            chouPref = int(
                                input(
                                    "Which chou do you want? 0 for XOO, 1 for OOX, 2 for OXO"
                                )
                            )
                        indexList.append(chouIndices[chouPref])
                        legal = True
                    else:
                        indexList.append(chouIndices[fakes.index(False)])
                        legal = True
                else:
                    print("Your turn isn't next.")
            else:
                print("No legal chous.")
        else:  # Pass
            indexList.append(None)
            legal = True
        return legal, indexList

    def _callForDiscard(self) -> tuple[list[int], list[list[int]]]:
        """Gets each player's legal move preference. Players submit a number 1-5 to tell what they'd like to do with the
        tile that was just discarded. This also vets their choice.

        returns
        ---------
        List (in order of self.playerList) of integers representing which of the 5 move options
        they want to do with the current most recently discarded tile.
        """
        # Calling for Discarded Tile
        prefList = []
        indexList = (
            []
        )  # place to store each player's final desired operation for locked tile transfer.
        for player in self.playerList:
            if player.name == self.activePlayer.name:
                prefList.append(1)
                indexList.append(None)
                continue
            print(self.graveyard[-1].displayTile())
            print(f"\n{player.name}'s Hand:")
            print(player.displayHand())
            prompt = f"{player.name} choose between options 1-5 for {str(self.graveyard[-1])}:\n5: Mahjong\n4: Kong\n3: Pong\n2: Chou\n1: Pass\n"
            legal = False
            while not legal:
                preference = 0
                while (preference <= 0) or (preference >= 6):
                    while True:
                        try:
                            preference = int(input(prompt))
                            break
                        except ValueError:
                            print("Not a number.")
                legal, indexList = self._checkLegalMove(preference, player, indexList)
            prefList.append(preference)  # in order of self.playerlist
        return prefList, indexList

    def _advanceToNextMove(
        self, prefList: list[int], indexList: list[list[int]]
    ) -> None:
        """Given the preference list, determine who goes next, reassign self.activePlayer and give the next player their tiles
        either from the graveyard or the deck, while checking for mahjong.
        """
        # If all players passed, next person draws from the deck.
        if sum(prefList) == len(prefList):
            self._advanceNextClockwisePlayer()
            print(f"Now {self.activePlayer.name}'s Turn. Drew from deck.")
            self.gameDeck.moveNRandom(1, self.activePlayer.hand)

        else:
            # reorder Player and Preference lists such that next player is first (to help break ties in preference)
            nextIndex = self._peakNextClockwisePlayer()[1]
            relativePlayerList = [
                self.playerList[(i - nextIndex) % len(self.playerList)]
                for i in range(len(self.playerList))
            ]
            relativePrefList = [
                prefList[(i - nextIndex) % len(self.playerList)]
                for i in range(len(self.playerList))
            ]

            # see who had the biggest play (who won the preference list)
            realMax = max(prefList)
            relArgMax = relativePrefList.index(realMax)
            prefWinnerIndex = self.playerList.index(relativePlayerList[relArgMax])

            # give the preference winner becomes active player and gets the last tile
            self.activePlayer = self.playerList[prefWinnerIndex]
            self.activePlayer.hand.append(
                self.graveyard.pop(-1)
            )  # TODO: somehow reorder the indices right to actually get ordered meld to locked tiles.
            print(
                f"{self.activePlayer.name} got {self.activePlayer.hand[-1]} from graveyard."
            )

            # move the drawn move to the lockedTiles
            toTransfer = indexList[prefWinnerIndex]
            transferSet = set(toTransfer)
            tilesToLock = [
                e for i, e in enumerate(self.activePlayer.hand) if i in transferSet
            ]
            assert (
                len(tilesToLock) > 0
            )  # when obtained from graveyard and not mahjong... something has to go to locked pong or chou.
            self.activePlayer.lockedTiles += tilesToLock
            self.activePlayer.hand = [
                e for i, e in enumerate(self.activePlayer.hand) if i not in transferSet
            ]

    def takeTurn(self) -> None:
        """Turn starts with one player discarding a tile,
        procedes by every expressing a potential desire to calling that discard
        Finally the CW player draws from the deck or someone got the grave tile.ctive player is adjusted accordingly.
        Checks whether someone won this turn.
        """
        self._discardFromPlayer()
        prefList, indexList = self._callForDiscard()
        self._advanceToNextMove(prefList, indexList)
        if check_win.checkMahjong(self.activePlayer.getEffectiveHand()):
            self.endgame(
                winner=self.activePlayer
            )  # CW player won from deck or prefWinner got mahjong with grave tile
