from mahjong.view.game_gui import GameGui

import tkinter as tk

root = tk.Tk()



game_gui = GameGui(root)

# game_gui.create_frame()
game_gui.create_tile("Bam", 2, orientation='left')
# game_gui.create_tile()
# game_gui.create_tile()
# game_gui.create_tile()



root.mainloop()