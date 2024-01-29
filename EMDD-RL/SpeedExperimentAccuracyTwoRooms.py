# Here we measure the precision and recall of yielded result of each configuration
# F1 score is calcualted as well in order to be able to compare configuration accuracies


# -*- coding: utf-8 -*-

import os
import time

class EMDD:
    DISTANCE_METRIC_STANDARDIZATION = 1
    DISTANCE_METRIC_GRAPH = 2
    DISTANCE_METRIC_NONE = 3
    LINEAR = "LINEAR"
    DD_MODEL = "DDMODEL"
    EXPONENTIAL = "EXPONENTIAL"
    M_MODEL = LINEAR

    # on maximization step which states will be checked for maximum h
    # all positive instances
    H_ALL = "H_ALL"
    # or only h's neightbor hood.
    H_NEIGHBOR = "H_NEIGHBOR"
    H_SET = "H_SET"


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
dataset_defs  = {STEP_LIMIT_EQUALLY_BALANCED: "STEPLIMITEQUALLYBALANCED",
                                 STEP_LIMIT_ONLY_POSITIVE: "STEPLIMITONLYPOSITIVE",
                                 EQUALLY_BALANCED: "EQUALLYBALANCED",
                                 ONLY_POSITIVE: "ONLYPOSITIVE"}

dataset_array = [STEP_LIMIT_EQUALLY_BALANCED, STEP_LIMIT_ONLY_POSITIVE, EQUALLY_BALANCED, ONLY_POSITIVE]

algorithm = "EMDD" # "EMDD

# EMDD.H_SET, EMDD.H_NEIGHBOR, EMDD.H_ALL

search_set_array = [EMDD.H_SET, EMDD.H_ALL, EMDD.H_NEIGHBOR]

# EMDD.EXPONENTIAL
method_array = [EMDD.LINEAR, EMDD.EXPONENTIAL]

# 1, 2, 3, 4
skipping_factor_array = [1, 2,3,4]



dataset_cell = []
search_cell = []
method_cell = []
skip_cell = []
total_emdd_time_cell = []
average_emdd_time_cell = []
average_emdd_loop_cell = []
date_cell = []
instance_count_cell = []
distance_cell = []



dataset_cell2 = []
search_cell2 = []
method_cell2 = []
skip_cell2 = []
total_emdd_time_cell2 = []
average_emdd_time_cell2 = []
average_emdd_loop_cell2 = []
date_cell2 = []
instance_count_cell2 = []
distance_cell2 = []

json = {}


for DATASET in dataset_array:
    if not json.has_key(dataset_defs[DATASET]):
        json[dataset_defs[DATASET]] = {}

    for SEARCH_SET in search_set_array:
        if not json[dataset_defs[DATASET]].has_key(SEARCH_SET):
            json[dataset_defs[DATASET]][SEARCH_SET] = {}


        for METHOD in method_array:
            if not json[dataset_defs[DATASET]][SEARCH_SET].has_key(METHOD):
                json[dataset_defs[DATASET]][SEARCH_SET][METHOD] = {}
            for SKIPPING_FACTOR in skipping_factor_array:

                if not json[dataset_defs[DATASET]][SEARCH_SET][METHOD].has_key(str(SKIPPING_FACTOR)):
                    json[dataset_defs[DATASET]][SEARCH_SET][METHOD][str(SKIPPING_FACTOR)] = {}

                if DATASET == STEP_LIMIT_EQUALLY_BALANCED or DATASET == STEP_LIMIT_ONLY_POSITIVE:
                    data_version = "ActionNoise(0.9)StepLimit(200)"
                elif DATASET == EQUALLY_BALANCED or DATASET == ONLY_POSITIVE:
                    data_version = "ActionNoise(0.9)"
           # Experiment folder
                if algorithm == "EMDD":
                    experiment_folder = "SpeedExperiments/"+data_version+"/"+dataset_defs[DATASET]+"/"+algorithm+"/"+METHOD+"/"+SEARCH_SET+"/"+str(SKIPPING_FACTOR)

                total_emdd_total_time = 0.0
                total_emdd_average_time = 0.0
                total_emdd_loop_average = 0.0
                date_count = 0
                for date in os.listdir(experiment_folder):
                    if date.__contains__(".png"):
                        continue
                    date_count += 1


                    emdd_total_time = 0.0
                    emdd_average_time = 0.0
                    emdd_loop_average = 0.0
                    experiment_f = experiment_folder+ "/"+date+"/"
                    run_file = open(experiment_f+"RUN.txt")
                    for line in run_file:
                        if line.__contains__("Total EMDD Run Time"):
                            parts = line.split(":")
                            emdd_total_time = float(parts[1])
                        elif line.__contains__("Average EMDD runtime"):
                            parts = line.split(":")
                            emdd_average_time = float(parts[1])
                        elif line.__contains__("EMDD Average loop"):
                            parts = line.split(":")
                            emdd_loop_average = float(parts[1])


                    run_file.close()
                    total_emdd_total_time += emdd_total_time;
                    total_emdd_average_time += emdd_average_time;
                    total_emdd_loop_average += emdd_loop_average

                    counts = states = pickle.load(open(experiment_f+algorithm+"SELECTEDSTATES.pickle", "rb"))
                    elements = set(states)
                    # 94, 115
                    distance_info = {}
                    for i in set(counts):
                        distance_info[i] = {"count": counts.count(i),
                                            "average_distance": float(G[94][i] + G[115][i]) / 2.0}

                    instance_count_cell.append(len(elements))
                    metric = 0.0
                    for i in distance_info:
                        metric += distance_info[i]["average_distance"]
                    metric /= len(distance_info)
                    distance_cell.append(metric)


                    date_cell.append(date)
                    dataset_cell.append(dataset_defs[DATASET])
                    search_cell.append(SEARCH_SET)
                    method_cell.append(METHOD)
                    skip_cell.append(SKIPPING_FACTOR)
                    total_emdd_time_cell.append(emdd_total_time)
                    average_emdd_time_cell.append(emdd_average_time)
                    average_emdd_loop_cell.append(emdd_loop_average)
                if not SEARCH_SET.__contains__("NEIGH"):
                    json[dataset_defs[DATASET]][SEARCH_SET][METHOD][str(SKIPPING_FACTOR)]["emdd loop"] = str(float(total_emdd_loop_average)/float(date_count))
                    json[dataset_defs[DATASET]][SEARCH_SET][METHOD][str(SKIPPING_FACTOR)]["emdd average run"] = str(float(total_emdd_average_time)/float(date_count))

                    latex_table += """
                    %s & %s & %s & %s & %.4f\\\\
                    """ % (METHOD[0:3], SEARCH_SET[2:], str(SKIPPING_FACTOR), str(float(total_emdd_loop_average)/float(date_count)),
                           float(total_emdd_average_time)/float(date_count))
                dataset_cell2.append(dataset_defs[DATASET])
                search_cell2.append(SEARCH_SET)
                method_cell2.append(METHOD)
                skip_cell2.append(SKIPPING_FACTOR)
                total_emdd_time_cell2.append(float(total_emdd_total_time)/float(date_count))
                average_emdd_time_cell2.append(float(total_emdd_average_time)/float(date_count))
                average_emdd_loop_cell2.append(float(total_emdd_loop_average)/float(date_count))




        date_cell.append("")
        dataset_cell.append("")
        search_cell.append("")
        method_cell.append("")
        skip_cell.append("")
        total_emdd_time_cell.append("")
        average_emdd_time_cell.append("")
        average_emdd_loop_cell.append("")
        distance_cell.append("")
        instance_count_cell.append("")

    latex_table += """
     \\hline
    \\end{tabular}
    """
    latex_file.write(latex_table+"\n\n\n")

    date_cell.append("");date_cell.append("");date_cell.append("")
    dataset_cell.append("");dataset_cell.append("");dataset_cell.append("")
    search_cell.append("");search_cell.append("");search_cell.append("")
    method_cell.append("");method_cell.append("");method_cell.append("")
    skip_cell.append("");skip_cell.append("");skip_cell.append("")
    total_emdd_time_cell.append("");total_emdd_time_cell.append("");total_emdd_time_cell.append("")
    average_emdd_time_cell.append("");average_emdd_time_cell.append("");average_emdd_time_cell.append("")
    average_emdd_loop_cell.append("");average_emdd_loop_cell.append("");average_emdd_loop_cell.append("")
    instance_count_cell.append("");instance_count_cell.append("");instance_count_cell.append("")
    distance_cell.append(""); distance_cell.append(""); distance_cell.append("")

latex_file.close()

date_cell.append("");
date_cell.append("");
date_cell.append("")
dataset_cell.append("");
dataset_cell.append("");
dataset_cell.append("")
search_cell.append("");
search_cell.append("");
search_cell.append("")
method_cell.append("");
method_cell.append("");
method_cell.append("")
skip_cell.append("");
skip_cell.append("");
skip_cell.append("")
total_emdd_time_cell.append("");
total_emdd_time_cell.append("");
total_emdd_time_cell.append("")
average_emdd_time_cell.append("");
average_emdd_time_cell.append("");
average_emdd_time_cell.append("")
average_emdd_loop_cell.append("");
average_emdd_loop_cell.append("");
average_emdd_loop_cell.append("")
instance_count_cell.append("");
instance_count_cell.append("");
instance_count_cell.append("")
distance_cell.append("");
distance_cell.append("");
distance_cell.append("")

import pandas as pd

EXCEL_FILE_NAME = "SPEEDExperimentEMDDResult.xlsx"
try:
    df = pd.DataFrame({'Data Set': dataset_cell,
                       'Search Set': search_cell,
                       "Method": method_cell,
                       "Skipping Factor": skip_cell,
                       "DateTime": date_cell,
                       "Total EMDD Run Time": total_emdd_time_cell,
                        "Average EMDD Run Time": average_emdd_time_cell,
                        "Average Loop": average_emdd_loop_cell,
                       "Selected Instance Count": instance_count_cell,
                       "Distance": distance_cell})
except Exception as err:

    exit()
# name the result excel file as Result
result_file = pd.ExcelWriter(EXCEL_FILE_NAME, engine='xlsxwriter')

# embed data frame to excel file...
df.to_excel(result_file, sheet_name='Sheet1', index=False)
result_file.save()


EXCEL_FILE_NAME2 = "SPEEDExperimentEMDDResultAveraged.xlsx"
try:
    df2 = pd.DataFrame({'Data Set': dataset_cell2,
                       'Search Set': search_cell2,
                       "Method": method_cell2,
                       "Skipping Factor": skip_cell2,
                       "Total EMDD Run Time": total_emdd_time_cell2,
                        "Average EMDD Run Time": average_emdd_time_cell2,
                        "Average Loop": average_emdd_loop_cell2})
except Exception as err:

    exit()
# name the result excel file as Result
result_file = pd.ExcelWriter(EXCEL_FILE_NAME2, engine='xlsxwriter')

# embed data frame to excel file...
df2.to_excel(result_file, sheet_name='Sheet1', index=False)
result_file.save()



import json as js

with open('SpeedExperimentVisualization/SpeedExperiment.json', 'w') as fp:
    js.dump(json, fp)