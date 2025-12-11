import os
import re
import math
import numpy as np

day = 10# Input day here

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

def draw_lights(machines, button_presses):
    out = ''
    for i in  range(len(machines)):
        out += f"Machine {i}:"
        out += f"\nGoal: ["
        for light in machines[i]['lights_goal']:
            if(light):
                out += '#'
            else:
                out += '.'
        out += '] - Current: ['    
        for light in machines[i]['lights_current']:
            if(light):
                out += '#'
            else:
                out += '.'
        out += ']'

        for j in range(len(machines[i]['buttons'])):
            out += f'\n\t- {machines[i]['buttons'][j]}. Pressed {button_presses[i][j]} times'

        out += '\n'
    out += '\n'
    return out
    
def figure_button_presses(machine):
    # Get amount of combinations:
    def lights_to_value(lights):
        length = len(lights)
        value = 0
        for i in range(length):
            if(lights[length- i- 1]):
                value +=  2 ** i

        return value
    
    def value_to_lights(value, bits):
        binary_str = f"{value:0{bits}b}"
        lights = np.full(len(binary_str), False, dtype=bool)
        for i in range(len(binary_str)):
            if int(binary_str[i]) > 0:
                lights[i] = True
        return lights

    
    class Node:
        def __init__(self, value, connections, bits):
            self.value = value
            self.connections = connections
            self.bits = bits
        
        def __str__(self):
            return f"Node of Value {self.value} ({self.value:0{self.bits}b})"
        
        def get_connections(self):
            str_out = ''
            for i in range(len(connections)):
                str_out += f'\tButton {i} leads to {self.connections[i]}\n'
            return str_out

    buttons = machine['buttons']
    if DEBUG:
        for i in range(len(buttons)):
            print(f"Button {i}: {buttons[i]}")
    lights_number = len(machine['lights_current'])
    max_combinations = 2 ** lights_number # We are considering every light as 1 bit.

    graph_nodes = []
    for value in range(max_combinations):
        connections = [None for _ in range(len(buttons))]
        graph_nodes.append(Node(value,connections,lights_number))

    # Connect Graph nodes:
    for graph_index in range(max_combinations):
        current_lights = value_to_lights(graph_index, lights_number)
        for b in range(len(buttons)):
            changed_lights = np.copy(current_lights)
            for change in buttons[b]:
                #switch lights
                changed_lights[change] = not changed_lights[change]
            
            connection_value = lights_to_value(changed_lights)
            graph_nodes[graph_index].connections[b] = connection_value

    # Breitensuche:
    search_done = False
    visited = np.full(len(graph_nodes), False)

    queue = []
    optimal_sequence = None
    start = 0 # start at 0
    goal = lights_to_value(machine['lights_goal'])
    queue.append({'val': start, 'button_sequence': []}) 

    while not search_done:
        current = queue.pop(0)
        current_val = current['val']
        if(not visited[current_val]):
            if (DEBUG):
                print(f"Looking at Value {current_val}...")
                print(f"Got here via {current['button_sequence']}")
            if current_val == goal:
                search_done = True
                if(DEBUG):
                    print(f"Goal reached")
                optimal_sequence = current['button_sequence']
            else:
                visited[current_val] = True
                current_node = graph_nodes[current_val]
                for i in range(len(buttons)):
                    next_val = current_node.connections[i]
                    if(DEBUG):
                        print(f"Button {i} leads from {current_val} to {next_val}. Adding {next_val}")
                    next_buttons = list(current['button_sequence'])
                    next_buttons.append(i)
                    queue.append({'val': next_val, 'button_sequence': next_buttons})
        else:
            if(DEBUG):
                print(f"Skipping {current_val}, cause already visited")
        


    
    if(DEBUG):
        for node in graph_nodes:
            print(node)
            print(node.get_connections())

    

    return optimal_sequence

        

        


def process_input(input):
    out = ''
    machines = []

    reg_pattern = r"\[(?P<lights>.+)\]\s*((?P<buttons>\(.+\))\s*)\s*{(?P<joltage>.+)}$"
    for line in input.split('\n'):
        match = re.search(reg_pattern, line)
        lights_string = match.group('lights')
        lights_goal = np.empty(len(lights_string), dtype=bool)
        for i in range(len(lights_string)):
            if(lights_string[i] == '#'):
                lights_goal[i] = True
            else:
                lights_goal[i] = False
        lights_current = np.full(len(lights_string), False, dtype=bool)
        buttons = []
        for button in re.findall(r'\(((\d,*)+)\)', match.group('buttons')):
            buttons.append(np.array(button[0].split(','), dtype=int))
        joltage = np.array(match.group('joltage').split(','), dtype=bool)

        machines.append({'lights_goal': lights_goal, 'lights_current' : lights_current, 'buttons' : buttons, 'joltage' : joltage})
    
    button_presses = np.zeros((len(machines), len(max(machines, key=lambda x: len(x['buttons']))['buttons'])), dtype='int')

    #How do we do this....
    for i in range(len(machines)):
        buttons_to_press = figure_button_presses(machines[i])
        for button_press in buttons_to_press:
            button_presses[i][button_press] += 1

        out += f"Press buttons {buttons_to_press} for machine {i}\n"
  
    total_presses = sum(sum(button_presses))
    out += f"A total of {total_presses} Buttons need to be pressed\n"

    return out, total_presses


with open(input_path, 'r') as file_in:
    input = file_in.read()
out, result = process_input(input)
print(f"A total of {result} Buttons need to be pressed")
with open(output_path, 'w') as file_out:
    file_out.write(out)