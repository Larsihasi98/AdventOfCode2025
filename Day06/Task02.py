import os
import re
import pandas as pd
from io import StringIO
import math

day = 6# Input day here

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

def convert_numbers(numbers_in):
    done = False
    numbers_out = []
    if(DEBUG):
        print(numbers_in)
    index = 0
    while not done:
        done = True #if we don't have any numbers left that are large enough we can stop
        new_number = ''
        for number in numbers_in:
            if(len(number) > index):
                #skip numbers that don't have enough digits
                new_number += number[index]
                done = False
        if(DEBUG):
            print(new_number)
        if(len(new_number) > 0):
            numbers_out.append(int(new_number))
        index += 1
    
    return numbers_out.reverse()

def process_input(input):
    out = ''
    input_array = []
    for line in input.split('\n'):
        input_array.append(list(line))

    calculations = []
    current_opperand = ''
    current_numbers = []
    for y in reversed(range(0, len(input_array[0]))):
        #iterate through rows right to left
        current_number = ''
        for x in range(0, len(input_array)):
            #iterate through column top to bottom
            current_item = input_array[x][y]
            if current_item.isdigit():
                current_number += f"{current_item}"
            if (current_item == '+' or current_item == '*'):
                current_opperand = current_item
        if(len(current_number) > 0):
            current_numbers.append(int(current_number)) #Change the string of this column to an int and append
        if(current_opperand != ''):
            # We have arrived at the end of the current calculation. Add it to our list of calculations and reset variables
            calculations.append({'Opperand': current_opperand, 'Numbers': current_numbers})
            current_opperand = ''
            current_numbers = []
    
    total_result = 0
    for calculation in calculations:
        if(calculation['Opperand'] == '+'):
            result = 0
            out += 'Adding up the numbers... '
            for number in calculation['Numbers']:
                out += f"{number} "
                result += number
            out += f'= {result}\n'
        if(calculation['Opperand'] == '*'):
            result = 1
            out += 'Multiplying the numbers... '
            for number in calculation['Numbers']:
                out += f"{number} "
                result *= number
            out += f"={result}"
        total_result += result
        

    out += f"\nAdding all results up leads us to {total_result}"
    return(out, total_result)



with open(input_path, 'r') as file_in:
    input = file_in.read()

(out, result) = process_input(input)
print(result)
with open(output_path, 'w') as file_out:
    file_out.write(out)