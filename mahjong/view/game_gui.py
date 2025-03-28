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

    def create_frame(self, width=500, height=400):
        """creates background"""
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg="green")
        self.canvas.pack() # puts canvas in root
    
    def create_drag_tile(self):
        """creates a draggable tile"""
        my_tile = DragTile(self.canvas, 100, 100, "view/tile_images/Man1.png")
    

