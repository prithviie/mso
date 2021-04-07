from PIL import Image
import numpy as np


def get_neighbours(px, co, w, h):
    '''given a pixel co ordinate, returns the adjacent co ordinates (neighvours) for the given co ordinate'''
    '''returns a list of tuples'''

    x, y = co
    #              top       bottom     left      right
    neighbours = [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]

    final_neighbours = []

    for neighbour in neighbours:

        if neighbour[0] >= w or neighbour[1] >= h:
            continue
        else:
            # if pixel aint white then its a neighbour
            if not px[neighbour] == (255, 255, 255, 255):
                final_neighbours.append(neighbour)

    return final_neighbours


def generate_map_with_path(map_image, output_image, path_coordinates, path_color):
    '''Creates an image file with the path drawn over the given path coordinates'''
    # print(path_coordinates)

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


def generate_map_with_broad_path(map_image, output_image, path_coordinates, path_color):

    im = Image.open(map_image)
    px = im.load()
    w, h = im.size
    pixels = []

    # reading through image to read pixels
    for x in range(h):
        pixels.append([])
        for y in range(w):
            pixels[x].append(px[y, x])
            
            # to find path ---- will be removed
            # if px[y, x] == (255, 0, 0, 255):
            #     path_coordinates.append((y, x))

    broad_path = []

    for cor in path_coordinates:
        first_neighbours = get_neighbours(px, cor, w, h)

        for neighbour1 in first_neighbours:
            second_neighbours = get_neighbours(px, neighbour1, w, h)

            for neighbour2 in second_neighbours:
                third_neighbours = get_neighbours(px, neighbour2, w, h)

                for neighbour3 in third_neighbours:
                    broad_path.append(neighbour3)

    # final replacements
    for cor in broad_path:
        x, y = cor
        pixels[y][x] = path_color

    array = np.array(pixels, dtype=np.uint8)
    new_image = Image.fromarray(array)
    new_image.save(output_image)


map_image = 'test.png'
output_image = 'output.png'
path = []
color = (255, 0, 0, 255)

generate_map_with_broad_path(map_image, output_image, path, color)
