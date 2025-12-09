import os
import re
import math
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
day = 9# Input day here

test = True # Change this to run program with the smaller testinput for debug
DEBUG = True # Change this to have debug outputs
OUTPUT_DATA = True

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
    
    out = "Grid:\n"

    if(square_coords != None):
        (corner_1, corner_2) = square_coords
        xmin = min(corner_1[0], corner_2[0])
        xmax = max(corner_1[0], corner_2[0])
        ymin = min(corner_1[1], corner_2[1])
        ymax = max(corner_1[1], corner_2[1])
        out += f"With Square ({corner_1[0]}|{corner_1[1]})-({corner_2[0]}|{corner_2[1]})\n"
        for x in range(xmin, xmax+1):
            for y in range(ymin, ymax+1):
                grid[x][y] = -1

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
    
    for y in range(grid_size):
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

def check_for_green(list_of_red_tiles, index_a, index_b):
    coords_a = list_of_red_tiles[index_a]
    coords_b = list_of_red_tiles[index_b]
    min_x = min(coords_a[0], coords_b[0])
    min_y = min(coords_a[1], coords_b[1])
    max_x = max(coords_a[0], coords_b[0])
    max_y = max(coords_a[1], coords_b[1])
    print(f"{coords_a}, {coords_b}")
    square = Polygon([
        Point(min_x, min_y),
        Point(max_x, min_y),
        Point(max_x, max_y),
        Point(min_x, max_y)      
    ])

    if(DEBUG):
        print(square)

    polygon = Polygon(list_of_red_tiles)

    valid_square = False

    if polygon.contains(square):
        valid_square == True
    

    return valid_square


# def check_for_green(list_of_red_tiles, index_a, index_b):
#     # iterate through list from index_a to index_b to see if we leave a hole in the rectangle
#     valid_square = True
#     corner_correct_1 = False
#     corner_correct_2 = False
#     corner_correct_3 = False
#     corner_correct_4 = False
#     done_checking = False

#     start_index = index_a
#     current_index = start_index
#     coords_a = list_of_red_tiles[index_a]
#     coords_b = list_of_red_tiles[index_b]
#     corner_1 = [min(coords_a[0], coords_b[0]),min(coords_a[1], coords_b[1])]
#     corner_2 = [max(coords_a[0], coords_b[0]),max(coords_a[1], coords_b[1])]
#     # Attempt 3:
#     while not done_checking:
        
#         current_index += 1
#         current_coords = list_of_red_tiles[current_index%len(list_of_red_tiles)]

#         #check if new coords are within the square (aka):
#         if(current_coords[0] > corner_1[0] and current_coords[0] < corner_2[0]):
#             if(current_coords[1] > corner_1[1] and current_coords[1] < corner_2[1]):
#                 valid_square = False
#                 done_checking = True
#                 if(DEBUG):
#                     print(f"\t{current_coords[0]}|{current_coords[1]} is within the square")

#         #Check if we found a point left/down from xmin/ymax:
#         if(not corner_correct_1):
#             if(current_coords[0]<=corner_1[0] and current_coords[1] >= corner_2[1]):
#                 corner_correct_1 = True
#         # up/right from xmax/ymin:
#         if(not corner_correct_2):
#             if(current_coords[0]>=corner_2[0] and current_coords[1] <= corner_1[1]):
#                 corner_correct_2 = True
#         # up/left from xmin/ymin:
#         if(not corner_correct_3):
#             if(current_coords[0]<=corner_1[0] and current_coords[1] <= corner_1[1]):
#                 corner_correct_3 = True
#         # up/right from xmax/ymax:
#         if(not corner_correct_4):
#             if(current_coords[0]>=corner_2[0] and current_coords[1] >= corner_2[1]):
#                 corner_correct_4 = True


#         if(current_index%len(list_of_red_tiles) == start_index):
#             done_checking = True
#             if(DEBUG):
#                 print(f"We are done checking Square ({coords_a[0]}|{coords_a[1]})-({coords_b[0]}|{coords_b[1]}). it is valid\n")

    
#     # Attempt 2:
#     # if(DEBUG):
#     #     print(f"Checking Square {coords_a[0]}|{coords_a[1]}-{coords_b[0]}|{coords_b[1]}")
#     # if coords_a[0] >= coords_b[0]:
#     #     #point a right of point b or in same column 
#     #     x_pos = 1
#     # else:
#     #     x_pos = -1

#     # if coords_a[1] >= coords_b[1]:
#     #     #point a above point b or in same row 
#     #     y_pos = 1
#     # else:
#     #     y_pos = -1

#     # while not done_checking:
#     #     last_coords = list_of_red_tiles[current_index%len(list_of_red_tiles)]
#     #     current_index += 1
#     #     current_coords = list_of_red_tiles[current_index%len(list_of_red_tiles)]
#     #     vector = [current_coords[0]-last_coords[0], current_coords[1]-last_coords[1]]
#     #     if(DEBUG):
#     #         print(f"Checking {last_coords[0]}|{last_coords[1]} to {current_coords[0]}|{current_coords[1]}")
#     #         print(vector)
#     #         print(f"xpos:{x_pos}, ypos:{y_pos}")
#     #     if (vector[0]*x_pos) < 0:
#     #         #We are moving towards the other corner on the x-axis
#     #         #Check if we move between them on the y-axis
#     #         if (last_coords[1] < max(coords_a[1], coords_b[1])) and (last_coords[1] > min(coords_a[1], coords_b[1])):
#     #             # We are between a and b on the y axis.
#     #             # Check if we end on the wrong side of point a
#     #             if(x_pos > 0):
#     #                 #Check if we moved through the right border:
#     #                 if current_coords[0] < coords_a[0] and last_coords[0] >= coords_a[0]:
#     #                     valid_square = False
#     #                     done_checking = True
#     #                     if(DEBUG):
#     #                         print(f"Square ({coords_a[0]}|{coords_a[1]})-({coords_b[0]}|{coords_b[1]}) is invalid because Tile ({current_coords[0]}|{current_coords[1]}) (crossed though the y axis border)")
#     #             elif(x_pos < 0):
#     #                 #Check if we moved through the left border:
#     #                 if current_coords[0] > coords_a[0] and last_coords[0] <= coords_a[0]:
#     #                     valid_square = False
#     #                     done_checking = True
#     #                     if(DEBUG):
#     #                         print(f"Square ({coords_a[0]}|{coords_a[1]})-({coords_b[0]}|{coords_b[1]}) is invalid because Tile ({current_coords[0]}|{current_coords[1]}) (crossed though the y axis border)")
#     #     if (vector[1]*y_pos) < 0:
#     #         #We are moving towards the other corner on the y-axis
#     #         #Check if we move between them on the x-axis
#     #         if (last_coords[0] < max(coords_a[0], coords_b[0])) and (last_coords[0] > min(coords_a[0], coords_b[0])):
#     #             # We are between a and b on the x axis.
#     #             # Check if we end on the wrong side of point a
#     #             if(y_pos > 0):
#     #                 #Check if we moved through the lower border:
#     #                 if current_coords[1] < coords_a[1] and last_coords[1] >= coords_a[1]:
#     #                     valid_square = False
#     #                     done_checking = True
#     #                     if(DEBUG):
#     #                         print(f"Square ({coords_a[0]}|{coords_a[1]})-({coords_b[0]}|{coords_b[1]}) is invalid because Tile ({current_coords[0]}|{current_coords[1]}) (crossed though the x axis border)")
#     #             elif(y_pos < 0):
#     #                 #Check if we moved through the lower border:
#     #                 if current_coords[1] > coords_a[1] and last_coords[1] <= coords_a[1]:
#     #                     valid_square = False
#     #                     done_checking = True
#     #                     if(DEBUG):
#     #                         print(f"Square ({coords_a[0]}|{coords_a[1]})-({coords_b[0]}|{coords_b[1]}) is invalid because Tile ({current_coords[0]}|{current_coords[1]}) (crossed though the x axis border)")

#     #     if(DEBUG):
#     #         print(f"No Issue with vektor ({last_coords[0]}|{last_coords[1]})-({current_coords[0]}|{current_coords[1]}) in Square ({coords_a[0]}|{coords_a[1]}|{coords_b[0]}|{coords_b[1]})")

#     #     if(current_index%len(list_of_red_tiles) == index_b):
#     #         #switch a and b for the return
#     #         if(DEBUG):
#     #             print(f"Switching the points")
#     #         coords_a = list_of_red_tiles[index_b]
#     #         coords_b = list_of_red_tiles[index_a]

#     #         if coords_a[0] >= coords_b[0]:
#     #             #point a right of point b or in same column 
#     #             x_pos = 1
#     #         else:
#     #             x_pos = -1

#     #         if coords_a[1] >= coords_b[1]:
#     #             #point a above point b or in same row 
#     #             y_pos = 1
#     #         else:
#     #             y_pos = -1

        

#         #elegant check that fails if we cross trough the entire square at once and don't stop at an invalid point
#         # if(((current_coords[0] - coords_a[0]) * x_pos < 0) and ((current_coords[0] - coords_b[0]) * x_pos > 0)):
#         #     #x betwrrent_coords[1] - coords_a[1]) * y_pos < 0) and ((current_coords[1] - coords_b[1]) * y_pos > 0)):
#         #         #y between coords a and b
#         #         valid_square = False
#         #         done_checking = True
#         #         if(DEBUG):
#         #             print(f"Square ({coords_a[0]}|{coords_a[1]})-({coords_b[0]}|{coords_b[1]}) is invalid because Tile ({current_coords[0]}|{current_coords[1]}) is between them on the x and y axis\n")
#         #             print(f"x-check 1: {current_coords[1]}-{coords_a[1]} * position {y_pos} = {(current_coords[1] - coords_a[1]) * y_pos}")
#         #             print(f"x-check 2: {current_coords[1]}-{coords_b[1]} * position {y_pos} = {(current_coords[1] - coords_b[1]) * y_pos}")
#         #             print(f"y-check 1: {current_coords[0]}-{coords_a[0]} * position {x_pos} = {(current_coords[0] - coords_a[0]) * x_pos}")
#         #             print(f"y-check 2: {current_coords[0]}-{coords_b[0]} * position {x_pos} = {(current_coords[0] - coords_b[0]) * x_pos}")
#         # else:
#         #     if(DEBUG):
#         #             print(f"Square ({coords_a[0]}|{coords_a[1]})-({coords_b[0]}|{coords_b[1]}) is valid with Tile ({current_coords[0]}|{current_coords[1]})\n")
#         #             print(f"x-check 1: {current_coords[1]}-{coords_a[1]} * position {y_pos} = {(current_coords[1] - coords_a[1]) * y_pos}")
#         #             print(f"x-check 2: {current_coords[1]}-{coords_b[1]} * position {y_pos} = {(current_coords[1] - coords_b[1]) * y_pos}")
#         #             print(f"y-check 1: {current_coords[0]}-{coords_a[0]} * position {x_pos} = {(current_coords[0] - coords_a[0]) * x_pos}")
#         #             print(f"y-check 2: {current_coords[0]}-{coords_b[0]} * position {x_pos} = {(current_coords[0] - coords_b[0]) * x_pos}")
        
#     if(DEBUG):
#         print(f"Done with check of Square {coords_a[0]}|{coords_a[1]}-{coords_b[0]}|{coords_b[1]}")
#     if((not corner_correct_1) or (not corner_correct_2) or (not corner_correct_3) or (not corner_correct_4)):
#         if(DEBUG):
#             print(f"Square is outside the area")
#         valid_square = False
#     return valid_square
        
        

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

    for i in range(len(redtiles)):
        for j in range(len(redtiles)):
            if i != j:
                tile = redtiles[i]
                other_tile = redtiles[j]
                current_x_min = min(tile[0], other_tile[0])
                current_x_max = max(tile[0], other_tile[0])
                current_y_min = min(tile[1], other_tile[1])
                current_y_max = max(tile[1], other_tile[1])
                current_size = (current_x_max-current_x_min + 1) * (current_y_max-current_y_min + 1)
                
                if current_size > largest_square_size:
                    #Found larger square
                    #check if valid:
                    if(check_for_green(redtiles, i, j)):  
                        largest_square_coords = (tile, other_tile)
                        largest_square_size = current_size

                        if DEBUG:
                            out += draw_grid(redtiles, square_coords = (tile, other_tile))
                            out += f"\nSquare of Size {current_size}\n"
                    else:
                        if(DEBUG):
                            out += draw_grid(redtiles, square_coords = (tile, other_tile))
                            out += f"\nSquare Invalid\n"
                else:
                    if(DEBUG):
                        out += draw_grid(redtiles, square_coords = (tile, other_tile))
                        out += f"\nSquare smaller than what we already have\n"
    
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