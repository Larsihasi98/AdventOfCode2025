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
    input_length = len(ID_in)
    if input_length%2 == 0:
        half1 = ID_in[0:input_length//2]
        half2 = ID_in[input_length//2:]

        if half1 == half2:
            invalid_IDs.append(int(ID_in))

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
        check_id(str(i))

if(DEBUG):
    for invalid_ID in invalid_IDs:
        print(f"ID {invalid_ID} is invalid")

print(f"Adding all invalid IDs together results in:\n{sum(invalid_IDs)}")