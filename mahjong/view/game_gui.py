from tkinter import *
from tkinter import ttk
import tkinter as tk
from mahjong.view.drag_tile import DragTile

class GameGui:
    """The view part of Model-View-Controller. This class is responsible for gathering input and 
    communicating with the controller
    """

    def __init__(self, root):
        self.root = root

        #create frame
        self.canvas = tk.Canvas(self.root, width=500, height=400, bg="green")
        self.canvas.pack() # puts canvas in root

        # snappable grid 
        self.grid_size = 50
        self.tile_width = 40
        self.tile_height = 40
        self.play_area = (50, 50, 450, 450)  # (x1, y1, x2, y2)

    
    def create_drag_tile(self):
        """creates a draggable tile"""
        my_tile = DragTile(self.canvas, 100, 100, "/home/schmoopsan/mahjong/mahjong/view/tile_images/Pin7.png", 50, (50, 50, 450, 450))
    

