import os
import re
import math
import numpy as np
from treelib import Tree

day = 10# Input day here

test = True # Change this to run program with the smaller testinput for debug
DEBUG = True # Change this to have debug outputs

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
    buttons = machine['buttons']
    if DEBUG:
        for i in range(len(buttons)):
            print(f"Button {i}: {buttons[i]}")
    combinations = 2 ** len(machine['lights_current']) # We are considering every light as 1 bit.
    #combinations_reached = np.full(combinations, -1, dtype=int) # For every combination, remember the amount of button presses we needed to get there. Negative value means we haven't reached this combination yet
    best_path = [None for _ in range(combinations)]
    # np.empty(combinations, dtype=str) # Save Node_IDs to the shortest way here
    #convert array of lights to integer
    def light_combination(lights):
        length = len(lights)
        out = 0
        for i in range(length):
            if(lights[length- i- 1]):
                out +=  2 ** i

        return out
    
    finished = False
    #Use a redundant search to try different combinations:
    tree = Tree()
    finished = False
    no_of_nodes = 0

    class Node_Structure:
        def __init__(self, last_button, lights, combination):
            self.last_button = last_button
            self.lights = np.copy(lights)
            self.combination = combination
            self.debug_out = f"Button {last_button}, Lights: {combination:04b}"
        
        def __str__(self):
            return f"{self.last_button}, lights: {self.lights}. Combination: {self.combination}"
    
    current_lights = np.copy(machine['lights_current'])
    current_combination = light_combination(current_lights)
    current_data = Node_Structure(None, current_lights, current_combination)
    
    tree.create_node(f"{no_of_nodes}", data = current_data)
    current_node = tree[tree.root]
    #combinations_reached[current_combination] = tree.depth(current_node)
    best_path[current_combination] = current_node.identifier
    while(not finished):
        #print(f"current_node at start: {current_node.identifier}, lights: {current_node.data.lights}")
        current_data = current_node.data
        current_ID = current_node.identifier
        
        current_lights = np.copy(current_data.lights)
        current_combination = current_data.combination
        buttons_tried = len(tree.children(current_ID))

        # If we haven't tried all follow up combinations of this node, try the next button
        next_button = buttons_tried
        if next_button < len(buttons): #Once we tried last Button, go back
            for change in buttons[next_button]:
                #switch lights
                current_lights[change] = not current_lights[change]
            current_combination = light_combination(current_lights)
            #print(f"Lights changed from {current_data.lights} to {current_lights}")
            node_data = Node_Structure(next_button, current_lights, current_combination)
            
            print(f"Current depth {tree.depth(current_ID)}")

            
            #Check if this is the first time we reach this combination:
            if(best_path[current_combination] is None):
                #update current_node
                no_of_nodes += 1
                new_node = tree.create_node(f"{no_of_nodes}", data = node_data, parent = current_ID)
                current_node = new_node
                current_ID = current_node.identifier
                #combinations_reached[current_combination] = tree.depth(current_ID)
                best_path[current_combination] = current_ID
                print(f"First time reaching combination {current_combination} ({current_combination:04b})")
                
            elif(tree.depth(current_ID) < tree.depth(best_path[current_combination])):
                # Found a more efficient route to combination
                # move node over here and update it's data
                print(f"Found more efficient Path to {current_combination} ({current_combination:04b})")
                print(f"Moving Node {tree[best_path[current_combination]].tag} over to {tree[current_ID].tag}")
                tree.move_node(best_path[current_combination], current_ID)
                tree[best_path[current_combination]].data = node_data

            else:
                #We have already reached this combination before. Go back to previous node
                # Add a note but don't save it's id in our fastest combination list
                print(f"Found less efficient Path to {current_combination} ({current_combination:04b})")
                no_of_nodes += 1
                tree.create_node(f"{no_of_nodes}", data = node_data, parent = current_ID)
                # Don't switch to new ID

        
        else:
            #We have tried every button and didn't arrive at a satisfying conclusion
            if(current_node.is_root(tree.identifier)):
               #We checked every possibility
               finished = True
            else:
                current_node = tree.parent(current_ID)
        
        if(DEBUG):
            tree.show(data_property='debug_out')
            for i in range(len(best_path)):
                if best_path[i] is None:
                    print(f"No Path for {i:04b} discovered yet")
                else:
                    print(f"Best Path for {i:04b} is node {tree[best_path[i]].tag} ({tree[best_path[i]]})")
            tree.show()
            

    # Get best path to goal:
    goal = light_combination(machine['lights_goal'])
    optimal_path = best_path[goal]
    optimal_buttons = np.zeros(len(buttons), dtype=int)

    for node_id in tree.rsearch(optimal_path):
        node = tree.get_node(node_id)
        button = node.data.last_button
        
        if button is not None:
            optimal_buttons[button] += 1
    
    if(DEBUG):
        tree.show(data_property='debug_out')
        for i in range(len(best_path)):
            print(f"Best starting Node for {i:04b} is node {tree[best_path[i]].tag} ({tree[best_path[i]]})")
        tree.show()

    return optimal_buttons

        

        


def process_input(input):
    out = ''
    machines = []
    button_presses = []

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
    
    

    ##How do we do this....
    #for i in range(len(machines)):
    #    buttons_to_press = figure_button_presses(machines[i])
    #    print(buttons_to_press)
    
    buttons_to_press = figure_button_presses(machines[0])
    print(buttons_to_press)
    
    out += draw_lights(machines, button_presses)
    

    return out


with open(input_path, 'r') as file_in:
    input = file_in.read()
out = process_input(input)

with open(output_path, 'w') as file_out:
    file_out.write(out)