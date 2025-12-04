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
        if DEBUG:
            out += f"Grid x:{x}|y:{y} has {surrounding} adjacent rolls.\n"
    if surrounding < 4:
        return True
    else:
        return False
    
def draw_grid(grid, *args):
    drawn = ''
    global x_max
    global y_max
    to_be_removed  = [[False for y in range(y_max)] for x in range(x_max)]
    for arg in args:
        to_be_removed = arg
    drawn += "\nCurrent Grid:\n"
    if(to_be_removed != None):
        for x in range(0, x_max):
            for y in range(0, y_max):
                if(to_be_removed[x][y] == True):
                    drawn += 'x'
                elif(grid[x][y] == True):
                    drawn += '@'
                else:
                    drawn += '.'
            drawn += '\n'
    return drawn

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

done = False
removed_rolls = 0

availeable = [[None for y in range(y_max)] for x in range(x_max)]
out += f"Starting to analyse grid of size x = {x_max} and y = {y_max}\n"
out += draw_grid(grid, availeable)
while not done:
    done = True #if not changed to false, we are done.
    for x in range(0, x_max):
        for y in range(0, y_max):
            if DEBUG:
                out += f"Checking grid {x}, {y}."
                if(grid[x][y]):
                    out += " \'@\'\n"
                else:
                    out += " \'.\'\n"
            if(check_roll(grid, x, y)):
                if DEBUG:
                    out += f"Marking {x}|{y} as availeable.\n"
                availeable[x][y] = True
                done = False
            else:
                if DEBUG:
                    out += f"Not marking {x}|{y}"
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
    current_round_removed = sum(row.count(True) for row in availeable)
    removed_rolls += current_round_removed
    if current_round_removed > 0:
        out += f"We could remove the following {current_round_removed} rolls from the grid: \n"
        out += draw_grid(grid, availeable)
    
    #update_grid
    for x in range(0, x_max):
        for y in range(0, y_max):
            if(availeable[x][y] == True):
                grid[x][y] = False
    
out += f"We were able to remove a total of {removed_rolls} rolls"

with open(output_path, 'w') as file_out:
    file_out.write(out)
    