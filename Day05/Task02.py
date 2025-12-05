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
total_min = -1
total_max = 0
for fresh_range in fresh_ranges.split('\n'):
    range_min = int(fresh_range.split('-')[0])
    range_max = int(fresh_range.split('-')[1])
    if(total_min < 0 or range_min < total_min):
        total_min = range_min
    if(range_max > total_max):
        total_max = range_max
    save_ranges.append({"min": range_min, "max": range_max})

#Combine ranges that are part of each other:
adjusted_ranges = []
while len(save_ranges) > 0:
    current_range = save_ranges.pop(0)
    done_with_current = False
    while done_with_current == False:
        out += f"\nlooking at range {current_range['min']} to {current_range['max']}..."
        done_with_current = True
        to_combine = []
        for i in range(0, len(save_ranges)):
            compare_range = save_ranges[i]
            if(DEBUG):
                out += f"\n\tcomparing to range {compare_range['min']} to {compare_range['max']}..."
            if(current_range['min'] >= compare_range['min'] and current_range['max'] <= compare_range['max']):
                #current range is entirely within compare range
                to_combine.append(i)
                if(DEBUG):
                    out += f"\tCurrent range is entirely within range {i}"
                done_with_current = False
            elif(current_range["min"] <= compare_range['max'] and current_range['max'] >= compare_range['min']):
                #current range ends where compare range starts
                to_combine.append(i)
                if(DEBUG):
                    out += f"\tCurrent range starts within range {i}"
                done_with_current = False
            elif(current_range["min"] <= compare_range['min'] and current_range['max'] >= compare_range['min']):
                #current range starts where compare range ends
                to_combine.append(i)
                if(DEBUG):
                    out += f"\tCurrent range ends  within range {i}"
                done_with_current = False
            else:
                if(DEBUG):
                    out += f"\tCurrent range does not cross range{i}"
        current_min = current_range['min']
        current_max = current_range['max']
        for j in range(len(to_combine), 0, -1):#count backwards so we start with the higher indexes
            #Check if any of the ranges we combine with have a lower min or higher max and adjust accordingly
            if(DEBUG):
                out += f"\nGetting range no. {to_combine[j-1]}"
            current_compare = save_ranges.pop(to_combine[j-1])
            out += f"\nCombining {current_min}-{current_max} and {current_compare['min']}-{current_compare['max']}"
            current_min = min(current_min, current_compare['min'])
            current_max = max(current_max, current_compare['max'])
            out += f"\tresult: {current_min}-{current_max}"
        current_range = {"min": current_min, "max": current_max}
    out += f"\nCan't further combine range {current_range['min']} to {current_range['max']} with other ranges"
    adjusted_ranges.append(current_range)

count = 0
out += f"\nThe combined ranges are:"
for adjusted_range in adjusted_ranges:
    count += adjusted_range['max']-adjusted_range['min']+1
    out +=f"\n\t{adjusted_range['min']} to {adjusted_range['max']}"

out += f"\nleading to a total of {count} fresh IDs"

with open(output_path, 'w') as file_out:
    file_out.write(out)