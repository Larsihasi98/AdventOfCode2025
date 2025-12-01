import os
import re
import math


test = False # Change this to run program with the smaller testinput for debug

root = os.getcwd()
current_day = os.path.join(root, "Day01")
if test:
    input_path = os.path.join(current_day, 'test.txt')
else:
    input_path = os.path.join(current_day, 'Input.txt')
output_path = os.path.join(current_day, 'Output.txt')
print(f"root dir = {root}")

instructions = []
with open(input_path, 'r') as file:
    for line in file:
        instructions.append(line)


dial_size = 100 # Including 0
dial_pos = 50
old_pos = dial_pos
count_zero = 0
#setup regex:
p = re.compile(r'^(?P<direction>L|R)(?P<amount>\d+$)')

out = ""

for instruction in instructions:
    old_pos = dial_pos
    left = True
    m = p.match(instruction)
    direction = m.group('direction')
    if direction == 'R':
        left = False
    amount = int(m.group('amount'))
    out += f"Next instruction: {instruction}Passed as {amount} towards {direction}\n"
    
    multiple = math.floor(amount / dial_size) # Subtract any full rotation
    count_zero += multiple
    out += f"Did {multiple} full rotations. Count currently {count_zero}\n"

    amount -= multiple * dial_size

    if amount > 0: # Need to also include an incomplete rotation:
        if left: # left rotations make numbers smaller
            amount *= -1
        
        dial_pos += amount
        dial_pos %= dial_size

        if(old_pos + amount <= 0): # passed 0 while going left
            if(old_pos > 0): # to prevent starting at 0 from triggering again
                count_zero += 1
                out += f"Passed 0 while going {amount * -1} left from {old_pos}, arriving at {dial_pos}. Count Currently {count_zero}\n"
        if(old_pos + amount >= 100):
            count_zero += 1
            out += f"Passed 99/0 while going {amount} right from {old_pos}, arriving at {dial_pos}. Count Currently {count_zero}\n"
    



    #Old
#     if left:
#         dial_pos -= amount
#         dial_pos%=  dial_size
#         out += f"Turning dial {amount} towards left.\n"
#         out += f"Now at Position {dial_pos}. Previously {old_pos}\n"
#         if amount >= dial_size: # We did a full rotation or more.
#             multiple = math.floor(amount / dial_size)
#             count_zero += multiple
#             out += f"Dial passed 0 a total of {multiple} times. Current count: {count_zero}\n"
#             if((dial_pos == 0) and (old_pos >= 0)): # if multiple turns also land on zero we need to count that aswell
#                 count_zero += 1
#                 out += f"Dial also landed on zero after an additional partial turn. Current count: {count_zero}\n"
#         elif((old_pos - amount <= 0) and (old_pos > 0)): # Checking if we went left through 0. Exception for starting on zero to not count it double
#             count_zero += 1
#             out += f"Dial passed (or is on) 0. Current count: {count_zero}\n"

#     else: # Turn Right
#         dial_pos += amount
#         dial_pos%=  dial_size
#         out += f"Turning dial {amount} towards right.\n"
#         out += f"Now at Position {dial_pos}. Previously {old_pos}\n"
#         if amount >= dial_size: # We did a full rotation or more.
#             multiple = math.floor(amount / dial_size)
#             count_zero += multiple
#             out += f"Dial passed 0 a total of {multiple} times. Current count: {count_zero}\n"
#             if(dial_pos == 0 and old_pos > 0): # if multiple turns also land on zero we need to count that aswell
#                 count_zero += 1
#                 out += f"Dial also landed on zero after an additional partial turn. Current count: {count_zero}\n"
#         elif(old_pos + amount >= dial_size): # Checking if we went right through 100/0
#             count_zero += 1
#             out += f"Dial passed (or is on) 0. Current count: {count_zero}\n"

out += f"Final Position: {dial_pos}. it pointed at 0 a total of {count_zero} times."
print(f"Final Position: {dial_pos}. it pointed at 0 a total of {count_zero} times.")

with open(output_path, 'w') as file:
    file.write(out)