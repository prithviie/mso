from PIL import Image

# '''to basically create the preset matrix for the astar file'''


def get_red_pixel(img_px, x, y):
    return px[y, x][0]


def get_green_pixel(img_px, x, y):
    return px[y, x][1]


def get_blue_pixel(img_px, x, y):
    return px[y, x][2]


def is_black(img_px, x, y):
    return img_px[y, x][0] == 0 and img_px[y, x][1] == 0 and img_px[y, x][2] == 0


def is_white(img_px, x, y):
    return img_px[y, x][0] == 255 and img_px[y, x][1] == 255 and img_px[y, x][2] == 255


def write_to_file(f, char, i, j, w, h):

    if j == 0:
        f.write("['{}', ".format(char))
    elif j == w-1 and i == h-1:
        f.write("'{}']".format(char))
    elif j == w-1:
        f.write("'{}'],".format(char))
    else:
        f.write("'{}', ".format(char))


def write_matrix_to_file(map_image, output_file):
    barrier = '0'
    nothing = '.'

    im = Image.open(map_image)
    px = im.load()
    w, h = im.size

    with open(output_file, 'w+') as f:
        f.write('[')

        for i in range(h):
            for j in range(w):

                if is_black(px, i, j):
                    char = nothing
                    write_to_file(f, char, i, j, w, h)

                else:
                    char = barrier
                    write_to_file(f, char, i, j, w, h)

            if i != h-1:
                f.write('\n')

        f.write(']')


def create_preset_matrix(map_image):
    im = Image.open(map_image)
    px = im.load()
    w, h = im.size
    matrix = []

    for i in range(h):
        matrix.append([])
        for j in range(w):

            if is_black(px, i, j):
                char = '.'
            else:
                char = '0'

            matrix[i].append(char)

    return matrix


map_file = 'final-map.png'

write_matrix_to_file(map_file, 'preset-matrix.txt')


# matrix = create_preset_matrix(map_file)

# for f in matrix:
#     for j in f:
#         print(j, end='  ')
#     print('\n')
