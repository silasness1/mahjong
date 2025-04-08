import tkinter as tk 
from mahjong.view.tile_image import resize_rotate_image

root = tk.Tk()
canvas = tk.Canvas(root, width=500, height=400, bg="green")
canvas.pack()

img = resize_rotate_image("/home/schmoopsan/dev/mahjong/mahjong/view/tile_images/with_background/Sou9.png", 90, 50, 50)
canvas.create_image(100, 100, image=img)

root.mainloop()