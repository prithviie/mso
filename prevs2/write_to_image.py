from PIL import Image
import numpy as np


def generate_map_with_path(map_image, output_image, path_coordinates, path_color):
    '''Creates an image file with the path drawn over the given path coordinates'''

    im = Image.open(map_image)
    px = im.load()
    w, h = im.size

    pixels = []

    for x in range(h):
        pixels.append([])
        for y in range(w):
            pixels[x].append(px[y, x])

    for co in path_coordinates:
        x, y = co
        pixels[y-1][x-1] = path_color


    array = np.array(pixels, dtype=np.uint8)

    new_image = Image.fromarray(array)
    new_image.save(output_image)










