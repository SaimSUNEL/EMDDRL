import os
import time

import pickle
G = pickle.load(open("MIL/data/TwoRooms1XDistanceDict.pck", "rb"))
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

algorithm = "DD" # "EMDD
# candidate states for subgoals...
# candidate states for subgoals...
ground_truth_for_subgoals = [106,107,109,110,
                             137,138,139,140,141,
                             168,169,170,171,172,
                             199,200,202,203]


dataset_cell = []
total_dd_time_cell = []
average_dd_time_cell = []
date_cell = []
instance_count_cell = []
distance_cell = []
precision_cell = []
recall_cell = []
f1_cell = []

dataset_cell2 = []
total_dd_time_cell2 = []
average_dd_time_cell2 = []
date_cell2 = []
instance_count_cell2 = []
distance_cell2 = []
precision_cell2 = []
recall_cell2 = []
f1_cell2 = []

json = {}

latex_file = open("DDTwoRooms1XSpeedAverageResults.txt", "w")

latex_table = """ \\ begin{tabular}{ |p{0.8cm}|p{1.5cm}|  }
                           \\hline
                           \multicolumn{2}{|c|}{DD Algorithm} \\\\
                           \\hline
                           Dataset & Run Time \\\\
                           \\hline
                          """




for DATASET in dataset_array:

                if not json.has_key(dataset_defs[DATASET]):
                   json[dataset_defs[DATASET]] = {}


                if DATASET == STEP_LIMIT_EQUALLY_BALANCED or DATASET == STEP_LIMIT_ONLY_POSITIVE:
                    data_version = "ActionNoise(0.9)StepLimit(300)"
                elif DATASET == EQUALLY_BALANCED or DATASET == ONLY_POSITIVE:
                    data_version = "ActionNoise(0.9)"
           # Experiment folder
                if algorithm == "DD":
                    experiment_folder = "SpeedExperimentsTwoRooms1X/"+data_version+"/"+dataset_defs[DATASET]+"/"+algorithm

                total_dd_total_time = 0.0
                total_dd_average_time = 0.0
                date_count = 0

                for date in os.listdir(experiment_folder):
                    if date.__contains__(".png"):
                        continue
                    date_count += 1
                    dd_total_time = 0.0
                    dd_average_time = 0.0
                    experiment_f = experiment_folder+ "/"+date+"/"
                    run_file = open(experiment_f+"RUN.txt")
                    for line in run_file:
                        if line.__contains__("Total DD run time"):
                            parts = line.split(":")
                            dd_total_time = float(parts[1])
                        elif line.__contains__("Average DD run time"):
                            parts = line.split(":")
                            dd_average_time = float(parts[1])

                    total_dd_total_time += dd_total_time;
                    total_dd_average_time += dd_average_time;
                    run_file.close()

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

                    hit_count = 0
                    for i in states:
                        if i in ground_truth_for_subgoals:
                            hit_count += 1
                    precision = float(hit_count) / float(len(states))
                    recall = float(hit_count) / float(len(ground_truth_for_subgoals))
                    f1 = 2 * float(precision) * float(recall) / (float(precision) + float(recall))

                    date_cell.append(date)
                    dataset_cell.append(dataset_defs[DATASET])

                    total_dd_time_cell.append(dd_total_time)
                    average_dd_time_cell.append(dd_average_time)

                    precision_cell.append(precision)
                    recall_cell.append(recall)
                    f1_cell.append(f1)



                json[dataset_defs[DATASET]]["precision"] = precision
                json[dataset_defs[DATASET]]["recall"] = recall
                json[dataset_defs[DATASET]]["f1"] = f1

                json[dataset_defs[DATASET]]["dd average run"] = str(float(total_dd_average_time)/float(date_count))
                latex_table += """
                                %s & %.4f \\\\
                               """ % (dataset_defs[DATASET], float(total_dd_average_time)/float(date_count))


                dataset_cell2.append(dataset_defs[DATASET])

                total_dd_time_cell2.append(float(total_dd_total_time)/float(date_count))
                average_dd_time_cell2.append(float(total_dd_average_time)/float(date_count))

                precision_cell2.append(precision)
                recall_cell2.append(recall)
                f1_cell2.append(f1)
latex_table += """
     \\hline
    \\end{tabular}
    """
latex_file.write(latex_table + "\n\n\n")
latex_file.close()

import json as js

# with open('SpeedExperimentVisualization/SpeedExperimentDD.json', 'w') as fp:
#     js.dump(json, fp)

date_cell.append("");

dataset_cell.append("");


total_dd_time_cell.append("");

average_dd_time_cell.append("");
distance_cell.append("")
instance_count_cell.append("")
precision_cell.append("")
recall_cell.append("")
f1_cell.append("")



import pandas as pd
EXCEL_FILE_NAME = "SPEEDExperimentDDTwoRooms1XResult.xlsx"
try:
    df = pd.DataFrame({'Data Set': dataset_cell,
                       "DateTime": date_cell,
                       "Total EMDD Run Time": total_dd_time_cell,
                        "Average EMDD Run Time": average_dd_time_cell,
                       "Selected Instance Count": instance_count_cell,
                       "Precision": precision_cell,
                       "Recall": recall_cell,
                       "F1": f1_cell
                        })
except Exception as err:
    print("Error", err)
    exit()
# name the result excel file as Result
result_file = pd.ExcelWriter(EXCEL_FILE_NAME, engine='xlsxwriter')

# embed data frame to excel file...
df.to_excel(result_file, sheet_name='Sheet1', index=False)
result_file.save()



EXCEL_FILE_NAME2 = "SPEEDExperimentDDTwoRooms1XResult.xlsx"
try:
    df2 = pd.DataFrame({'Data Set': dataset_cell2,
                       "Total EMDD Run Time": total_dd_time_cell2,
                        "Average EMDD Run Time": average_dd_time_cell2,
                        "Precision": precision_cell2,
                        "Recall": recall_cell2,
                        "F1": f1_cell2
                        })
except Exception as err:
    print("Error", err)
    exit()
# name the result excel file as Result
result_file = pd.ExcelWriter(EXCEL_FILE_NAME2, engine='xlsxwriter')

# embed data frame to excel file...
df2.to_excel(result_file, sheet_name='Sheet1', index=False)
result_file.save()

print("Okay....")