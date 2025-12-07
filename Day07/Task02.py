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
                if(Beam_Travel[i][j] > 0):
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
    out += "Timelines:\n"
    for i in range(0, len(Beam_Travel[0])):
        timelines = Beam_Travel[len(Beam_Travel)-1][i]
        out += f"\t-Column {i} has {timelines} timelines\n"
    
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
            Beam_timelines = [0] * len(Field[0])
            #Set Beam Startpoint:
            Beam_timelines[Beam_start] = 1
        
        elif(index > 0):
            #Row 1 and onwards, past the start
            Last_row = Beam_Travel[index-1]
            Beam_timelines = [0] * len(Field[0])
            if(DEBUG):
                out += f"\nProcessing line {index}"

            for i in range(0, len(Last_row)):
                if(DEBUG):
                    out += f"\n\tlooking at element {i}"
                if Last_row[i] > 0:
                    # Beam arrives from above
                    if(DEBUG):
                        out += f"There is a Beam above on {Last_row[i]} timelines"
                    if Field[index][i]:
                        #Check if we need to split:
                        if(DEBUG):
                            out += f"- It needs to be split"
                        no_split += 1
                        if i > 0:
                            Beam_timelines[i-1] += Last_row[i] # If we are not at the left edge, add all possible timelines to left
                        if i < len(Beam_timelines)-1:
                            Beam_timelines[i+1] += Last_row[i] # If we are not at the right edge, add all possible timelines to right
                    else:
                        #No need to split:
                        if(DEBUG):
                            out += f"- It didn't need to split"
                        Beam_timelines[i] += Last_row[i]
        Beam_Travel.append(Beam_timelines)
        out += f"\nBeam after {index} steps:\n{print_field(Field, Beam_Travel)}"
    no_of_timelines = sum(Beam_Travel[len(Beam_Travel)-1])
    return (out, no_split, no_of_timelines)


    




with open(input_path, 'r') as file_in:
    input = file_in.read()

(out, splits, timelines) = process_input(input)
print(f"The Beam split a total of {splits} times into {timelines} different timelines")
with open(output_path, 'w') as file_out:
    file_out.write(out)