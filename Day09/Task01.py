import os
import re
import math
import numpy as np
day = 9# Input day here

test = False # Change this to run program with the smaller testinput for debug
DEBUG = False # Change this to have debug outputs
OUTPUT_DATA = False

root = os.getcwd()
if(os.path.basename(root) != 'AdventOfCode2025'):
    root = os.path.normpath(os.path.join(root, '..'))
current_day = os.path.join(root, f"Day{day:02d}")
if test:
    input_path = os.path.join(current_day, 'test.txt')
else:
    input_path = os.path.join(current_day, 'Input.txt')
output_path = os.path.join(current_day, 'Output.txt')

def draw_grid(red_tiles, square_coords=None):
    grid_size = red_tiles.max() +1
    grid = np.zeros((grid_size, grid_size))
    for tile in red_tiles:
        grid[tile[0]][tile[1]] = 1

    if(square_coords != None):
        (corner_1, corner_2) = square_coords
        xmin = min(corner_1[0], corner_2[0])
        xmax = max(corner_1[0], corner_2[0])
        ymin = min(corner_1[1], corner_2[1])
        ymax = max(corner_1[1], corner_2[1])
        for x in range(xmin, xmax+1):
            for y in range(ymin, ymax+1):
                grid[x][y] = -1
    #grid = np.rot90(grid)
    out = "Grid:\n"
    #draw coordinates:
    no_of_digits = len(str(grid_size))
    coord_array = np.empty((grid_size, no_of_digits), dtype=str)
    for i in range(grid_size):
        for j in range(no_of_digits):
            if(no_of_digits-j > len(str(i))):
                coord_array[i][j] = ' '
            else:
                coord_array[i][j] = f'{i:0{no_of_digits}d}'[j]

    for j in range(no_of_digits):
        out += ' ' * no_of_digits
        for i in range(grid_size):
            out += coord_array[i][j]
        out += '\n'
    
    for y in reversed(range(grid_size)):
        #coordinates:
        for j in range(no_of_digits):
            out += coord_array[y][j]
        for x in range(grid_size):
            tile = grid[x][y]
            if tile < 0:
                out += 'O'
            elif tile > 0:
                out += '#'
            else:
                out += '.'
        out += '\n'

    return out

    


def process_input(input):
    out = ''

    redtiles = []
    for line in input.split('\n'):
        tiles = []
        for tile in line.split(','):
            loc = int(tile)
            tiles.append(loc)
        redtiles.append(tiles)
    redtiles = np.array(redtiles)
    if OUTPUT_DATA:
        out += draw_grid(redtiles)

    # Try drawing squares:
    largest_square_coords = None
    largest_square_size = 0

    for tile in redtiles:
        for other_tile in redtiles:
            #No elegant way to prevent tiles being compared to themself. But also it doesn't matter
            current_x_min = min(tile[0], other_tile[0])
            current_x_max = max(tile[0], other_tile[0])
            current_y_min = min(tile[1], other_tile[1])
            current_y_max = max(tile[1], other_tile[1])
            current_size = (current_x_max-current_x_min + 1) * (current_y_max-current_y_min + 1)

            if current_size > largest_square_size:
                #Found larger square
                largest_square_coords = (tile, other_tile)
                largest_square_size = current_size

            if DEBUG:
                out += draw_grid(redtiles, square_coords = (tile, other_tile))
                out += f"\nSquare of Size {current_size}\n"
    
    largest_square_corner_1, largest_square_corner_2 = largest_square_coords
    out += f"\n\n\nLargest Square using the tiles ({largest_square_corner_1[0]}|{largest_square_corner_1[1]}) and ({largest_square_corner_2[0]}|{largest_square_corner_2[1]})"
    if OUTPUT_DATA:
        out += draw_grid(red_tiles=redtiles, square_coords=largest_square_coords)
    out += f"The Largest Area is {largest_square_size}"
    return (out, largest_square_size)



with open(input_path, 'r') as file_in:
    input = file_in.read()
(out, result) = process_input(input)

print(result)

with open(output_path, 'w') as file_out:
    file_out.write(out)