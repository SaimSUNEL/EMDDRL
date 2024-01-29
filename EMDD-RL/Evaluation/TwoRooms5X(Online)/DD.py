from Environments import RLTwoRoomsEnvironment
import networkx as nx
import os
import pickle

environment = RLTwoRoomsEnvironment.RLTwoRoomsEnvironment("v10", is_step_restricted=True, step_limit=500)
environment_adjacency_dict = environment.getEnvironmentGraph()
G = nx.Graph()
# environment.renderEnvironment()



for node in environment_adjacency_dict:
    neighbors = environment_adjacency_dict[node]
    G.add_node(node)
    for neighbor in neighbors:
        G.add_edge(node, neighbor)


experiment_folder_path = "../../TwoRoomExperiments5X/AccuracyExperimentsTwoRoom5X(Online)/ActionNoise(0.9)StepLimit(700)/STEPLIMITEQUALLYBALANCED"

DD_RESULT = None


subgoal_regions = {1: [319, 390]}
REGION_DISTANCE_RESULTS = dict()
TABLE_STRING = ""
def calculate_distance_to_region(state, region_states):
    average_distance = 0.0
    for t in region_states:
        average_distance += nx.shortest_path_length(G, state, t)
    return average_distance / len(region_states)

for root, dirs, files in os.walk(experiment_folder_path, topdown=True):
    # print(root)
    for name in files:
        # print(name)
        if name == "DDSELECTEDSTATES.pickle":
            DD_RESULT = pickle.load(open(root+"/"+name, "rb"))

            run_time_file = open(root + "/RUN.txt")
            for line in run_time_file:
                line = line.strip("\n\r\t")
                if "Average DD run time" in line:
                    average_run_time = float(line.split(" : ")[1])
                    break
            run_time_file.close()

            average_region_distance = 0.0
            for s in DD_RESULT:

                closest_distance = float('inf')
                for region in subgoal_regions:
                    distance_to_region = calculate_distance_to_region(s, subgoal_regions[region])
                    closest_distance = min(closest_distance, distance_to_region)
                average_region_distance += closest_distance

            REGION_DISTANCE_RESULTS = average_region_distance / len(DD_RESULT)
            print(root, name)

print(DD_RESULT)



gate_states = []
for region in subgoal_regions:
    for s in subgoal_regions[region]:
        gate_states.append(s)



for radius in [0, 1, 2, 3, 4]:
    expected_subgoals = set()
    for gate_state in gate_states:
        ego_graph = nx.ego_graph(G, gate_state, radius=radius)  # nodes at depth k
        for n in ego_graph.nodes:
            expected_subgoals.add(n)

    print(expected_subgoals)
    color_information = dict()
    for state in expected_subgoals:
        color_information[state] = (255, 0, 255)
    environment.setEnableColorState(True)
    environment.setColorData(color_information)
    environment.renderEnvironment()
    environment.saveEnvironmentImage("images/"+str(radius)+".png")

    hit_count = 0
    for i in DD_RESULT:
        if i in expected_subgoals:
            hit_count += 1
    precision = float(hit_count) / float(len(DD_RESULT))
    recall = float(hit_count) / float(len(expected_subgoals))
    try:
        f1 = 2 * float(precision) * float(recall) / (float(precision) + float(recall))
    except:
        f1 = 0
    print("DD radius %d Precision - %.3f" % (radius, precision))
    TABLE_STRING += "%.2f (%.4f)\t" % (precision, average_run_time)


print("Regional distance : ", REGION_DISTANCE_RESULTS)
TABLE_STRING += "%.2f (%.4f)" % (REGION_DISTANCE_RESULTS, average_run_time)
print(TABLE_STRING)