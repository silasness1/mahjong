import tkinter as tk
from PIL import Image, ImageTk

def resize_rotate_image(image_path:str, degrees:int, target_width:int, target_height:int)-> ImageTk:
    """wrapper for creating a PhotoImage that makes the image smaller or bigger depending on the target size while preserving the aspect ratio"""

    # Load and rotate image
    img = Image.open(image_path)
    rotated = img.rotate(degrees, expand=True)

    # Convert to RGBA to ensure transparency info is preserved
    rotated = rotated.convert("RGBA")

    # Get the bounding box of the non-transparent area
    bbox = rotated.getbbox()

    # Crop the rotated image to its bounding box
    rotated = rotated.crop(bbox)

    # Get the current image size
    rotated_width = rotated.width
    rotated_height = rotated.height
    
    # Calculate the aspect ratio
    rotated_width = rotated.width
    aspect_ratio = rotated_width / rotated_height
    
    # Calculate the new width and height while preserving the aspect ratio
    if rotated_width > target_width or rotated_height > target_height:
        if rotated_width / target_width > rotated_height / target_height:
            # Use subsample for width
            new_width = target_width
            new_height = int(target_width / aspect_ratio)
        else:
            # Use subsample for height
            new_height = target_height
            new_width = int(target_height * aspect_ratio)
    else:
        # Use zoom for enlarging
        new_width = target_width
        new_height = target_height

    resized_rotated_image = rotated.resize((new_width, new_height))

    return ImageTk.PhotoImage(resized_rotated_image)
    

class TileImage: 
    """Tile class for the gui
    
    params:
    - `canvas`: the canvas to draw on
    - `x`: x coordinate for where the tile should be
    - `y`: y coordinate for where the tile should be
    - `draggable`: whether the tile is draggable or not
    - `suit`: the suit of the tile in ['Bam', 'Ball', 'Crack']
    - `rank`: the rank of the tile in [1, 9]
    - `orientation`: the orientation of the tile in ['bottom', 'right', 'top', 'left']
    - `grid_size`: the size of the grid to snap to
    - `play_area`: the area to snap to in (x1, y1, x2, y2)
    - `max_tile_width`: the maximum width of the tile
    - `max_tile_height`: the maximum height of the tile
    - `image_path`: the path to the image of the tile
    - `tile`: the tile object
    - `tile_photo`: the tile image object

    Relationship with TileCollection class
        - expecting to use play_area from TileCollection so that tile only snaps within the collection
        - 
    """

    image_dict = { 
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
    orientation_dict = {"bottom": 0, "right": 90, "top": 180, "left": 270}

    def __init__(self, canvas, x, y, draggable:bool, suit:str, rank:int, orientation: str, grid_size_x, grid_size_y, play_area:tuple[int,int,int,int], max_tile_width=50, max_tile_height=50):

        assert orientation in ['bottom', 'right', 'top', 'left']
        assert suit in ["Bam", "Ball", "Crack"], "suit must be 'Bam', 'Ball', or 'Crack'"
        assert rank in [i for i in range(1, 10)], "rank must be between 1 and 9"

        self.canvas = canvas
        self.draggable = draggable
        self.x = x
        self.y = y
        self.grid_size_x = grid_size_x
        self.grid_size_y = grid_size_y
        self.play_area = play_area
        self.suit = suit
        self.rank = rank
        self.orientation = orientation

        self.start_x = x
        self.start_y = y

        # image
        self.image_path = self.image_dict[(suit, rank)]
        self.degrees = self.orientation_dict[orientation]
        self.tile_photo = resize_rotate_image(self.image_path, self.degrees, max_tile_width, max_tile_height)
        self.tile = self.canvas.create_image(x, y, image=self.tile_photo)

        # rectangle approach to tiles
        # self.tile = self.canvas.create_rectangle(x, y, x+50, y+60, fill='red')     

        if draggable:
            # makes clickable
            self.canvas.tag_bind(self.tile, "<Button-1>", lambda event: print("Rectangle clicked!"))

            # Bind events for dragging
            self.canvas.tag_bind(self.tile, "<ButtonPress-1>",  lambda event: self.start_drag(event))
            self.canvas.tag_bind(self.tile, "<B1-Motion>",  lambda event: self.on_drag(event))
            self.canvas.tag_bind(self.tile, "<ButtonRelease-1>", lambda event: self.snap_tile(event))
                
    def start_drag(self, event):
        """Store the initial click position."""
        self.start_x = event.x
        self.start_y = event.y


    def on_drag(self, event):
        """Move the rectangle based on mouse movement."""
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        self.canvas.move(self.tile, dx, dy)

        # Update start position
        self.start_x = event.x
        self.start_y = event.y

    def snap_tile(self, event):
        """ Snap the tile to the nearest grid position and check boundaries. """
        # Calculate grid coordinates
        new_x = (event.x // self.grid_size_x) * self.grid_size_x
        new_y = (event.y // self.grid_size_y) * self.grid_size_y

        # Snap to grid but ensure it's within the play area
        new_x = max(self.play_area[0], min(new_x, self.play_area[2] - self.tile_photo.width()))
        new_y = max(self.play_area[1], min(new_y, self.play_area[3] - self.tile_photo.height()))

        # Move the tile to the snapped position
        self.canvas.coords(self.tile, new_x + self.tile_photo.width() // 2, new_y + self.tile_photo.height() // 2)
        
        print(f"Rectangle dropped at ({event.x}, {event.y})")



