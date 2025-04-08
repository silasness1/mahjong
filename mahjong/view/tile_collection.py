from mahjong.view.tile_image import TileImage
from tkinter import Canvas

class TileCollection:
    """An area on the board that contains tiles. 
    
    params: 
    - `anchorpoint`: "topleft" "topright" "bottomleft" "bottomright"
    - `position_x`: x coordinate for where the anchorpoint should be
    - `position_y` : y coordinate for where the achorpoint should be 
    - `num_tiles_x` : how many tiles the grid wide in the x direction is wide
    - `num_tiles_y` : how many tiles the grid is high in the y direction
    - `tile_orientation`: "top", "left", "bottom", "right" - the direction which the bottom of the tile images are facing
    - `tile_collection`: a list of TileImage objects 
    """

    def __init__(self, canvas:Canvas, anchorpoint:str, position_x, position_y, num_tiles_x, num_tiles_y, tile_orientation:str, tile_collection:list[TileImage]):

        assert tile_orientation in ["top", "bottom", "left", "right"], "tile_orientation must be 'horizontal' or 'vertical'"
        assert anchorpoint in ["topleft", "topright", "bottomleft", "bottomright"], "anchorpoint must be 'topleft', 'topright', 'bottomleft', or 'bottomright'"
        # assert isinstance(tile_collection, list), "tile_collection must be a list of TileImage objects"
        

        self.anchorpoint=anchorpoint
        self.position_x=position_x
        self.position_y=position_y
        self.num_tiles_x=num_tiles_x
        self.num_tiles_y=num_tiles_y
        self.tile_orientation=tile_orientation
        self.tile_collection=tile_collection

        # create drop regions
        # snappable grid 
        self.grid_size = 50
        self.tile_width = 40
        self.tile_height = 40
        self.play_area = (50, 50, 450, 450)  # (x1, y1, x2, y2)