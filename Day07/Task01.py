import os
import re
import math

day = 7# Input day here

test = False # Change this to run program with the smaller testinput for debug
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

def print_field(Field, Beam_Travel):
    out = "Current Field:\n"
    for i in range(0, len(Field)):
        for j in range(0, len(Field[i])):
            if(i < len(Beam_Travel)):
                if(Beam_Travel[i][j]):
                    out += '|'
                elif(Field[i][j]):
                    out += '^'
                else:
                    out += '.'
            else:
                if(Field[i][j]):
                    out += '^'
                else:
                    out += '.'
        out += '\n'
    
    return out

def process_input(input):
    out = ''
    no_split = 0
    Beam_start = 0
    Field = []
    Beam_Travel = []
    out += f"Input:\n{input}\n"
    for row in input.split('\n'):
        Field_Row = []
        for i in range(0, len(row)):
            current_char = row[i]
            if current_char == 'S':
                out += f"Beam Starts at index {i}"
                Beam_start = i
                Field_Row.append(False)
            if current_char == '^':
                Field_Row.append(True)
            elif current_char == '.':
                Field_Row.append(False)
        Field.append(Field_Row)
    
    #Go line by line.
    for index in range(0, len(Field)):
        if(index == 0):
            Beam_row = [False] * len(Field[0])
            #Set Beam Startpoint:
            Beam_row[Beam_start] = True
        
        elif(index > 0):
            #Row 1 and onwards, past the start
            Last_row = Beam_Travel[index-1]
            Beam_row = [False] * len(Field[0])
            if(DEBUG):
                out += f"\nProcessing line {index}"

            for i in range(0, len(Last_row)):
                if(DEBUG):
                    out += f"\n\tlooking at element {i}"
                if Last_row[i]:
                    # Beam arrives from above
                    if(DEBUG):
                        out += f"There is a Beam above."
                    if Field[index][i]:
                        #Check if we need to split:
                        if(DEBUG):
                            out += f"- It needs to be split"
                        no_split += 1
                        if i > 0:
                            Beam_row[i-1] = True # If we are not at the left edge, make beam split to left
                        if i < len(Beam_row)-1:
                            Beam_row[i+1] = True # If we are not at the right edge, make beam split to right
                    else:
                        #No need to split:
                        if(DEBUG):
                            out += f"- It didn't need to split"
                        Beam_row[i] = True
        Beam_Travel.append(Beam_row)
        out += f"\nBeam after {index} steps:\n{print_field(Field, Beam_Travel)}"

    return (out, no_split)


    




with open(input_path, 'r') as file_in:
    input = file_in.read()

(out, result) = process_input(input)
print(f"The Beam split a total of {result} times")
with open(output_path, 'w') as file_out:
    file_out.write(out)