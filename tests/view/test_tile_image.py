from mahjong.view.tile_image import TileImage, resize_rotate_image
import pytest

import tkinter as tk
from unittest.mock import patch  # ,MagicMock

# Fixture for initializing a TileImage object
@pytest.fixture
def example_tile():

    root = tk.Tk()
    
    #create frame
    canvas = tk.Canvas(root, width=500, height=400, bg="green")
    canvas.pack() # puts canvas in root
    
    return TileImage(
        canvas=canvas, 
        x=100, 
        y=100, 
        draggable=True, 
        suit="Bam",
        rank=9, 
        orientation="bottom",
        grid_size_y=50,
        grid_size_x=50,
        play_area=(50, 50, 450, 450),
        max_tile_width=50,
        max_tile_height=50
    )

import tkinter as tk

def test_drag_simulation():
    """Example test to simulate a drag event in Tkinter"""
    root = tk.Tk()
    canvas = tk.Canvas(root, width=400, height=300)
    canvas.pack()

    state = {'dragged': False}

    def on_drag_start(event):
        state['dragged'] = True

    canvas.bind("<ButtonPress-1>", on_drag_start)

    def run_test():
        # Simulate drag start
        canvas.event_generate("<ButtonPress-1>", x=50, y=50)

        # Perform your assertions here
        assert state['dragged'] == True, "Drag handler didn't update state"

        print("✅ Test passed.")
        root.destroy()  # Exit the mainloop after test

    # Schedule the test to run after mainloop starts
    root.after(1000, run_test)

    root.mainloop()


def test_rotate_resize():
    """Test the rotate and resize method of the TileImage class"""
    root = tk.Tk()
    canvas = tk.Canvas(root, width=500, height=400, bg="green")
    canvas.pack()

    img = resize_rotate_image("/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Sou9.png", 90, 50, 50)
    canvas.create_image(100, 100, image=img)
    root.mainloop()
    
    assert img is not None

def test_init_run(example_tile):
    """Test the initialization of the TileImage class"""
    assert example_tile.canvas is not None
    assert example_tile.x == 100
    assert example_tile.y == 100
    assert example_tile.draggable == True
    assert example_tile.suit == "Bam"
    assert example_tile.rank == 9
    assert example_tile.orientation == "bottom"
    assert example_tile.grid_size_x == 50
    assert example_tile.grid_size_y == 50
    assert example_tile.play_area == (50, 50, 450, 450)
    # assert example_tile.max_tile_width == 50
    # assert example_tile.max_tile_height == 50
    assert example_tile.image_path == "/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Sou9.png"