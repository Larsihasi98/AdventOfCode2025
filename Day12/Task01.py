import os
import re
import math
import numpy as np

day = 12# Input day here

test = True # Change this to run program with the smaller testinput for debug
DEBUG = False # Change this to have debug outputs

root = os.getcwd()
if(os.path.basename(root) != 'AdventOfCode2025'):
    root = os.path.normpath(os.path.join(root, '..'))
current_day = os.path.join(root, f"Day{day:02d}")
if test:
    input_path = os.path.join(current_day, 'test.txt')
else:
    input_path = os.path.join(current_day, 'Input.txt')
output_path = os.path.join(current_day, 'Output.txt')

regex_pattern = r"(?P<present_shapes>(^\d:\n.*\n.*\n.*\n*)+)\n*(?P<Grids>(\d+x\d+:\s(\d+\s*)*$\n*)*)"
shape_pattern = r"(?P<Index>\d):\n(?P<Shape>.*\n.*\n.*)"
grid_pattern = r"(?P<Shape>\d+x\d+): (?P<content>(?:\d+ *)+)"
def process_input(input):
    match = re.search(regex_pattern, input)
    shapes_input = re.findall(shape_pattern, input)
    grids_input = re.findall(grid_pattern, input)
    shapes = []
    for shape in shapes_input:
        index = shape[0]
        pattern = shape[1].split('\n')
        shape_np = np.empty((len(pattern), len(pattern[0])), dtype=bool)
        for i in range(len(pattern)):
            for j in range(len(pattern[i])):
                if pattern[i][j] == '#':
                    shape_np[i][j] = True
                else:
                    shape_np[i][j] = False
        
        shapes.append({
            'index': index,
            'pattern': shape_np
        })

    grids = []
    for grid in grids_input:
        dimensions = grid[0].split('x')
        content = np.array(grid[1].split(' '), dtype=int)

        grids.append({
            'x_max' : int(dimensions[0]) - 1, #As we will be starting at 0
            'y_max' : int(dimensions[1]) - 1,
            'content' : content
        })

    return (shapes, grids)

def check_shape_fill(grid, shape, thread_ID = -1):
    if(thread_ID >= 0):
        print(f"Starting thread {thread_ID}")

    current_grid = np.full((grid['x'], grid['y']), False, dtype = bool)
    

with open(input_path, 'r') as file_in:
    input = file_in.read()
shapes, grids = process_input(input)

with open(output_path, 'w') as file_out:
    file_out.write(out)