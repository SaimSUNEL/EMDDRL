import os
import time

from Environments import RLTwoRoomsEnvironment
from MIL.Methods.DD import DiverseDensity
from MIL.Methods.EMDD import EMDD

import pickle
G = pickle.load(open("MIL/data/TwoRoomsEnvironmentDistanceDict.pck", "rb"))

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

algorithm = "DD" # "EMDD

DATASET = ONLY_POSITIVE


# EMDD.H_SET, EMDD.H_NEIGHBOR, EMDD.H_ALL
SEARCH_SET = EMDD.H_SET

# EMDD.EXPONENTIAL
METHOD = EMDD.LINEAR

# 1, 2, 3, 4
SKIPPING_FACTOR = 3




dataset_defs  = {STEP_LIMIT_EQUALLY_BALANCED: "STEPLIMITEQUALLYBALANCED",
                 STEP_LIMIT_ONLY_POSITIVE: "STEPLIMITONLYPOSITIVE",
                 EQUALLY_BALANCED: "EQUALLYBALANCED",
                 ONLY_POSITIVE: "ONLYPOSITIVE"}

if DATASET == STEP_LIMIT_EQUALLY_BALANCED or DATASET == STEP_LIMIT_ONLY_POSITIVE:
    data_version = "ActionNoise(0.9)StepLimit(200)"
elif DATASET == EQUALLY_BALANCED or DATASET == ONLY_POSITIVE:
    data_version = "ActionNoise(0.9)"



# Experiment folder
if algorithm == "EMDD":
    experiment_folder = "SpeedExperiments/"+data_version+"/"+dataset_defs[DATASET]+"/"+algorithm+"/"+METHOD+"/"+SEARCH_SET+"/"+str(SKIPPING_FACTOR)
else:
    experiment_folder = "SpeedExperiments/"+data_version+"/"+dataset_defs[DATASET]+"/"+algorithm

experiment_folder += "/#2020-8-2#11:6:49"

if not os.path.exists(experiment_folder):
    create_path = "SpeedExperiments"
    for i in experiment_folder.split("/")[1:]:
        create_path += "/" + i
        if not os.path.exists(create_path):
            os.mkdir(create_path)

experiment_folder += "/"



two_rooms_env_v2 = RLTwoRoomsEnvironment.RLTwoRoomsEnvironment('v2', is_step_restricted=True, step_limit=500)

counts = states = pickle.load(open(experiment_folder+algorithm+"SELECTEDSTATES.pickle", "rb"))
elements = set(states)

print(counts)
print(set(counts))
# 94, 115
distance_info = {}
for i in set(counts):
    distance_info[i] = {"count": counts.count(i), "average_distance": float(G[94][i]+G[115][i])/2.0}

two_rooms_env_v2.setEnableSubgoalDisplay(True)

subgoals_dict = {}
for subgoal in set(elements):
    subgoals_dict[subgoal] = (counts.count(subgoal)+10)*5
print(subgoals_dict)
two_rooms_env_v2.setDisplaySubgoal(subgoals_dict)
if algorithm == "EMDD":
    two_rooms_env_v2.setEnvironmentImageTitle(data_version+""+dataset_defs[DATASET]+""+algorithm+SEARCH_SET+METHOD)
else:
    two_rooms_env_v2.setEnvironmentImageTitle(data_version+""+dataset_defs[DATASET]+""+algorithm)
two_rooms_env_v2.renderEnvironment()
for i in distance_info:
    print(i, distance_info[i])

raw_input("")