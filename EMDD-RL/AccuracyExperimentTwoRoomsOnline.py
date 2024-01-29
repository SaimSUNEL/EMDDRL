import os
import time

from Environments import RLTwoRoomsEnvironment
from MIL.Methods.DD import DiverseDensity
from MIL.Methods.EMDD import EMDD
import sys
t = time.localtime()
import Graph.TransitionGraph
from timeit import default_timer as timer

start_time = timer()
import pickle
# G = pickle.load(open("MIL/data/TwoRoomsEnvironmentDistanceDict.pck", "rb"))
t = time.localtime()
experiment_date = "%02d-%02d-%d#%02d-%02d-%02d" % (t.tm_mday, t.tm_mon, t.tm_year, t.tm_hour, t.tm_min, t.tm_sec)

emdd_results = []
dd_results = []
eliminated_states = [188, 187, 208, 207, 186, 165, 166, 167, 206, 186, 164, 143, 144, 145, 146, 205, 184, 185,
                     163, 142, 143, 144, 145, 146]
average_count = 0

# DATASETS
# Step limit (200)
# Without step limit
    # first 20 negative next 20 positive bag
    # 20 only positive bag

STEP_LIMIT_EQUALLY_BALANCED = 1
EQUALLY_BALANCED = 3

algorithm = "DD" # "EMDD

DATASET = STEP_LIMIT_EQUALLY_BALANCED

NEGATIVE_BAG_COUNT = 20
POSITIVE_BAG_COUNT = 20

# EMDD.H_SET, EMDD.H_NEIGHBOR, EMDD.H_ALL
SEARCH_SET = EMDD.H_ALL

# EMDD.EXPONENTIAL
METHOD = EMDD.EXPONENTIAL

# 1, 2, 3, 4
SKIPPING_FACTOR = 4

# H_SET - LINEAR - 1->1.0, 2->1.0, 3->0.99, 4->0.99
# H_SET - Exponential - 1->1.0, 2->1.0, 3->1.0, 4->0.98
# H_ALL - LINEAR - 1->1.0, 2->1.0, 3->1.0, 4->0.99
# H_ALL - Exponential - 1->1.0, 2->1.0, 3->1.0, 4->0.98
# DD - 1.0
if(len(sys.argv)>2):
    for setting in sys.argv:
        if setting.__contains__("data="):
            DATASET = int(setting.split("=")[1])
        elif setting.__contains__("algh="):
            algorithm = setting.split("=")[1]
        elif setting.__contains__("search="):
            SEARCH_SET = setting.split("=")[1]
        elif setting.__contains__("method="):
            METHOD = setting.split("=")[1]
        elif setting.__contains__("skip="):
            SKIPPING_FACTOR = int(setting.split("=")[1])
        elif setting.__contains__("neg="):
            NEGATIVE_BAG_COUNT = int(setting.split("=")[1])
        elif setting.__contains__("pos="):
            POSITIVE_BAG_COUNT = int(setting.split("=")[1])

dataset_defs  = {STEP_LIMIT_EQUALLY_BALANCED: "STEPLIMITEQUALLYBALANCED",
                 EQUALLY_BALANCED: "EQUALLYBALANCED"}

print("Dataset : ", dataset_defs[DATASET])
print("Algorithm : ", algorithm)
print("SEARCH :" , SEARCH_SET)
print("METHOD : ", METHOD)
print("SKIP : ", SKIPPING_FACTOR)
print("NEGATIVE BAG COUNT", NEGATIVE_BAG_COUNT)
print("POSITIVE BAG COUNT", POSITIVE_BAG_COUNT)

if DATASET == STEP_LIMIT_EQUALLY_BALANCED:
    data_version = "ActionNoise(0.9)StepLimit(200)"
elif DATASET == EQUALLY_BALANCED:
    data_version = "ActionNoise(0.9)"

included_experiment_count = 0

total_dd_time = 0

total_emdd_time = 0

# Experiment folder
if algorithm == "EMDD":
    experiment_folder = "AccuracyExperiments(Online)/"+data_version+"/"+dataset_defs[DATASET]+"/"+algorithm+"/"+METHOD+"/"+SEARCH_SET+"/"+str(SKIPPING_FACTOR)
else:
    experiment_folder = "AccuracyExperiments(Online)/"+data_version+"/"+dataset_defs[DATASET]+"/"+algorithm

experiment_folder += "/#"+str(POSITIVE_BAG_COUNT)+"Positive"+"#"+str(NEGATIVE_BAG_COUNT)+"Negative/"+experiment_date

if not os.path.exists(experiment_folder):
    create_path = "AccuracyExperiments(Online)"
    for i in experiment_folder.split("/")[1:]:
        create_path += "/" + i
        if not os.path.exists(create_path):
            os.mkdir(create_path)

experiment_folder += "/"

run_file_name = "RUN.txt"
run_file = open(experiment_folder+run_file_name, "w")

run_file.write("DATASET:"+dataset_defs[DATASET]+"\n")
run_file.write("ALGORITHM:"+algorithm+"\n")
run_file.write("POSITIVEBAG:"+str(POSITIVE_BAG_COUNT)+"\n")
run_file.write("NEGATIVEBAG:"+str(NEGATIVE_BAG_COUNT)+"\n")
if algorithm == "EMDD":
    run_file.write("SEARCHSET:"+SEARCH_SET+"\n")
    run_file.write("METHOD:"+METHOD+"\n")
    run_file.write("SKIP:"+str(SKIPPING_FACTOR)+"\n")



for experiment_id in range(1, 101):
    # how many experiments are used for experiment
    transition_graph = Graph.TransitionGraph.TransitionGraph(None)

    included_experiment_count += 1

    data_directory = "MIL/data/TwoRoomsQAgentTrajectories/"
    experiment_number = experiment_id

    file_name = "TwoRoomsBagExperiment["+str(experiment_number)+"].txt"

    print("File to be opened : ", file_name)
    data_file = open(data_directory + data_version+"/"+file_name, "r");
    positive_bags = []
    negative_bags = []
    negative_bag_count = 0
    positive_episodes = []
    negative_episodes = []

    for line in data_file:
        parts = line.split(",")
        bag = []
        for i in range(1, len(parts)):
            # print("parts ", int(parts[i]), " - ", int(parts[i]) in eliminated_states)

            if int(parts[i]) in eliminated_states:
                pass
            else:
                bag.append(int(parts[i]))

        if DATASET == STEP_LIMIT_EQUALLY_BALANCED:
            if parts[0] == "1":# len(parts) <= 201:
                positive_bags.append(list(set(bag)))
                positive_episodes.append(bag)

            else:
                negative_bags.append(list(set(bag)))
                negative_episodes.append(bag)

        elif DATASET == EQUALLY_BALANCED:
            if negative_bag_count>=20:
                positive_bags.append(list(set(bag)))
            else:
                negative_bags.append(list(set(bag)))
                negative_bag_count += 1


    print("Total Positive bag count in experiment : ", len(positive_bags))
    print("Total Negative bag count in experiment : ", len(negative_bags))
    data_file.close()

    # only use first 20 episode data...
    if DATASET == STEP_LIMIT_EQUALLY_BALANCED:
        positive_bags = positive_bags[0:POSITIVE_BAG_COUNT]
        negative_bags = negative_bags[0:NEGATIVE_BAG_COUNT]
        positive_episodes = positive_episodes[0:POSITIVE_BAG_COUNT]
        negative_episodes = negative_episodes[0:NEGATIVE_BAG_COUNT]
    elif DATASET == EQUALLY_BALANCED:
        positive_bags = positive_bags[0:POSITIVE_BAG_COUNT]
        negative_bags = negative_bags[0:NEGATIVE_BAG_COUNT]


    print("ALgorithm : ", algorithm)
    print("DATASET : ", dataset_defs[DATASET])
    print("Data Version ", data_version)
    print("positive bag count : ", len(positive_bags))
    print("negative bag count : ", len(negative_bags))
    # # construnct the transition graph from selected negative and positive episodes...
    for pos_episode in positive_episodes:
        # construnct the graph...
        for i in range(len(pos_episode) - 1):
            transition_graph.add2Vertices(pos_episode[i], pos_episode[i + 1])
    #
    for neg_episode in negative_episodes:
        # construnct the graph...
        for i in range(len(neg_episode) - 1):
            transition_graph.add2Vertices(neg_episode[i], neg_episode[i + 1])

    STATES_TO_TEST = set()
    for Bi in positive_bags:
        for state in Bi:
            STATES_TO_TEST.add(state)

    DD = DiverseDensity(positive_bags, negative_bags, transition_graph, distance_metric=DiverseDensity.DISTANCE_METRIC_GRAPH)
    emdd = EMDD(positive_bags, negative_bags, transition_graph, STATES_TO_TEST, METHOD, distance_metric=DiverseDensity.DISTANCE_METRIC_GRAPH,
                H_CHECK=SEARCH_SET, SKIPPING_FACTOR=SKIPPING_FACTOR)
    if algorithm == "EMDD":
        print("EMDD working")
        emdd_start_time = timer();
        emdd_result = emdd()
        emdd_end_time = timer();
        total_emdd_time += emdd_end_time - emdd_start_time
        print("EMDD run time : ", emdd_end_time-emdd_start_time, " seconds")
        average_count += emdd.average_loop_count
        emdd_results.append(emdd_result[0])

    # for DD calculation...
    if algorithm == "DD":
        print("DD is working")
        max_value = -1*float("inf")
        max_dd_state = 0
        all_instances = set()
        for b in positive_bags:
             for instan in b:
                 all_instances.add(instan)
        #
        # # for k in positive_bags:
        # #     for i in k:
        dd_start_time = timer()
        for i in all_instances:
                if i in eliminated_states:
                    continue
                dd_value = DD(i)
                # print("Diverse density : ", i , " - ", dd_value)
                if dd_value > max_value:
                    max_value = dd_value
                    max_dd_state = i
        dd_end_time = timer()
        total_dd_time += dd_end_time - dd_start_time
        print("DD run time : ", dd_end_time - dd_start_time, " seconds")
        dd_results.append(max_dd_state)

dd_elements = set(dd_results)
emdd_elements = set(emdd_results)

two_rooms_env_v2 = RLTwoRoomsEnvironment.RLTwoRoomsEnvironment('v2', is_step_restricted=True, step_limit=500)
elements = dd_elements if algorithm == "DD" else emdd_elements
counts = dd_results if algorithm == "DD" else emdd_results

pickle.dump(counts,open(experiment_folder+algorithm+"SELECTEDSTATES.pickle", "wb"))


two_rooms_env_v2.setEnableSubgoalDisplay(True)

subgoals_dict = {}
for subgoal in elements:
    subgoals_dict[subgoal] = (counts.count(subgoal)+10)*5
print(subgoals_dict)
two_rooms_env_v2.setDisplaySubgoal(subgoals_dict)
two_rooms_env_v2.renderEnvironment()
if algorithm == "EMDD":
    two_rooms_env_v2.setEnvironmentImageTitle(data_version+""+dataset_defs[DATASET]+""+algorithm+SEARCH_SET+METHOD+"#"+str(POSITIVE_BAG_COUNT)+"Positive#"+str(NEGATIVE_BAG_COUNT))
else:
    two_rooms_env_v2.setEnvironmentImageTitle(data_version+""+dataset_defs[DATASET]+""+algorithm+"#"+str(POSITIVE_BAG_COUNT)+"Positive#"+str(NEGATIVE_BAG_COUNT))

two_rooms_env_v2.renderEnvironment()
if algorithm == "EMDD":
    two_rooms_env_v2.saveEnvironmentImage(experiment_folder+data_version+""+dataset_defs[DATASET]+""+algorithm+SEARCH_SET+METHOD+"#"+str(POSITIVE_BAG_COUNT)+"Positive#"+str(NEGATIVE_BAG_COUNT)+"Negative.png")
else:
    two_rooms_env_v2.saveEnvironmentImage(experiment_folder+data_version+""+dataset_defs[DATASET]+""+algorithm+"#"+str(POSITIVE_BAG_COUNT)+"Positive#"+str(NEGATIVE_BAG_COUNT)+"Negative.png")


print("Total experiment count : ", included_experiment_count)
print("\n")
print("ALgorithm : ", algorithm)
print("DATASET : ", dataset_defs[DATASET])
if algorithm == "EMDD":
    print("EMDD search set : "+SEARCH_SET)
    print("EMDD method : "+METHOD)
    print("Total EMDD run time : ", total_emdd_time)
    print("Average EMDD runtime : ", float(total_emdd_time) / float(included_experiment_count))
    print("Average loop : ", float(average_count)/float(included_experiment_count))
    print("EMDD skip factor : "+str(SKIPPING_FACTOR))
    run_file.write("Total EMDD Run Time : "+ str(total_emdd_time)+"\n")
    run_file.write("Average EMDD runtime : "+str(float(total_emdd_time) / float(included_experiment_count))+"\n")
    run_file.write("EMDD Average loop : "+ str(float(average_count)/float(included_experiment_count))+"\n")
    run_file.write("EMDD skip factor : "+ str(SKIPPING_FACTOR)+"\n")


elif algorithm == "DD":
    print("Total DD run time : ", total_dd_time)
    print("Average DD run time : ", float(total_dd_time) / float(included_experiment_count))
    run_file.write("Total DD run time : "+str(total_dd_time)+"\n")
    run_file.write("Average DD run time : "+str(float(total_dd_time) / float(included_experiment_count))+"\n")


elements = counts
ground_truth_for_subgoals = [71, 72,74,75,
                             92, 93, 94, 95, 96,
                             113, 114, 115, 116, 117,
                             134,135, 137, 138]

hit_count = 0
for i in elements:
    if i in ground_truth_for_subgoals:
        hit_count += 1
precision = float(hit_count) / float(len(elements))
recall = float(hit_count) / float(len(ground_truth_for_subgoals))
try:
    f1 = 2 * float(precision) * float(recall) / (float(precision) + float(recall))
except:
    f1 = 0
print("Precision : ", precision)
run_file.write("Precisition : " + str(precision))
run_file.close()

if len(sys.argv) == 1:
    input("")

print("Found state : ", elements)