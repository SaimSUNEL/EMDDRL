from Environments import RLTwoRoomsEnvironment
import networkx as nx
import os
import pickle

environment = RLTwoRoomsEnvironment.RLTwoRoomsEnvironment('v2', is_step_restricted=True, step_limit=500)
environment_adjacency_dict = environment.getEnvironmentGraph()
G = nx.Graph()



for node in environment_adjacency_dict:
    neighbors = environment_adjacency_dict[node]
    G.add_node(node)
    for neighbor in neighbors:
        G.add_edge(node, neighbor)


experiment_folder_path = "../../TwoRoomExperiments/AccuracyExperimentsTwoRoom(Online)/ActionNoise(0.9)StepLimit(200)/STEPLIMITEQUALLYBALANCED"

EMDD_RESULTS = dict()


subgoal_regions = {1: [94, 115]}
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
        if name == "EMDDSELECTEDSTATES.pickle":
            configuration = root.split("EMDD/")[1].split("/")
            model = configuration[0]
            search_set = configuration[1]
            skip_factor = configuration[2]
            if model not in EMDD_RESULTS:
                EMDD_RESULTS[model] = dict()
                REGION_DISTANCE_RESULTS[model] = dict()
            if search_set not in EMDD_RESULTS[model]:
                EMDD_RESULTS[model][search_set] = dict()
                REGION_DISTANCE_RESULTS[model][search_set] = dict()
            if skip_factor not in EMDD_RESULTS[model][search_set]:
                EMDD_RESULTS[model][search_set][skip_factor] = {"subgoals": pickle.load(open(root+"/"+name, "rb"))}

            run_time_file = open(root+"/RUN.txt")
            for line in run_time_file:
                line = line.strip("\n\r\t")
                if "Average EMDD runtime" in line:
                    average_run_time = float(line.split(" : ")[1])
                    break
            run_time_file.close()
            EMDD_RESULTS[model][search_set][skip_factor]["average run time"] = average_run_time

            found_subgoals = EMDD_RESULTS[model][search_set][skip_factor]["subgoals"]
            average_region_distance = 0.0
            for s in found_subgoals:

                closest_distance = float('inf')
                for region in subgoal_regions:
                    distance_to_region = calculate_distance_to_region(s, subgoal_regions[region])
                    closest_distance = min(closest_distance, distance_to_region)
                average_region_distance += closest_distance

            REGION_DISTANCE_RESULTS[model][search_set][skip_factor] = average_region_distance / len(found_subgoals)

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

    for model in EMDD_RESULTS:
        for search_set in EMDD_RESULTS[model]:
            for skip_factor in EMDD_RESULTS[model][search_set]:

                subgoal_results = EMDD_RESULTS[model][search_set][skip_factor]["subgoals"]

                hit_count = 0
                for i in subgoal_results:
                    if i in expected_subgoals:
                        hit_count += 1
                precision = float(hit_count) / float(len(subgoal_results))
                recall = float(hit_count) / float(len(expected_subgoals))
                try:
                    f1 = 2 * float(precision) * float(recall) / (float(precision) + float(recall))
                except:
                    f1 = 0
                # print("DD radius %d Precision - %.3f" % (radius, precision))

                EMDD_RESULTS[model][search_set][skip_factor]["radius-"+str(radius)] = precision
print("Okeee")

BEST_MODELS = dict()
FASTEST_MODELS = dict()
for radius in [0, 1, 2, 3, 4]:

    best_models = set()
    best_precision_score = -float('inf')
    for model in EMDD_RESULTS:
        for search_set in EMDD_RESULTS[model]:
            for skip_factor in EMDD_RESULTS[model][search_set]:
                precision_score = EMDD_RESULTS[model][search_set][skip_factor]["radius-"+str(radius)]
                if precision_score > best_precision_score:
                    best_precision_score = precision_score
    fastest_configuration = None
    best_run_time = float('inf')

    for model in EMDD_RESULTS:
        for search_set in EMDD_RESULTS[model]:
            for skip_factor in EMDD_RESULTS[model][search_set]:
                precision_score = EMDD_RESULTS[model][search_set][skip_factor]["radius-"+str(radius)]
                if precision_score == best_precision_score:
                    best_models.add((model, search_set, skip_factor, precision_score))

                    run_time = EMDD_RESULTS[model][search_set][skip_factor]["average run time"]
                    if run_time < best_run_time:
                        best_run_time = run_time
                        fastest_configuration = (model, search_set, skip_factor)

    BEST_MODELS[radius] = best_models
    TABLE_STRING += "%.2f (%.4f)\t" % (best_precision_score, best_run_time)

    FASTEST_MODELS[radius] = (fastest_configuration, best_run_time)
print("\n\n")
print(BEST_MODELS)
for radius in BEST_MODELS:
    print("******** "+str(radius))
    for config in BEST_MODELS[radius]:
        print("\t", config)
    print("Fastest configuration : ", FASTEST_MODELS[radius])

print("\n\nRegion Distance")

best_regional_distance = float('inf')

for model in REGION_DISTANCE_RESULTS:
    for search_set in REGION_DISTANCE_RESULTS[model]:
        for skip_factor in REGION_DISTANCE_RESULTS[model][search_set]:
            best_regional_distance = min(best_regional_distance, REGION_DISTANCE_RESULTS[model][search_set][skip_factor])
            print("%s = %.3f" % ((model, search_set, skip_factor), REGION_DISTANCE_RESULTS[model][search_set][skip_factor]))






fastest_region_config = None
best_run_time = float('inf')
best_regional_models = []



for model in REGION_DISTANCE_RESULTS:
    for search_set in REGION_DISTANCE_RESULTS[model]:
        for skip_factor in REGION_DISTANCE_RESULTS[model][search_set]:
            regional_distance = REGION_DISTANCE_RESULTS[model][search_set][skip_factor]
            if regional_distance == best_regional_distance:
                best_regional_models.append((model, search_set, skip_factor))
                run_time = EMDD_RESULTS[model][search_set][skip_factor]["average run time"]
                if run_time < best_run_time:
                    best_run_time = run_time
                    fastest_region_config = (model, search_set, skip_factor)


print("Best regional distance : ", best_regional_distance)
print("Fastest regional config : ", (best_run_time, fastest_configuration))
TABLE_STRING += "%.2f (%.4f)" % (best_regional_distance, best_run_time)
print(TABLE_STRING)