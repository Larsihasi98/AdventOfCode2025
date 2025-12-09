import os
import re
import math

day = 8# Input day here

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

def visualise_junctions(junctions):
    visual_out = '\n\nCurrent Junctions:\n'
    for junction in junctions:
        visual_out += f"Junction No. {junction['ID']} ({junction['x']}|{junction['y']}|{junction['z']})"
        if(len(junction['connections']) > 0):
            visual_out += f"is part of circtuit {junction['circuit']} with"
            for connection in junction['connections']:
                visual_out += f" {connection},"
        else:
            visual_out += f"is not connected to another junction."
        visual_out += '\n'
    return visual_out

def process_input(input):
    out = ''

    junction_boxes = []
    index = 0
    #Setup Junctions
    for line in input.split('\n'):
        [x,y,z] = line.split(',')
        junction_boxes.append({
            'ID': index,
            'x': int(x),
            'y': int(y),
            'z': int(z),
            'connections': [],
            'circuit': False})
        index += 1
    out += visualise_junctions(junction_boxes)

    distance_list = []
    # Do this calculation just once to save on ressources
    for i in range(len(junction_boxes)):
        current_junction = junction_boxes[i]
        connections = []
        #compare to every junction and save connections
        for j in range(len(junction_boxes)):
            compare_junction = junction_boxes[j]
            #We are not calculating the root, as we don't care about actual distance, just what is shorter. This should save on calculation time
            distance = ((current_junction['x']-compare_junction['x'])**2) + ((current_junction['y']-compare_junction['y'])**2) + ((current_junction['z']-compare_junction['z'])**2)
            out +=f"distance between ({current_junction['x']}|{current_junction['y']}|{current_junction['z']}) and ({compare_junction['x']}|{compare_junction['y']}|{compare_junction['z']})is {distance}\n"
            connections.append({'connected_ID' : compare_junction['ID'], 'distance': distance})
        distance_list.append(connections)

    amount_to_connect = 1000 # how many connections
    if(test):
        amount_to_connect = 10
    
    current_circuits = 0
    # Save established connections in a 2 dimensional array where x is the ID of Junction 1 and y is the ID of junction 2
    circuits_connected = [[False for x in range(len(distance_list))] for y in range(len(distance_list))]
    # Save arrays of IDs that are within the same circuit
    circuits =  []
    print(f"Starting loop for {amount_to_connect} runs")
    for i in range(0, amount_to_connect):
        # Connect closest two junctions
        ID_a = -1
        ID_b = -1
        min_distance = -1

        for a in range(0, len(junction_boxes)):
            for b in range(0, len(junction_boxes)):
                if a != b: # Don't compare to self
                    if not circuits_connected[a][b]: #skip established connections
                        current_distance = distance_list[a][b]['distance']
                        if(DEBUG):
                            out += f"Distance between {a} and {b} is {current_distance}\n"
                        if min_distance < 0:
                            min_distance = current_distance
                            ID_a = a
                            ID_b = b
                        elif current_distance < min_distance:
                            if(DEBUG):
                                out += f"{current_distance} is shorter than {min_distance}\n"
                            min_distance = current_distance
                            ID_a = a
                            ID_b = b
                    else:
                        if(DEBUG):
                            out += f"Connection between {a} and {b} already exists"
        
        #Establish connection:
        out += f"Shortest connection between junction {ID_a} and {ID_b}\n"
        circuits_connected[ID_a][ID_b] = True
        circuits_connected[ID_b][ID_a] = True
        junction_boxes[ID_a]['connections'].append(ID_b)
        junction_boxes[ID_b]['connections'].append(ID_a)
        out += f"A: {junction_boxes[ID_a]['x']}|{junction_boxes[ID_a]['y']}|{junction_boxes[ID_a]['y']})\tB: {junction_boxes[ID_b]['x']}|{junction_boxes[ID_b]['y']}|{junction_boxes[ID_b]['y']})"
        #update circuits
        circuit_a = junction_boxes[ID_a]['circuit']
        circuit_b = junction_boxes[ID_b]['circuit']
        if(DEBUG):
            out +=f"Current circuits for a{ID_a}: {circuit_a} and b{ID_b}: {circuit_b}\n"
        if((not circuit_a) and (not circuit_b)):
            # Neither Box in circuit, we can create a new one.
            circuit_ID = current_circuits
            if(DEBUG):
                out +=f"\tcreating circuit {circuit_ID}\n"
            current_circuits += 1
            junction_boxes[ID_a]['circuit'] = circuit_ID
            junction_boxes[ID_b]['circuit'] = circuit_ID
            circuits.append([ID_a, ID_b])

        elif(circuit_a and (not circuit_b)):
            # only box a already in circuit:
            circuit_ID = junction_boxes[ID_a]['circuit']
            if(DEBUG):
                out +=f"\tAppending junction {ID_b} to circuit {circuit_ID}\n"
            junction_boxes[ID_b]['circuit'] = circuit_ID
            circuits[circuit_ID].append(ID_b)

        elif((not circuit_a) and circuit_b):
            # only box b already in circuit:
            circuit_ID = junction_boxes[ID_b]['circuit']
            if(DEBUG):
                out +=f"\tAppending junction {ID_a} to circuit {circuit_ID}\n"
            junction_boxes[ID_a]['circuit'] = circuit_ID
            circuits[circuit_ID].append(ID_a)

        else:
            #combine 2 existing circuits by making all of circuit B's boxes become circuit A
            circuit_ID = junction_boxes[ID_a]['circuit']
            other_circuit_ID = junction_boxes[ID_b]['circuit']
            if(circuit_ID == other_circuit_ID):
                #No changes neccessary
                if(DEBUG):
                    out += f"\tBoth junctions part of circuit {other_circuit_ID}\n"
            else:
                if(DEBUG):
                    out += f"Absorbing {other_circuit_ID} into circuit {circuit_ID}"
                for junction_ID in circuits[other_circuit_ID]:
                    # Append ID to circuit a
                    circuits[circuit_ID].append(junction_ID)
                    # Update circuit in juntion:
                    junction_boxes[junction_ID]['circuit'] = circuit_ID
            
            #set old circuit to empty.
            circuits[other_circuit_ID] = []

        if(DEBUG):
            print(f"{i+1} out of {amount_to_connect} check done")
            out += visualise_junctions(junction_boxes)

    #Get Circuit sizes:
    circuit_sizes = []
    for i in range(len(circuits)):
        connected_amount =  len(circuits[i])
        out += f"\nCircuit {i} contains {connected_amount} amount of Junctions"
        circuit_sizes.append(connected_amount)
    circuit_sizes.sort()
    circuit_sizes.reverse()
    if(DEBUG):
        print(circuit_sizes)
    multiply_amount = 3

    result = 1

    for i in range(multiply_amount):
        result *= circuit_sizes[i]

    return (out, result)


with open(input_path, 'r') as file_in:
    input = file_in.read()
(out, result) = process_input(input)
print(f"The result is {result}")
with open(output_path, 'w') as file_out:
    file_out.write(out)