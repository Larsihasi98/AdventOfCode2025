import os
import re
import math

day = 3 # Input day here

test = False # Change this to run program with the smaller testinput for debug
DEBUG = False # Change this to have debug outputs

root = os.getcwd()
current_day = os.path.join(root, f"Day{day:02d}")
print(f"Setting up directories at {current_day}")
if test:
    input_path = os.path.join(current_day, 'test.txt')
else:
    input_path = os.path.join(current_day, 'Input.txt')
output_path = os.path.join(current_day, 'Output.txt')

out = ''

def get_highest_joltage(bank_in):
    global out
    digit_1 = 0
    digit_2 = 0
    battery_1_pos = -1
    battery_2_pos = -1

    if(len(bank_in) > 1): #idk if this is neccessary
    #Get first battery
        for index in range(0, len(bank_in) - 1):
            current_battery = int(bank_in[index])
            if digit_1 < current_battery:
                digit_1 = current_battery
                battery_1_pos = index
        
        #Get second battery
        for index in range(0, len(bank_in)):
            current_battery = int(bank_in[index])
            if digit_2 < current_battery and index > battery_1_pos:
                digit_2 = current_battery
                battery_2_pos = index

        joltage = int(f"{digit_1}{digit_2}")

        out += f"looking at the bank {bank_in}, we turn on the batteries in position {battery_1_pos} and {battery_2_pos} for a joltage of {joltage}\n"
        if DEBUG:
            print(f"looking at the bank {bank_in}, we turn on the batteries in position {battery_1_pos} and {battery_2_pos} for a joltage of {joltage}")

    else:
        out += f"The bank {bank_in} only contains a single battery with joltage {int(bank_in)}"
        joltage = int(bank_in)
    return joltage        


with open(input_path, 'r') as file_in:
    input = file_in.read()

banks = []

for bank in input.split('\n'):
    out += f"Read Bank {bank}\n"
    banks.append(bank)

joltage_per_bank = []

for bank in banks:
    out += f"..getting Joltage for {bank}\n"
    joltage_per_bank.append(get_highest_joltage(bank))

out += "Got these amounts of joltage:\n"
for joltage in joltage_per_bank:
    out += f"\t-{joltage}\n"

total = sum(joltage_per_bank)

out += f"Total Joltage is {total}"

print(f"The total amount of Joltage is {total}")

with open(output_path, 'w') as file_out:
    file_out.write(out)