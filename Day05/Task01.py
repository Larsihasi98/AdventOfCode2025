import os
import re
import math

day = 5# Input day here

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

out = ''

with open(input_path, 'r') as file_in:
    input = file_in.read()
    if(DEBUG):
        out += f"Input:\n{input}\n"
    
    fresh_ranges = input.split('\n\n')[0]
    IDs = input.split('\n\n')[1]

if(DEBUG):
    out += f"\nThe Ranges are:\n{fresh_ranges}\n"
    out += f"\nAnd the IDs are:\n{IDs}\n"

# Setup save ranges:
save_ranges = []
min = -1
max = 0
for fresh_range in fresh_ranges.split('\n'):
    range_min = int(fresh_range.split('-')[0])
    range_max = int(fresh_range.split('-')[1])
    if(min < 0 or range_min < min):
        min = range_min
    if(range_max > max):
        max = range_max
    save_ranges.append({"min": range_min, "max": range_max})

# fresh_check = [False] * (max-min)

# for save_range in save_ranges:
#     if(DEBUG):
#         out += f"Marking IDs {save_range["min"]} to {save_range["max"]} as fresh\n"
#     for ID in range(save_range["min"]-min, save_range['max']-min):
#         fresh_check[ID] = True

# if(DEBUG):
#     out += "The following IDs are fresh:\n"
#     for index in range(0,len(fresh_check)):
#         if(fresh_check[index]):
#             out += f"{index+min},"
#     out += "\n"

def check_id(ID):
    global save_ranges
    applicable_ranges = []
    for range in save_ranges:
        if(ID >= range["min"] and ID <= range["max"]):
            applicable_ranges.append(range)
    if(len(applicable_ranges) <=0):
        return False
    else:
        return True

fresh_count = 0
for ID in IDs.split('\n'):
    ID = int(ID)
    out += f"checking ID {ID}...\n"
    if(check_id(ID)):
        out += "\tIt is fresh\n"
        fresh_count += 1
    else:
        out += "\tIt is spoiled\n"
    
out += f"A total of {fresh_count} IDs are fresh"

with open(output_path, 'w') as file_out:
    file_out.write(out)