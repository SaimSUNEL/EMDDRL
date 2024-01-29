import os
import time

from Environments import RLFourRoomsEnvironment
from MIL.Methods.DD import DiverseDensity
from MIL.Methods.EMDD import EMDD
import sys
from timeit import default_timer as timer

t = time.localtime()
experiment_date = str(t.tm_year)+"-"+str(t.tm_mon)+"-"+str(t.tm_mday)
experiment_time = str(t.tm_hour)+":"+str(t.tm_min)+":"+str(t.tm_sec)

start_time = timer()
import pickle
G = pickle.load(open("../MIL/data/FourRoomsEnvironmentDistanceDict.pck", "rb"))


subgoal_results = []

eliminated_states = [183,184, 185,
                     204,205,206,
                     246, 247, 248,
                     267,268,269]


average_count = 0

# Parameters of EMDD
# starting seed states
# H_ALL or H_NEIGHBOR
# LINEAR or EXPONENTIAL
# time and loop count

# DATASETS
# Step limit (200)
# Without step limit
    # first 20 negative next 20 positive bag
    # 20 only positive bag

STEP_LIMIT_EQUALLY_BALANCED = 1
STEP_LIMIT_ONLY_POSITIVE = 2
EQUALLY_BALANCED = 3
ONLY_POSITIVE = 4

algorithm = "EMDD" # "EMDD

DATASET = STEP_LIMIT_EQUALLY_BALANCED


NEGATIVE_BAG_COUNT = 20
POSITIVE_BAG_COUNT = 20

# EMDD.H_SET, EMDD.H_ALL
SEARCH_SET = EMDD.H_SET

# EMDD.EXPONENTIAL
METHOD = EMDD.EXPONENTIAL

# 1, 2, 3, 4
SKIPPING_FACTOR = 3

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

dataset_defs  = {STEP_LIMIT_EQUALLY_BALANCED: "STEPLIMITEQUALLYBALANCED",
                 STEP_LIMIT_ONLY_POSITIVE: "STEPLIMITONLYPOSITIVE",
                 EQUALLY_BALANCED: "EQUALLYBALANCED",
                 ONLY_POSITIVE: "ONLYPOSITIVE"}

print("Dataset : ", dataset_defs[DATASET])
print("Algorithm : ", algorithm)
print("SEARCH :" , SEARCH_SET)
print("METHOD : ", METHOD)
print("SKIP : ", SKIPPING_FACTOR)




if DATASET == STEP_LIMIT_EQUALLY_BALANCED or DATASET == STEP_LIMIT_ONLY_POSITIVE:
    data_version = "ActionNoise(0.9)StepLimit(400)"
elif DATASET == EQUALLY_BALANCED or DATASET == ONLY_POSITIVE:
    data_version = "ActionNoise(0.9)"

included_experiment_count = 0

total_dd_time = 0

total_emdd_time = 0

# Experiment folder
if algorithm == "EMDD":
    experiment_folder = "AccuracyExperimentsFourRooms/"+data_version+"/"+dataset_defs[DATASET]+"/"+algorithm+"/"+METHOD+"/"+SEARCH_SET+"/"+str(SKIPPING_FACTOR)
else:
    experiment_folder = "AccuracyExperimentsFourRooms/"+data_version+"/"+dataset_defs[DATASET]+"/"+algorithm

experiment_folder += "/#"+experiment_date+"#"+experiment_time

if not os.path.exists(experiment_folder):
    create_path = "AccuracyExperimentsFourRooms"
    for i in experiment_folder.split("/")[1:]:
        create_path += "/" + i
        if not os.path.exists(create_path):
            os.mkdir(create_path)

experiment_folder += "/"

run_file_name = "RUN.txt"
run_file = open(experiment_folder+run_file_name, "w")

run_file.write("DATASET:"+dataset_defs[DATASET]+"\n")
run_file.write("ALGORITHM:"+algorithm+"\n")
if algorithm == "EMDD":
    run_file.write("SEARCHSET:"+SEARCH_SET+"\n")
    run_file.write("METHOD:"+METHOD+"\n")


for experiment_id in range(1, 101):# 101):
    # how many experiments are used for experiment

    included_experiment_count += 1

    data_directory = "../MIL/data/FourRoomsQAgentTrajectories/"
    experiment_number = experiment_id

    file_name = "FourRoomsBagExperiment["+str(experiment_number)+"].txt"

    print("File to be opened : ", file_name)
    data_file = open(data_directory + data_version+"/"+file_name, "r");
    positive_bags = []
    negative_bags = []
    negative_bag_count = 0

    for line in data_file:
        parts = line.split(",")
        bag = []
        for i in range(1, len(parts)):
            # print("parts ", int(parts[i]), " - ", int(parts[i]) in eliminated_states)

            if int(parts[i]) in eliminated_states:
                pass
            else:
                bag.append(int(parts[i]))

        if DATASET == STEP_LIMIT_EQUALLY_BALANCED or DATASET == STEP_LIMIT_ONLY_POSITIVE:
            if parts[0] == "1":# len(parts) <= 201:
                positive_bags.append(list(set(bag)))
            else:
                negative_bags.append(list(set(bag)))
        elif DATASET == EQUALLY_BALANCED:
            if negative_bag_count>=POSITIVE_BAG_COUNT:
                positive_bags.append(list(set(bag)))
            else:
                negative_bags.append(list(set(bag)))
                negative_bag_count += 1
        elif DATASET == ONLY_POSITIVE:
            positive_bags.append(list(set(bag)))

    print("Total Positive bag count in experiment : ", len(positive_bags))
    print("Total Negative bag count in experiment : ", len(negative_bags))

    data_file.close()

    # only use first 20 episode data...
    if DATASET == STEP_LIMIT_EQUALLY_BALANCED:
        positive_bags = positive_bags[0:POSITIVE_BAG_COUNT]
        negative_bags = negative_bags[0:NEGATIVE_BAG_COUNT]
    elif DATASET == STEP_LIMIT_ONLY_POSITIVE:
        positive_bags = positive_bags[0:POSITIVE_BAG_COUNT]
        negative_bags = []
    elif DATASET == EQUALLY_BALANCED:
        positive_bags = positive_bags[0:POSITIVE_BAG_COUNT]
        negative_bags = negative_bags[0:NEGATIVE_BAG_COUNT]
    elif DATASET == ONLY_POSITIVE:
        positive_bags = positive_bags[0:POSITIVE_BAG_COUNT]
        negative_bags = []

    print("ALgorithm : ", algorithm)
    print("DATASET : ", dataset_defs[DATASET])
    print("Data Version ", data_version)
    print("positive bag count : ", len(positive_bags))
    print("negative bag count : ", len(negative_bags))

    STATES_TO_TEST = set()
    for Bi in positive_bags:
        for state in Bi:
            STATES_TO_TEST.add(state)

    DD = DiverseDensity(positive_bags, negative_bags, G, distance_metric=DiverseDensity.DISTANCE_METRIC_GRAPH)
    emdd = EMDD(positive_bags, negative_bags, G, STATES_TO_TEST, METHOD, distance_metric=DiverseDensity.DISTANCE_METRIC_GRAPH,
                H_CHECK=SEARCH_SET, SKIPPING_FACTOR=SKIPPING_FACTOR)
    if algorithm == "EMDD":
        print("EMDD working")
        emdd_start_time = timer();
        emdd_result = emdd()
        emdd_end_time = timer();
        total_emdd_time += emdd_end_time - emdd_start_time
        print("EMDD run time : ", emdd_end_time-emdd_start_time, " seconds")
        average_count += emdd.average_loop_count
        subgoal_results.append(emdd_result[0])

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
        subgoal_results.append(max_dd_state)

environment = RLFourRoomsEnvironment.RLFourRoomsEnvironment('v2', is_step_restricted=True, step_limit=500)
pickle.dump(subgoal_results,open(experiment_folder+algorithm+"SELECTEDSTATES.pickle", "wb"))


environment.setEnableSubgoalDisplay(True)

subgoals_dict = {}
for subgoal in set(subgoal_results):
    subgoals_dict[subgoal] = (subgoal_results.count(subgoal)+10)*5
print(subgoals_dict)
environment.setDisplaySubgoal(subgoals_dict)
environment.renderEnvironment()
environment.setEnvironmentImageTitle(data_version+""+dataset_defs[DATASET]+""+algorithm)
environment.renderEnvironment()

environment.saveEnvironmentImage(experiment_folder+data_version+""+dataset_defs[DATASET]+""+algorithm+".png")

print("\n\n\n")

print ("Total run time : ", timer() - start_time, "seconds")
print("Total experiment count : ", included_experiment_count)
print("\n")
print("Algorithm : ", algorithm)
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


ground_truth_for_subgoals = [71,72,74,75,
                             92,93,94,95,96,
                             113, 114, 116, 117,

                             171,172,173,
                             192,193,194,
                                       214,
                             234, 235, 236,
                             255, 256, 257,

                             302,303,305,306,
                             323,324,325,326,327,
                             344,345,347,348,

                             # aroun goal state
                             161,162,163,164,165,
                             182,186,
                             203,207,

                             245,249,
                             266,270,
                             287,288,289,290,291

                             ]

hit_count = 0
for i in subgoal_results:
    if i in ground_truth_for_subgoals:
        hit_count += 1
precision = float(hit_count) / float(len(subgoal_results))
recall = float(hit_count) / float(len(ground_truth_for_subgoals))
try:
    f1 = 2 * float(precision) * float(recall) / (float(precision) + float(recall))
except:
    f1 = 0
print("Precision : ", precision)
run_file.write("Precision : "+ str(precision))
run_file.close()
