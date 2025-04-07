from PIL import Image
import os

def autocrop_transparent(input_path, output_path=None):
    image = Image.open(input_path).convert("RGBA")
    bbox = image.getbbox()  # bounding box of non-transparent pixels
    if bbox:
        cropped = image.crop(bbox)
        if output_path:
            cropped.save(output_path)
        else:
            cropped.save(input_path)  # overwrite original

# Example usage
autocrop_transparent("img/player1.png")
autocrop_transparent("img/player2.1.gif")
