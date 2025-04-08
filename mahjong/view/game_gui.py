from tkinter import *
from tkinter import ttk
import tkinter as tk
from mahjong.view.tile_image import TileImage

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



    
    def create_tile(self, suit:str, rank:int, x = 100, y = 100, grid_size_x = 50, grid_size_y =50, play_area = (50, 50, 450, 450), max_tile_width = 50, max_tile_height = 50, orientation = "bottom"):
        """creates a draggable tile at position x, y"""
        
        my_tile = TileImage(self.canvas, 
                            x, 
                            y, 
                            draggable=True,
                            suit=suit, 
                            rank=rank, 
                            orientation=orientation,
                            grid_size_x=grid_size_x, 
                            grid_size_y=grid_size_y,
                            play_area=play_area, 
                            max_tile_height=max_tile_height, 
                            max_tile_width=max_tile_width)


    def render_game_state(self):
        """updates the screen too reflect tiles in graveyard and player hands

        checks to see if player's tile collection is functionally the same as their model hand. 

        if not, update the local hand either by popping extra tiles or adding drawn tiles to the end so as to preserve player reordering preferences
        """

    

    
    def render_hand(self, player_hand):
        """updates the screen to reflect the player's hand"""
        pass

    def render_graveyard(self, graveyard):
        """updates the screen to reflect the graveyard"""

    def query_player_hand(self):
        """returns the current player's hand"""
        pass

    def query_graveyard(self):
        """returns the current graveyard"""
        pass

    def query_gamestate(self):
        """returns the current game state"""
        
        for player in player_list:
            self.query_player_hand(player)
     
        self.query_graveyard()
    
        pass


    

