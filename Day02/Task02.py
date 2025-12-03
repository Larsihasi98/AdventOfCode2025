import os
import re
import math


test = False # Change this to run program with the smaller testinput for debug
DEBUG = False

root = os.getcwd()
current_day = os.path.join(root, "Day02")
if test:
    input_path = os.path.join(current_day, 'test.txt')
else:
    input_path = os.path.join(current_day, 'Input.txt')
output_path = os.path.join(current_day, 'Output.txt')

def check_id(ID_in):
    invalid = False #Assume ID is valid for now.
    for i in range(1, math.floor(len(ID_in)/2) + 1):
        # Decide to check increasing pattern sizes
        parts = []
        for j in range(0, len(ID_in), i):
            parts.append(ID_in[j:(j+i)])
        
        if(len(set(parts)) == 1):
            if(DEBUG):
                print(f"Invalid ID found in {ID_in}")
            invalid = True

    return invalid


with open(input_path) as file_in:
    input = file_in.read()

IDs = []
invalid_IDs = []
id_ranges = input.split(',')
for id_range in id_ranges:
    IDs.append(id_range.split('-'))

for ID in IDs:
    print(f"Got an ID from {ID[0]} to {ID[1]}")
    for i in range(int(ID[0]), int(ID[1])+1):
        if(check_id(str(i))):
            invalid_IDs.append(i)

if(DEBUG):
    for invalid_ID in invalid_IDs:
        print(f"ID {invalid_ID} is invalid")

print(f"Adding all invalid IDs together results in:\n{sum(invalid_IDs)}")