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

        self.image_dict = { 
                            ("Bam", 1): "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Sou1.png",
                            ("Bam", 2): "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Sou2.png",
                            ("Bam", 3): "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Sou3.png",
                            ("Bam", 4): "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Sou4.png",
                            ("Bam", 5): "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Sou5.png",
                            ("Bam", 6): "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Sou6.png",
                            ("Bam", 7): "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Sou7.png",
                            ("Bam", 8): "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Sou8.png",
                            ("Bam", 9): "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Sou9.png",
                            ("Ball", 1): "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Pin1.png",
                            ("Ball", 2): "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Pin2.png",
                            ("Ball", 3): "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Pin3.png",
                            ("Ball", 4): "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Pin4.png",
                            ("Ball", 5): "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Pin5.png",
                            ("Ball", 6): "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Pin6.png",
                            ("Ball", 7): "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Pin7.png",
                            ("Ball", 8): "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Pin8.png",
                            ("Ball", 9): "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Pin9.png",
                            ("Crack", 1): "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Man1.png",
                            ("Crack", 2): "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Man2.png",
                            ("Crack", 3): "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Man3.png",
                            ("Crack", 4): "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Man4.png",
                            ("Crack", 5): "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Man5.png",
                            ("Crack", 6): "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Man6.png",
                            ("Crack", 7): "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Man7.png",
                            ("Crack", 8): "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Man8.png",
                            ("Crack", 9): "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Man9.png",
                    }

    
    def create_drag_tile(self, suit:str, rank:int, x = 100, y = 100, grid_size = 50, play_area = (50, 50, 450, 450), max_tile_width = 50, max_tile_height = 50):
        """creates a draggable tile at position x, y"""
        image_path = self.image_dict[(suit, rank)]
        my_tile = DragTile(self.canvas, x, y, 
        image_path=image_path, grid_size=grid_size, play_area=play_area, max_tile_height=max_tile_height, max_tile_width=max_tile_width)


    def render_others_closed(self):
        "shows the backs of tiles for other 3 non-active players in closed-hand"
    

