from tkinter import *
from tkinter import ttk
import tkinter as tk

class MahjongGui:

    def __init__(self):
        self.root = Tk()
        self.root.title("Mahjong Game")

    def create_frame(self):

        
    def start_drag(event):
        """Store the initial click position."""
        global start_x, start_y
        start_x = event.x
        start_y = event.y


def on_drag(event):
    """Move the rectangle based on mouse movement."""
    global start_x, start_y
    dx = event.x - start_x
    dy = event.y - start_y
    canvas.move(tile_example, dx, dy)

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


canvas = tk.Canvas(root, width=500, height=400, bg="green")
canvas.pack()  # puts canvas in root

# rectangle
# rect_id = canvas.create_rectangle(50, 50, 150, 100, fill="blue")

# image
# tile_example_photo = load_resized_image("frontend/tile_images/Man1.png", 100)
tile_example_photo = tk.PhotoImage(file="frontend/tile_images/Man1.png")
print(tile_example_photo.width(), tile_example_photo.height())
tile_example_photo = tile_example_photo.subsample(4)
tile_example = canvas.create_image(100, 100, image=tile_example_photo)

# makes clickable
canvas.tag_bind(tile_example, "<Button-1>", lambda event: print("Rectangle clicked!"))

# makes draggable
# Bind events for dragging
canvas.tag_bind(tile_example, "<ButtonPress-1>", start_drag)
canvas.tag_bind(tile_example, "<B1-Motion>", on_drag)
canvas.tag_bind(tile_example, "<ButtonRelease-1>", stop_drag)

root.mainloop()
