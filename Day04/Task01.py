import os
import re
import math

day = 4# Input day here

test = False # Change this to run program with the smaller testinput for debug
DEBUG = False # Change this to have debug outputs

root = os.getcwd()
current_day = os.path.join(root, f"Day{day:02d}")
if test:
    input_path = os.path.join(current_day, 'test.txt')
else:
    input_path = os.path.join(current_day, 'Input.txt')
output_path = os.path.join(current_day, 'Output.txt')

out = ''

def check_roll(grid, x, y):
    global x_max
    global y_max
    global out

    if(grid[x][y] != True):
        #spot isn't a roll
        if DEBUG:
            out += f"Grid x:{x}|y:{y} is not a roll\n"
        return False
    else:
        surrounding = 0
        if(y > 0):
            #check left side
            if(grid[x][y-1] == True):
                if(DEBUG):
                    out += f"Left side is occupied\n"
                surrounding += 1
            if(x > 0):
                #check top left corner
                if(grid[x-1][y-1] == True):
                    if(DEBUG):
                        out += f"Top Left side is occupied\n"
                    surrounding += 1
            if(x < x_max - 1):
                #check bottom left corner
                if(grid[x+1][y-1] == True):
                    if(DEBUG):
                        out += f"Bottom left side is occupied\n"
                    surrounding += 1
        if(y < y_max - 1):
            #checl right side
            if(grid[x][y+1] == True):
                if(DEBUG):
                    out += f"Right side is occupied\n"
                surrounding += 1
            if(x > 0):
                #check top right cornerif(DEBUG):
                if(grid[x-1][y+1] == True):
                    if(DEBUG):
                        out += f"Top right side is occupied\n"
                    surrounding += 1
            if(x < x_max - 1):
                #check bottom right cornerif(DEBUG):
                if(grid[x+1][y+1] == True):
                    if(DEBUG):
                        out += f"Bottom right side is occupied\n"
                    surrounding += 1
        if(x > 0):
            #check top
            if(grid[x-1][y] == True):
                if(DEBUG):
                    out += f"top side is occupied\n"
                surrounding += 1
        if(x < x_max - 1):
            #check top
            if(grid[x+1][y] == True):
                if(DEBUG):
                    out += f"bottom side is occupied\n"
                surrounding += 1

        out += f"Grid x:{x}|y:{y} has {surrounding} adjacent rolls.\n"
    if surrounding < 4:
        return True
    else:
        return False
    


with open(input_path, 'r') as file_in:
    input = file_in.read()

grid = []

for line in input.split('\n'):
    row = []
    for spot in line:
        if spot == '@':
            row.append(True) #Roll
        else:
            row.append(False)
    grid.append(row)
x_max = len(grid[0])
y_max = len(grid)
availeable = [[None for y in range(y_max)] for x in range(x_max)]
out += f"Starting to analyse grid of size x = {x_max} and y = {y_max}\n"
for x in range(0, x_max):
    for y in range(0, y_max):
        if DEBUG:
            out += f"Checking grid {x}, {y}."
            if(grid[x][y]):
                out += " \'@\'\n"
            else:
                out += " \'.\'\n"
        if(check_roll(grid, x, y)):
            out += f"Marking {x}|{y} as availeable.\n"
            availeable[x][y] = True
        else:
            out += f"Not marking {x}|{y}\n"
            availeable[x][y] = False
        
        if DEBUG:
            out += "\nAvaileability grid...\n"
            for x_list in range(0, x_max):
                for y_list in range(0, y_max):
                    if(availeable[x_list][y_list] == False):
                        out += 'O'
                    else:
                        out += 'X'
                out += '\n'

if DEBUG:
    out += "\nAvaileability grid...\n"
    for x in range(0, x_max):
        for y in range(0, y_max):
            if(availeable[x][y] == False):
                out += 'O'
            else:
                out += 'X'
        out += '\n'

out += "\nOutput grid:\n"
for x in range(0, x_max):
    for y in range(0, y_max):
        if(availeable[x][y] == True):
            out += 'x'
        elif(grid[x][y] == True):
            out += '@'
        else:
            out += '.'
    out += '\n'

out += f"\n\t- A total of {sum(row.count(True) for row in availeable)} can be moved.\n"

with open(output_path, 'w') as file_out:
    file_out.write(out)