import tkinter as tk


def resize_image(image_path, target_width, target_height):
    # Load the image
    img = tk.PhotoImage(file=image_path)
    
    # Get the current image size
    img_width = img.width()
    img_height = img.height()
    
    # Calculate the aspect ratio
    aspect_ratio = img_width / img_height
    
    # Calculate the new width and height while preserving the aspect ratio
    if img_width > target_width or img_height > target_height:
        if img_width / target_width > img_height / target_height:
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
    
    # Resize using subsample (for reduction) or zoom (for enlargement)
    if new_width < img_width or new_height < img_height:
        img_resized = img.subsample(int(img_width / new_width), int(img_height / new_height))
    else:
        img_resized = img.zoom(int(new_width / img_width), int(new_height / img_height))
    
    return img_resized

class DragTile: 
    """Tile class for the gui"""
    def __init__(self, canvas, x, y, image_path, grid_size, play_area, max_tile_width=50, max_tile_height=50):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.image_path = image_path
        self.grid_size = grid_size
        self.play_area = play_area

        self.start_x = x
        self.start_y = y

        # image
        self.tile_photo = resize_image(self.image_path, max_tile_width, max_tile_height)
        self.tile = self.canvas.create_image(x, y, image=self.tile_photo)

        # rectangle approach to tiles
        # self.tile = self.canvas.create_rectangle(x, y, x+50, y+60, fill='red')     

        # makes clickable
        self.canvas.tag_bind(self.tile, "<Button-1>", lambda event: print("Rectangle clicked!"))

        # makes draggable
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
        new_x = (event.x // self.grid_size) * self.grid_size
        new_y = (event.y // self.grid_size) * self.grid_size

        # Snap to grid but ensure it's within the play area
        new_x = max(self.play_area[0], min(new_x, self.play_area[2] - self.tile_photo.width()))
        new_y = max(self.play_area[1], min(new_y, self.play_area[3] - self.tile_photo.height()))

        # Move the tile to the snapped position
        self.canvas.coords(self.tile, new_x + self.tile_photo.width() // 2, new_y + self.tile_photo.height() // 2)
        
        print(f"Rectangle dropped at ({event.x}, {event.y})")



