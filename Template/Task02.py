import os
import re
import math

day = # Input day here

test = False # Change this to run program with the smaller testinput for debug
DEBUG = False # Change this to have debug outputs

root = os.getcwd()
current_day = os.path.join(root, f"Day{day:2d}")
if test:
    input_path = os.path.join(current_day, 'test.txt')
else:
    input_path = os.path.join(current_day, 'Input.txt')
output_path = os.path.join(current_day, 'Output.txt')

out = ''

with open(input_path, 'r') as file_in:
    input = file_in.read()


with open(output_path, 'w') as file_out:
    file_out.write(output_path)