import tkinter as tk

class DragTile: 
    """Tile class for the gui"""
    def __init__(self, canvas, x, y, image_path):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.image_path = image_path

        # image
        tile_photo = tk.PhotoImage(file=self.image_path)
        tile_photo = tile_photo.subsample(4)
        self.tile = self.canvas.create_image(100, 100, image=tile_photo)

        # makes clickable
        self.canvas.tag_bind(self.tile, "<Button-1>", lambda event: print("Rectangle clicked!"))

        # makes draggable
        # Bind events for dragging
        self.canvas.tag_bind(self.tile, "<ButtonPress-1>", self.start_drag)
        self.canvas.tag_bind(self.tile, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.tile, "<ButtonRelease-1>", self.stop_drag)
                
    def start_drag(event):
        """Store the initial click position."""
        global start_x, start_y
        start_x = event.x
        start_y = event.y


    def on_drag(event,self):
        """Move the rectangle based on mouse movement."""
        global start_x, start_y
        dx = event.x - start_x
        dy = event.y - start_y
        self.canvas.move(self.tile, dx, dy)

        # Update start position
        start_x = event.x
        start_y = event.y


    def stop_drag(event):
        """Optional: Trigger an event when dragging stops."""
        print(f"Rectangle dropped at ({event.x}, {event.y})")

# def load_resized_image(file_path, max_size):
#     image = tk.PhotoImage(file_path)

#     # Resize while maintaining aspect ratio
#     aspect_ratio = image.height() / image.width()
#     if image.height() > image.width():
#         new_height = max_size
#         new_width = int(new_height / aspect_ratio)
#     else:
#         new_width = max_size
#         new_height = int(new_width * aspect_ratio)

#     image = image.zoom(new_width // image.width(), new_height // image.height())

#     return image




# rectangle
# rect_id = canvas.create_rectangle(50, 50, 150, 100, fill="blue")




