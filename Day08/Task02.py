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

def visualise_junctions(junctions, circuits):
    visual_out = '\n\nCurrent Junctions:\n'
    for junction in junctions:
        visual_out += f"Junction No. {junction['ID']} ({junction['x']}|{junction['y']}|{junction['z']})"
        if(len(junction['connections']) > 0):
            visual_out += f"is part of circtuit {junction['circuit']} and connected to"
            for connection in junction['connections']:
                visual_out += f" {connection},"
        else:
            visual_out += f"is the only junction in circtuit {junction['circuit']}"
        visual_out += '\n'
    
    for i in range(len(circuits)):
        connected_amount =  len(circuits[i])
        visual_out += f"\nCircuit {i} contains {connected_amount} amount of Junctions"
    visual_out+='\n\n'
    return visual_out

def process_input(input):
    out = ''

    junction_boxes = []
    # Save arrays of IDs that are within the same circuit
    circuits =  []
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
            'circuit': index})
        circuits.append([index])
        index += 1
    out += visualise_junctions(junction_boxes, circuits)

    distance_list = []
    connection_calculated = [[False for x in range(len(junction_boxes))] for y in range(len(junction_boxes))]
    # Do this calculation just once to save on ressources
    print(f"Calculating Distances....")
    for i in range(len(junction_boxes)):
        current_junction = junction_boxes[i]
        #compare to every junction and save connections
        for j in range(len(junction_boxes)):
            if (i!=j) and (not connection_calculated[i][j]): #Don't consider connections twice
                compare_junction = junction_boxes[j]
                #We are not calculating the root, as we don't care about actual distance, just what is shorter. This should save on calculation time
                distance = ((current_junction['x']-compare_junction['x'])**2) + ((current_junction['y']-compare_junction['y'])**2) + ((current_junction['z']-compare_junction['z'])**2)
                if DEBUG:
                    out +=f"distance between ({current_junction['x']}|{current_junction['y']}|{current_junction['z']}) and ({compare_junction['x']}|{compare_junction['y']}|{compare_junction['z']})is {distance}\n"
                connection_calculated[j][i] = True
                connection_calculated[i][j] = True
                distance_list.append({'outgoing_ID': current_junction['ID'], 'connected_ID' : compare_junction['ID'], 'distance': distance})
    distance_list = sorted(distance_list, key=lambda d: d['distance'])
    print(f"Done with distance calculation")

    done = False
    index = 0
    final_connection_a = -1
    final_connection_b = -1
    print(f"Starting loop for runs")
    while not done:
        # Connect closest two junctions
        connection = distance_list[index]
        ID_a = connection['outgoing_ID']
        ID_b = connection['connected_ID']

        #Establish connection:
        out += f"Shortest connection between junction {ID_a} and {ID_b}\n"
        out += f"A: ({junction_boxes[ID_a]['x']}|{junction_boxes[ID_a]['y']}|{junction_boxes[ID_a]['z']})\tB: ({junction_boxes[ID_b]['x']}|{junction_boxes[ID_b]['y']}|{junction_boxes[ID_b]['z']})\n"
        junction_boxes[ID_a]['connections'].append(ID_b)
        junction_boxes[ID_b]['connections'].append(ID_a)
        #update circuits
        circuit_a = junction_boxes[ID_a]['circuit']
        circuit_b = junction_boxes[ID_b]['circuit']
        
        if(DEBUG):
            out +=f"Current circuits for a{ID_a}: {circuit_a} and b{ID_b}: {circuit_b}\n"
        #combine 2 existing circuits by making all of circuit B's boxes become circuit A
        circuit_ID = junction_boxes[ID_a]['circuit']
        other_circuit_ID = junction_boxes[ID_b]['circuit']
        if(circuit_ID == other_circuit_ID):
            #No changes neccessary
            if(DEBUG):
                out += f"\tBoth junctions part of circuit {other_circuit_ID}\n"
        else:
            if(DEBUG):
                out += f"Absorbing circuit {other_circuit_ID} into circuit {circuit_ID}"
            for junction_ID in circuits[other_circuit_ID]:
                # Append ID to circuit a
                if(DEBUG):
                    out += f"Adding {junction_ID} to circuit {circuit_ID}"
                circuits[circuit_ID].append(junction_ID)
                # Update circuit in juntion:
                junction_boxes[junction_ID]['circuit'] = circuit_ID
        
            #set old circuit to empty.
            circuits[other_circuit_ID] = []

        #check if done:
        if len(circuits[circuit_ID]) == len(junction_boxes):
            done = True
            final_connection_a = ID_a
            final_connection_b = ID_b

        if(DEBUG):
            print(f"{index} connections done")
            out +=(f"\nDone with {index} checks")
            out += visualise_junctions(junction_boxes, circuits)
        index += 1
    
    if(final_connection_a > 0):
        final_box_a = junction_boxes[final_connection_a]
        final_box_b = junction_boxes[final_connection_b]
        out += f"The last connections is done between box {final_connection_b} ({final_box_a['x']}|{final_box_a['y']}|{final_box_a['z']}) and box {final_connection_a} ({final_box_b['x']}|{final_box_b['y']}|{final_box_b['z']})"

        result = final_box_a['x'] * final_box_b['x']
    else:
        result = -1
    return (out, result)


with open(input_path, 'r') as file_in:
    input = file_in.read()
(out, result) = process_input(input)
print(f"The result is {result}")
with open(output_path, 'w') as file_out:
    file_out.write(out)