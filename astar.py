from queue import PriorityQueue
from PIL import Image
import numpy as np

locs_with_cors = {1: ['Tennis court', (214, 248, 10), (37, 397)],
                  2: ['Gym', (145, 162, 44), (109, 397)],
                  3: ['Basketball court', (73, 76, 53), (153, 397)],
                  4: ['Hockeycourt', (21, 24, 0), (229, 397)],
                  5: ['Yampa/PNB', (9, 231, 227), (185, 451)],
                  6: ['Football ground', (81, 122, 121), (345, 397)],
                  7: ['Golden Jubilee Bhavan', (160, 246, 244), (497, 397)],
                  8: ['MBA block', (233, 160, 246), (592, 421)],
                  9: ['Boys hostel', (191, 56, 215), (63, 354)],
                  10: ['Parking', (76, 8, 88), (188, 335)],
                  11: ['Garden', (208, 60, 60), (218, 393)],
                  12: ['Garden2', (249, 13, 13), (274, 394)],
                  13: ['Temple', (98, 0, 0), (189, 298)],
                  14: ['Quadrangle/Assembly Hall', (207, 104, 104), (243, 301)],
                  15: ['Admin block', (86, 16, 16), (212, 368)],
                  16: ['Civil Dept.', (138, 105, 105), (301, 331)],
                  17: ['ENV+IP+Polymer Dept.', (38, 128, 49), (359, 367)],
                  18: ['Mech+EE Dept.', (80, 241, 99), (254, 297)],
                  19: ['Polytech hostel', (71, 109, 76), (407, 62)],
                  20: ['Polytech block', (10, 40, 14), (437, 55)],
                  21: ['Cricket ground', (159, 208, 166), (480, 109)],
                  22: ['Vuon Tech', (159, 172, 208), (405, 262)],
                  23: ['SJCE-STEP', (75, 116, 231), (405, 344)],
                  24: ['Mylari', (211, 138, 249), (508, 354)],
                  25: ['PDA block', (27, 31, 42), (617, 393)],
                  26: ['Womens Polytechnic college', (1, 4, 11), (641, 410)],
                  27: ['Canteen1', (9, 53, 156), (643, 332)],
                  28: ['Staff quarters', (43, 28, 51), (645, 268)],
                  29: ['JSS School', (17, 4, 24), (627, 34)],
                  30: ['Canteen2', (154, 109, 178), (514, 56)],
                  31: ['Gate1', (154, 109, 178), (184, 470)],
                  32: ['Gate2', (46, 19, 60), (632, 477)],
                  33: ['Parking2', (25, 80, 96), (367, 393)],
                  34: ['Nescafe', (189, 57, 131), (330, 297)]}


class Node():

    # states:
    # . -> nothing yet (available path)
    # s -> start
    # e -> end
    # 0 -> barrier
    # '+' -> reconstructed path
    # closed -> closed
    # open -> open
    # '#'no -> location number

    def __init__(self, x, y, total_cols, total_rows):
        self.x = x
        self.y = y
        self.total_rows = total_rows
        self.total_cols = total_cols
        self.state = '.'
        self.neighbours = []

    def get_pos(self):
        return self.x, self.y

    def make_start(self):
        self.state = 's'

    def make_end(self):
        self.state = 'e'

    def make_barrier(self):
        self.state = '0'

    def make_path(self):
        self.state = '+'

    def make_closed(self):
        self.state = 'closed'

    def make_open(self):
        self.state = 'open'

    def reset(self):
        self.state = '.'

    def is_barrier(self):
        return self.state == '0'

    def is_start(self):
        return self.state == 's'

    def is_end(self):
        return self.state == 'e'

    def update_neighbours(self, grid):
        '''checking neighbouring nodes in the grid to check if they are barriers or available path'''
        self.neighbours = []
        # BOTTOM neighbour
        if self.x < self.total_cols - 1 and not grid[self.x + 1][self.y].is_barrier():
            self.neighbours.append(grid[self.x + 1][self.y])

        if self.x > 0 and not grid[self.x - 1][self.y].is_barrier():  # TOP neighbour
            self.neighbours.append(grid[self.x - 1][self.y])

        # RIGHT neighbour
        if self.y < self.total_rows - 1 and not grid[self.x][self.y + 1].is_barrier():
            self.neighbours.append(grid[self.x][self.y + 1])

        if self.y > 0 and not grid[self.x][self.y - 1].is_barrier():  # LEFT neighbour
            self.neighbours.append(grid[self.x][self.y - 1])

    def __str__(self):
        return str(self.state)


def h(p1, p2):
    '''Hueristic function- returns the manhattan distance between any given two points'''
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)


def make_grid(width, height):
    '''returns a 2D array (grid) of nodes'''
    grid = []

    for x in range(height):
        grid.append([])
        for y in range(width):
            node = Node(x, y, height, width)
            grid[x].append(node)

    return grid


def draw_grid(grid, width, height):
    '''draws the grid'''

    for x in range(height):
        for y in range(width):
            print(grid[x][y], end='  ')
        print('\n')


def choose_loc(dic, point):
    '''prompts the user to choose a location- returns the color code of location from the dic'''
    for key in dic:
        print(f"{key}: {dic[key][0]}")

    chosen = input(f"Choose the {point} point (enter number): ")
    # returning the color code for chosen position
    color_code = dic.get(int(chosen))[1]
    # print(color_code)

    return color_code


def update_grid_with_start_end_gui(map_image, grid, height, width, dic, start_cc, end_cc):
    '''sets the start and end node on the grid and returns the grid and start and end nodes'''

    def neighbour_satisfied(px, x, y):
        '''for a given node- it checks the adjacent nodes if they are black, returns True/False accordingly'''

        if px[y, x-1] == (0, 0, 0, 255) and px[y, x+1] == (0, 0, 0, 255) \
                and px[y-1, x] == (0, 0, 0, 255) and px[y+1, x] == (0, 0, 0, 255):

            return True

        return False

    start_color_code = start_cc
    sr, sg, sb = start_color_code
    end_color_code = end_cc
    er, eg, eb = end_color_code

    im = Image.open(map_image)
    px = im.load()

    start, end = 0, 0

    for x in range(height):
        for y in range(width):
            node = grid[x][y]
            if px[y, x][0] == sr and px[y, x][1] == sg and px[y, x][2] == sb and neighbour_satisfied(px, x, y):
                node.make_start()
                start = node
            elif px[y, x][0] == er and px[y, x][1] == eg and px[y, x][2] == eb and neighbour_satisfied(px, x, y):
                node.make_end()
                end = node

    if start and end:
        return grid, start, end

    elif start and not end:
        print('start set')
        return grid, start, None

    elif not start and end:
        print('end set')
        return grid, None, end

    else:
        print('both not set')
        return grid, None, None


def set_start_and_end(map_image, grid, height, width, dic):
    '''sets the start and end node for the algorithm, if not found returns None'''

    def neighbour_satisfied(px, x, y):
        '''for a given node- it checks the adjacent nodes if they are black, returns True/False accordingly'''

        if px[y, x-1] == (0, 0, 0, 255) and px[y, x+1] == (0, 0, 0, 255) \
                and px[y-1, x] == (0, 0, 0, 255) and px[y+1, x] == (0, 0, 0, 255):

            return True

        return False

    start_color_code = choose_loc(dic, "start")
    sr, sg, sb = start_color_code
    end_color_code = choose_loc(dic, "end")
    er, eg, eb = end_color_code

    im = Image.open(map_image)
    px = im.load()

    start, end = 0, 0

    for x in range(height):
        for y in range(width):
            node = grid[x][y]
            if px[y, x][0] == sr and px[y, x][1] == sg and px[y, x][2] == sb and neighbour_satisfied(px, x, y):
                node.make_start()
                start = node
            elif px[y, x][0] == er and px[y, x][1] == eg and px[y, x][2] == eb and neighbour_satisfied(px, x, y):
                node.make_end()
                end = node

    if start and end:
        return grid, start, end

    elif start and not end:
        print('start set')
        return grid, start, None

    elif not start and end:
        print('end set')
        return grid, None, end

    else:
        print('both not set')
        return grid, None, None


def preset_barriers(map_image, width, height):
    '''reads through the image file and creates a grid of Nodes acoording to the color and 
    sets the Node state acoordingly. Returns a grid of nodes'''

    def is_black(img_px, x, y):
        if img_px[y, x][0] <= 5 and img_px[y, x][1] <= 5 and img_px[y, x][2] <= 5:
            return True
        return False

    im = Image.open(map_image)
    px = im.load()

    grid = []

    for x in range(height):
        grid.append([])
        for y in range(width):

            node = Node(x, y, height, width)
            if is_black(px, x, y):
                node.state = '.'
            else:
                node.state = '0'

            grid[x].append(node)

    return grid

    # map = [['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    #        ['0', '0', '.', '.', '.', '.', '.', '.', '.', '.',
    #         '.', '.', '.', '.', '.', '.', '.', '.', '.', '0'],
    #        ['0', '0', '.', '0', '0', '0', '0', '0', '.', '0',
    #         '0', '0', '0', '0', '0', '0', '0', '0', '.', '0'],
    #        ['0', '0', '.', '0', '0', '0', '0', '0', '.', '0',
    #         '0', '0', '0', '0', '0', '0', '0', '0', '.', '0'],
    #        ['0', '0', '.', '0', '0', '0', '0', '0', '.', '0',
    #         '0', '0', '0', '0', '0', '0', '0', '0', '.', '0'],
    #        ['0', '0', '.', '0', '0', '0', '0', '0', '.', '0',
    #         '0', '0', '0', '0', '0', '0', '0', '0', '.', '0'],
    #        ['0', '0', '.', '0', '0', '0', '0', '0', '.', '0',
    #         '0', '0', '0', '0', '0', '0', '0', '0', '.', '0'],
    #        ['0', '0', '.', '0', '0', '0', '0', '0', '.', '.',
    #         '.', '.', '.', '.', '.', '.', '.', '.', '.', '0'],
    #        ['0', '0', '.', '0', '0', '0', '0', '0', '0', '0',
    #         '0', '0', '0', '0', '0', '0', '0', '0', '.', '0'],
    #        ['0', '0', '.', '0', '0', '0', '0', '0', '0', '0',
    #         '0', '0', '0', '0', '0', '0', '0', '0', '.', '0'],
    #        ['0', '0', '.', '.', '.', '.', '.', '.', '.', '.',
    #         '.', '.', '.', '.', '.', '.', '.', '.', '.', '0'],
    #        ['0', '0', '.', '0', '0', '0', '0', '0', '0', '0',
    #         '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    #        ['0', '0', '.', '0', '0', '0', '0', '0', '0', '0',
    #         '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    #        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
    #         '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
    #        ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']]

    # grid = []
    # for x in range(height):
    #     grid.append([])
    #     for y in range(width):
    #         node = Node(x, y, height, width)
    #         node.state = map[x][y]
    #         grid[x].append(node)

    # returns a 2d matrix containing nodes -- not values

    # return grid


def reconstruct_path(came_from, current, start, draw_grid):
    '''Reconstructs the path with state = '+', returns a list of co ordinates of the path constructed'''

    path_cos = []

    end = current
    while current in came_from:
        current = came_from[current]
        current.make_path()

        # to get cos of path constructed
        x, y = current.get_pos()
        x, y = x + 1, y + 1
        path_cos.append((y, x))

    start.make_start()
    end.make_end()
    # draw_grid()

    # print('recons')
    # print(path_cos)
    # print()

    return path_cos[:len(path_cos)-1]


def generate_map_with_broad_path(map_image, output_image, path_coordinates, path_color):
    '''Creates an image file with the path drawn over the given path coordinates (broad path)'''

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

    im = Image.open(map_image)
    px = im.load()
    w, h = im.size
    pixels = []

    # reading through image to read pixels
    for x in range(h):
        pixels.append([])
        for y in range(w):
            pixels[x].append(px[y, x])

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


def algorithm(draw_grid, grid, start, end):
    '''The algorithm takes in 2D grid of nodes, the start node and the end node, returns the co-ordinates of the shortest path found'''
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            path_cos = reconstruct_path(came_from, end, start, draw_grid)
            if path_cos:
                return path_cos
            # return True

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + \
                    h(neighbour.get_pos(), end.get_pos())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    # neighbour.make_open()

        # if current != start:
        #     # current.make_closed()
        #     pass

    return False


def main(width, height, map_image, output_image, locs_with_cors):

    grid = preset_barriers(map_image, width, height)

    grid, start, end = set_start_and_end(
        map_image, grid, height, width, locs_with_cors)

    if start and end:
        print('start and end set')
        for row in grid:
            for node in row:
                node.update_neighbours(grid)
        print('neighbours updated')

        try:
            print('trying to find path')
            path_cos = algorithm(lambda: draw_grid(
                grid, width, height), grid, start, end)
            if path_cos:
                print('path found')
                generate_map_with_broad_path(
                    map_image, output_image, path_cos, (255, 0, 0, 255))
            else:
                print('path not found')

        except Exception as e:
            print(e)

    else:
        # print('Start or end not set')
        pass


map_image = 'final-map.png'
output_image = 'final-output-from-astar.png'

im = Image.open(map_image)
WIDTH, HEIGHT = im.size

if __name__ == '__main__':
    main(WIDTH, HEIGHT, map_image, output_image, locs_with_cors)
