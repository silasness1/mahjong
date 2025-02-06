"""GameMaster manages the main game loop."""

from deck import Deck
from player import Player
from player_ai import PlayerAI
from player_human import PlayerHuman
from tile import Tile
from check_win import checkMahjong, getOfAKindIndices, getChouIndices
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
    - `_checkLegalDraw`
    - `_callForDiscard`
    - `_advanceToNextMove`

    """

    def __init__(self, playerDictionary: dict[str:str], NUMPLAYERS=4) -> None:

        self.status = "playing"
        self.test = True
        self.turn_count = 0  # set right before discard; helps with debugging

        # Initiate Deck
        self.gameDeck = Deck()
        self.gameDeck.shuffle()
        self.graveyard = []  # For discarded tiles, behaves like stack

        # Initiate Players
        self.playerList = []

        assert len(playerDictionary.items()) == NUMPLAYERS
        for player_name, player_type in playerDictionary.items():
            if player_type == "ai":
                self.playerList.append(PlayerAI(player_name, self))
            elif player_type == "human":
                self.playerList.append(PlayerHuman(player_name, self))

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
        if winner is None:
            print("Everyone lost.")
        else:
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
        """Gets input from active player and moves the selected tile to the graveyard.
        TODO: have to call a method from player in order to get input so that we can override it for non-human players.
        """
        discardChoice = self.activePlayer.get_discard_input()
        self.graveyard.append(self.activePlayer.hand.pop(discardChoice - 1))
        print(f"{self.activePlayer.name} discarded {self.graveyard[-1]}.")

    def _checkLegalDraw(
        self, moveType: int, player: Player, drawTile: Tile
    ) -> tuple[bool, list[int]]:
        """Function checks whether each is legal given an integer from 1 to 5 which corresponse to the following
        - 5: Mahjong
        - 4: Kong
        - 3: Pong
        - 2: Chou
        - 1: Pass

        DONT be tempted to make this a static method. Requires knowledge of game state (Player order and graveyard)

        TODO: Actually just pass a boolean about whether this is the next player and what the last graveyard tile was.

        Params:
        -----------

        - moveType: 1-5 corresponding to preference
        - player : who we're checking for
        - drawTile: imagine adding 1 tile before checking legality of moveType

        Returns:
        -----------

        A tuple containing whether move is legal and an indexList, the set of legal tiles to operate the moveType.

        One use will be to move all legal tiles to `player.lockedTiles`
        """
        indexList = None
        legal = False
        is_human = isinstance(player, PlayerHuman)

        # check number of matching with discarded tile
        ofAKind = getOfAKindIndices(-1, player.hand + [drawTile])
        matchCount = len(ofAKind)

        if moveType == 5:  # Mahjong

            # TODO: player.getEffectiveHand isn't returninga s expected
            legal = checkMahjong(player.hand + [drawTile], player.lockedMelds)

            if not legal and is_human:
                print("No legal mahjong.")
        elif moveType == 4:  # Kong
            if matchCount == 4:
                indexList = ofAKind  # queue kong to remove to locked
                legal = True  # TODO: somehow kong got passed even though not legal.
            elif is_human:
                print("No legal kongs.")
        elif moveType == 3:  # Pong
            if matchCount > 2:
                indexList = ofAKind[0:3]
                legal = True
            elif is_human:
                print("No legal pongs.")
        elif moveType == 2:  # Chou
            chouIndices = getChouIndices(
                -1, player.hand + [drawTile]
            )  # TODO: ensure inability to throw something you just needed to pick up (newly locked tiles)
            if not (chouIndices == [None] * 3):
                if self._peakNextClockwisePlayer()[0].name == player.name:
                    fakes = [
                        i is None for i in chouIndices
                    ]  # seems wrong during debug?
                    if sum(fakes) < 2:  # two or three options

                        # TODO: validate input; also appears to be broken. It locked tiles that weren't even one of the options.

                        chouPref = player.get_chou_type()  # init while loop
                        # prevents illegal options being none
                        while chouIndices[chouPref] is None:
                            chouPref = player.get_chou_type()

                        indexList = chouIndices[chouPref]
                        legal = True
                    else:
                        indexList = chouIndices[fakes.index(False)]
                        legal = True
                elif is_human:
                    print("Your turn isn't next.")
            elif is_human:
                print("No legal chous.")
        else:  # Pass
            indexList = None
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

        # Store what each player would like to do using 1-5
        prefList = []

        # place to store how each player's collection of tiles for their desired operation
        prefIndexList: list[list[int]] = []

        for player in self.playerList:

            # Person who discarded automatically passes
            if player.name == self.activePlayer.name:
                prefList.append(1)
                prefIndexList.append(None)
                continue

            # Other players get to express preference
            legal = False
            while not legal:
                preference = player.get_draw_preference(last_tile=self.graveyard[-1])
                legal, indexList = self._checkLegalDraw(
                    moveType=preference, player=player, drawTile=self.graveyard[-1]
                )
                # For human players print a message, for AI set a flag
                player.draw_pref_feedback(legal, preference)
            prefList.append(preference)  # in order of self.playerlist
            prefIndexList.append(indexList)

        msg = "Index List is showing no tile transfers even though pref list has non-pass move."
        if prefList != [1, 1, 1, 1]:
            assert prefIndexList != [
                None,
                None,
                None,
                None,
            ], msg
        return prefList, prefIndexList

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
            successful_transfer = self.gameDeck.moveNRandom(1, self.activePlayer.hand)
            if not successful_transfer:
                print("Ending game due to lack of tiles in stock")
                self.endgame(winner=None)

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

            # The preference winner becomes active player and gets the last tile
            # TODO: somehow reorder the indices right to actually get ordered meld to locked tiles.
            self.activePlayer = self.playerList[prefWinnerIndex]
            self.activePlayer.hand.append(self.graveyard.pop(-1))
            print(
                f"{self.activePlayer.name} got {self.activePlayer.hand[-1]}from graveyard."
            )

            # assemble the tiles that need to get locked
            toTransfer = indexList[prefWinnerIndex]
            transferSet = set(toTransfer)
            tilesToLock = [
                e for i, e in enumerate(self.activePlayer.hand) if i in transferSet
            ]
            assert len(tilesToLock) > 0, "Moved 0 tiles into locked."
            # Add to locked
            self.activePlayer.lockedTiles += tilesToLock
            # Get rid of them from hand
            self.activePlayer.hand = [
                e for i, e in enumerate(self.activePlayer.hand) if i not in transferSet
            ]
            # all grave -> locked are melds, helps with mahjong check
            self.activePlayer.lockedMelds += 1

    def takeTurn(self) -> None:
        """Turn starts with one player discarding a tile,
        procedes by every expressing a potential desire to calling that discard
        Finally the CW player draws from the deck or someone got the grave tile.ctive player is adjusted accordingly.
        Checks whether someone won this turn.
        """
        self.turn_count += 1
        print(f"Turn {self.turn_count}-{self.activePlayer.name}:")
        self._discardFromPlayer()
        prefList, indexList = self._callForDiscard()
        self._advanceToNextMove(prefList, indexList)
        # CW player won from deck or prefWinner got mahjong with grave tile
        won = checkMahjong(self.activePlayer.hand, self.activePlayer.lockedMelds)
        if won:
            self.endgame(winner=self.activePlayer)
