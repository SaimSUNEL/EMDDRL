import os
import time

from Environments import RLTwoRoomsEnvironment
from MIL.Methods.DD import DiverseDensity
from MIL.Methods.EMDD import EMDD
import sys

import pickle
G = pickle.load(open("MIL/data/TwoRoomsEnvironmentDistanceDict.pck", "rb"))

emdd_results = []
dd_results = []
eliminated_states = [188, 187, 208, 207, 186, 165, 166, 167, 206, 186, 164, 143, 144, 145, 146, 205, 184, 185,
                     163, 142, 143, 144, 145, 146]


STEP_LIMIT_EQUALLY_BALANCED = 1
STEP_LIMIT_ONLY_POSITIVE = 2
EQUALLY_BALANCED = 3
ONLY_POSITIVE = 4

algorithm = "DD"

DATASET = STEP_LIMIT_ONLY_POSITIVE

dataset_defs  = {STEP_LIMIT_EQUALLY_BALANCED: "STEPLIMITEQUALLYBALANCED",
                 STEP_LIMIT_ONLY_POSITIVE: "STEPLIMITONLYPOSITIVE",
                 EQUALLY_BALANCED: "EQUALLYBALANCED",
                 ONLY_POSITIVE: "ONLYPOSITIVE"}



if DATASET == STEP_LIMIT_EQUALLY_BALANCED or DATASET == STEP_LIMIT_ONLY_POSITIVE:
    data_version = "ActionNoise(0.9)StepLimit(200)"
elif DATASET == EQUALLY_BALANCED or DATASET == ONLY_POSITIVE:
    data_version = "ActionNoise(0.9)"

included_experiment_count = 0

dd_value_dict = {}


for experiment_id in range(1, 101):
    # how many experiments are used for experiment

    included_experiment_count += 1

    data_directory = "MIL/data/TwoRoomsQAgentTrajectories/"
    experiment_number = experiment_id

    file_name = "TwoRoomsBagExperiment["+str(experiment_number)+"].txt"

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
            if negative_bag_count>=20:
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
        positive_bags = positive_bags[0:20]
        negative_bags = negative_bags[0:20]
    elif DATASET == STEP_LIMIT_ONLY_POSITIVE:
        positive_bags = positive_bags[0:20]
        negative_bags = []
    elif DATASET == EQUALLY_BALANCED:
        positive_bags = positive_bags[0:20]
        negative_bags = negative_bags[0:20]
    elif DATASET == ONLY_POSITIVE:
        positive_bags = positive_bags[0:20]
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


    # for DD calculation...
    if algorithm == "DD":
        print("DD is working")
        max_value = -1*float("inf")
        max_dd_state = 0
        all_instances = set()
        for b in positive_bags:
             for instan in b:
                 all_instances.add(instan)

        dd_start_time = time.clock()
        for i in all_instances:
                if i in eliminated_states:
                    continue
                dd_value = DD(i)
                if not dd_value_dict.has_key(i):
                    dd_value_dict[i] = {"val": dd_value, "count": 1}
                else:
                    dd_value_dict[i]["val"] += dd_value
                    dd_value_dict[i]["count"] += 1

        dd_end_time = time.clock()
        print("DD run time : ", dd_end_time - dd_start_time, " seconds")

average_dd_values = {}

for k in dd_value_dict:
    value = dd_value_dict[k]["val"]
    count = dd_value_dict[k]["count"]
    average_dd_values[k] = float(value)/100.0# float(included_experiment_count)


min_dd_value = min(average_dd_values.values())



two_rooms_env_v2 = RLTwoRoomsEnvironment.RLTwoRoomsEnvironment('v2', is_step_restricted=True, step_limit=500)

two_rooms_env_v2.setEnableSubgoalDisplay(True)

subgoals_dict = {}
for subgoal in average_dd_values:
    subgoals_dict[subgoal] = (average_dd_values[subgoal]/abs(min_dd_value))*255.0+255

print(subgoals_dict)
# print(subgoals_dict)
two_rooms_env_v2.setDisplaySubgoal(subgoals_dict)
two_rooms_env_v2.renderEnvironment()

two_rooms_env_v2.setEnvironmentImageTitle(data_version+""+dataset_defs[DATASET]+""+algorithm)

two_rooms_env_v2.renderEnvironment()

two_rooms_env_v2.saveEnvironmentImage("LogDDMapImages/"+data_version+""+dataset_defs[DATASET]+""+algorithm+".png")

raw_input("")