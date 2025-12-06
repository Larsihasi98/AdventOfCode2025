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
def process_input(input):
    global out
    calculation_df = pd.read_csv(StringIO(input), sep=r'\s+', header=None).transpose()
    calculation_df.columns = [*calculation_df.columns[:-1], 'operator']
    out += 'The Calculations are:\n'
    out += calculation_df.to_string()
    out += '\n'
    total_result = 0
    for index, row in calculation_df.iterrows():
        if(DEBUG):
            out+= f"Looking at row {index}\n"
        result = 0
        operator = row['operator']
        if(operator == '+'):
            if(DEBUG):
                out+= f"Row needs to be added up {index}\n"
            #Add elements
            for j in range(0, row.shape[0]-1):
                if(DEBUG):
                    out += f"\tadding element{j}\n"
                result +=  int(row[j])
        if(operator == '*'):
            if(DEBUG):
                out+= f"Row needs to be multiplied {index}\n"
            #Multiply elements
            for j in range(0, row.shape[0]-1):
                if(DEBUG):
                    out += f"\tmultiplying with element{j}\n"
                if(result > 0):
                    result *=  int(row[j])
                else:
                    result = int(row[j])
        else:
            out += f"Unknown operator in row {index}: {operator}\n"
        out += f"Result of row  {index} is {result}\n"
        total_result  += result
    out += f"\nAdding all results up leads us to {total_result}"
    return(out, total_result)



with open(input_path, 'r') as file_in:
    input = file_in.read()

(out, result) = process_input(input)
print(result)
with open(output_path, 'w') as file_out:
    file_out.write(out)