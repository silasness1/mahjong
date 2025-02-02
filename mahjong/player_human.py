from typing import TYPE_CHECKING
from tile import Tile
from player import Player

if TYPE_CHECKING:
    from game_master import GameMaster  # Only for type hints, prevents circular import


class PlayerHuman(Player):
    def __init__(self, name: str, game_master: "GameMaster") -> None:
        super().__init__(name, game_master)

    def get_discard_input(self):
        """Overwrites abstractmethod for humans"""
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

    def get_draw_preference(self, last_tile: Tile) -> int:
        """For human players use `input` to describe whether you want to interact
        with the last discarded tile."""
        print(last_tile.displayTile())
        print(f"\n{self.name}'s Hand:")
        print(self.displayHand())
        prompt = f"{self.name} choose between options 1-5 for {str()}:\n5: Mahjong\n4: Kong\n3: Pong\n2: Chou\n1: Pass\n"
        preference = 0
        while (preference <= 0) or (preference >= 6):
            while True:
                try:
                    preference = int(input(prompt))
                    break
                except ValueError:
                    print("Not a number.")
        return preference
