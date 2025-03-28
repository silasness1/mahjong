"""Mahjong Program Entry Point"""

import tkinter as tk
from view.game_gui import GameGui
from model.game_master import GameMaster
from controller.game_controller import GameController


# start the GUI window
root = tk.Tk()

#
view = GameView(root, None)
#
model = MahjongGame()
controller = GameController(model, view)
view.controller = controller

if __name__ == "__main__":
    mahjong()
