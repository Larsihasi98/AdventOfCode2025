import os
import re

root = os.getcwd()
current_day = os.path.join(root, "Day01")
input_path = os.path.join(current_day, 'Input.txt')
print(f"root dir = {root}")

instructions = []
with open(input_path, 'r') as file:
    for line in file:
        instructions.append(line)


dial = range(0, 100)
dial_pos = 50
count_zero = 0
#setup regex:
p = re.compile(r'^(?P<direction>L|R)(?P<amount>\d+$)')
for instruction in instructions:
    #print(instruction)
    left = True
    m = p.match(instruction)
    direction = m.group('direction')
    if direction == 'R':
        left = False
    amount = int(m.group('amount'))

    if left:
        dial_pos -= amount
        print(f"Turning dial {amount} towards left.")
        #print(f"Debug: {dial_pos}, {dial_pos%100}")
        print(f"Now at Position {dial[dial_pos%100]}")
    else:
        dial_pos += amount
        print(f"Turning dial {amount} towards right.")
        print(f"Now at Position {dial[dial_pos%100]}")
    
    if(dial_pos%100 == 0):
        count_zero += 1
        print(f"Dial points at 0. Current count is {count_zero}")
    
#print(f"Dial position total = {dial_pos}. Modified that's {dial_pos%100}")
print(f"Final Position: {dial[dial_pos%100]}. it pointed at 0 a total of {count_zero} times.")