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
digits = 12
def get_highest_joltage(bank_in):
    global out
    global digits

    digit_value = [-1]*12
    digit_position = [-1]*12

    for digit in range(0, digits):
        if digit == 0:
            #first digit, can start at beginning
            if(DEBUG):
                out+=f"Getting digit {digit}...\n"
            for index in range(0, len(bank_in) - (digits-digit)):
                current_battery = int(bank_in[index])
                if digit_value[digit] < current_battery:
                    digit_value[digit] = current_battery
                    digit_position[digit] = index
            if(DEBUG):
                out += f"\tSettled on value {digit_value[digit]} in position {digit_position[digit]}\n"
        else:
            if(DEBUG):
                out += f"Starting at position {digit_position[digit-1]+1} for digit {digit}\n"
            for index in range(digit_position[digit-1]+1, len(bank_in) - (digits-(digit+1))):
                current_battery = int(bank_in[index])
                if digit_value[digit] < current_battery:
                    digit_value[digit] = current_battery
                    digit_position[digit] = index
            if(DEBUG):
                out += f"\tSettled on value {digit_value[digit]} in position {digit_position[digit]}\n"

    joltage_string = ''
    out += f"For the Bank {bank_in} we found the batteries in position\n\t-"
    for digit in range(0, digits):
        joltage_string = f"{joltage_string}{digit_value[digit]}"
        out += f"{digit_position[digit]}-"

    joltage = int(joltage_string)
    out += f"\nfor a total joltage of {joltage}"

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