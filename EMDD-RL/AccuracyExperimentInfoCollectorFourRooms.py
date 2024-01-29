from Environments import RLTwoRoomsEnvironment
from MIL.Methods.DD import DiverseDensity
from MIL.Methods.EMDD import EMDD
import os
from PIL import Image
import cv2
STEP_LIMIT_EQUALLY_BALANCED = 1
EQUALLY_BALANCED = 3
import pickle

G = pickle.load(open("MIL/data/FourRoomsEnvironmentDistanceDict.pck", "rb"))

algorithm = "DDCF" # "EMDD

DATASET = STEP_LIMIT_EQUALLY_BALANCED

NEGATIVE_BAG_COUNT = 5

# EMDD.H_SET, EMDD.H_NEIGHBOR, EMDD.H_ALL
SEARCH_SET = EMDD.H_SET
ALGORITHM_ARRAY = ["DDCF"]# ["EMDD", "DD"]
DATASET_ARRAY = [STEP_LIMIT_EQUALLY_BALANCED]
METHOD_ARRAY = [EMDD.LINEAR, EMDD.EXPONENTIAL]
SEARCH_ARRAY = [EMDD.H_ALL, EMDD.H_SET]
SKIP_ARRAY = [1, 2, 3, 4]
NEGATIVE_BAG_COUNT_ARRAY = [20] # [0, 5, 10, 15, 20]
POSITIVE_BAG_COUNT_ARRAY = [20] # [5, 10, 15, 20]
K_PARAMETER_ARRAY = [2, 4, 6 , 8, 10, 12]
# EMDD.EXPONENTIAL
METHOD = EMDD.EXPONENTIAL

# 1, 2, 3, 4
SKIPPING_FACTOR = 1


dataset_defs  = {STEP_LIMIT_EQUALLY_BALANCED: "STEPLIMITEQUALLYBALANCED"}
# candidate states for subgoals...
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


json = {}

dataset_cell = []
search_cell = []
method_cell = []
skip_cell = []
negative_count_cell = []
positive_count_cell = []
total_emdd_time_cell = []
average_emdd_time_cell = []
average_emdd_loop_cell = []
instance_count_cell = []
precision_cell = []
recall_cell = []
f1_cell = []


dataset_cell2 = []
negative_count_cell2 = []
positive_count_cell2 = []
precision_cell2 = []
recall_cell2 = []
f1_cell2 = []
dd_average_cell =[]
dd_total_cell = []


k_param_cell = []

for algorithm in ALGORITHM_ARRAY:
    if not algorithm in json:
        json[algorithm] = {}

    for DATASET in DATASET_ARRAY:
        if not dataset_defs[DATASET] in json[algorithm]:
            json[algorithm][dataset_defs[DATASET]] =  {}
        if algorithm == "EMDD":
            for METHOD in METHOD_ARRAY:
                if not json[algorithm][dataset_defs[DATASET]].has_key(METHOD):
                    json[algorithm][dataset_defs[DATASET]][METHOD] = {}

                for SEARCH_SET in SEARCH_ARRAY:
                    if not json[algorithm][dataset_defs[DATASET]][METHOD].has_key(SEARCH_SET):
                        json[algorithm][dataset_defs[DATASET]][METHOD][SEARCH_SET] = {}

                    for SKIPPING_FACTOR in SKIP_ARRAY:
                        if not json[algorithm][dataset_defs[DATASET]][METHOD][SEARCH_SET].has_key(str(SKIPPING_FACTOR)):
                            json[algorithm][dataset_defs[DATASET]][METHOD][SEARCH_SET][str(SKIPPING_FACTOR)] = {}

                        for POSITIVE_BAG_COUNT in POSITIVE_BAG_COUNT_ARRAY:
                            if not json[algorithm][dataset_defs[DATASET]][METHOD][SEARCH_SET][str(SKIPPING_FACTOR)].has_key(str(POSITIVE_BAG_COUNT)):
                                json[algorithm][dataset_defs[DATASET]][METHOD][SEARCH_SET][str(SKIPPING_FACTOR)][str(POSITIVE_BAG_COUNT)] = {}
                            for NEGATIVE_BAG_COUNT in NEGATIVE_BAG_COUNT_ARRAY:
                                if not json[algorithm][dataset_defs[DATASET]][METHOD][SEARCH_SET][str(SKIPPING_FACTOR)][str(POSITIVE_BAG_COUNT)].has_key(str(NEGATIVE_BAG_COUNT)):
                                    json[algorithm][dataset_defs[DATASET]][METHOD][SEARCH_SET][str(SKIPPING_FACTOR)][
                                        str(POSITIVE_BAG_COUNT)][str(NEGATIVE_BAG_COUNT)] = {}
                                print("Dataset : ", dataset_defs[DATASET])
                                print("Algorithm : ", algorithm)
                                print("SEARCH :", SEARCH_SET)
                                print("METHOD : ", METHOD)
                                print("SKIP : ", SKIPPING_FACTOR)
                                print("NEGATIVE BAG COUNT", NEGATIVE_BAG_COUNT)
                                if DATASET == STEP_LIMIT_EQUALLY_BALANCED:
                                    data_version = "ActionNoise(0.9)StepLimit(400)"
                                elif DATASET == EQUALLY_BALANCED:
                                    data_version = "ActionNoise(0.9)"

                                included_experiment_count = 0

                                total_dd_time = 0

                                total_emdd_time = 0

                                # Experiment folder
                                if algorithm == "EMDD":
                                    experiment_folder = "AccuracyExperimentsFourRooms/" + data_version + "/" + dataset_defs[
                                        DATASET] + "/" + algorithm + "/" + METHOD + "/" + SEARCH_SET + "/" + str(
                                        SKIPPING_FACTOR)
                                else:
                                    experiment_folder = "AccuracyExperimentsFourRooms/" + data_version + "/" + dataset_defs[
                                        DATASET] + "/" + algorithm
                                experiment_folder += "/#"+str(POSITIVE_BAG_COUNT)+"Positive" + "#" + str(NEGATIVE_BAG_COUNT) + "Negative"

                                experiment_folder += "/"



                                image_file = experiment_folder+data_version+dataset_defs[DATASET]+algorithm+SEARCH_SET+METHOD+"#"+str(POSITIVE_BAG_COUNT)+"Positive#"\
                                             + str(NEGATIVE_BAG_COUNT)+"Negative.png"

                                img = Image.open(image_file)

                                cropped = img.crop((0, 0, 700, 700))
                                cropped.save(
                                    image_file)

                                # os.rename(image_file, image_file+".tga")
                                # img = Image.open(image_file+".tga")
                                # img.save(image_file+".png")
                                dd_average_time = 0.0

                                experiment_f = experiment_folder
                                run_file = open(experiment_f + "RUN.txt")
                                for line in run_file:
                                    key, value = line.split(":")
                                    json[algorithm][dataset_defs[DATASET]][METHOD][SEARCH_SET][str(SKIPPING_FACTOR)][
                                        str(POSITIVE_BAG_COUNT)][str(NEGATIVE_BAG_COUNT)][key] = value

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

                                counts = states = pickle.load(
                                    open(experiment_folder + algorithm + "SELECTEDSTATES.pickle", "rb"))
                                elements = set(states)
                                # 94, 115
                                distance_info = {}
                                for i in set(counts):
                                    distance_info[i] = {"count": counts.count(i),
                                                        "average_distance": float(G[5][i] + G[6][i]) / 2.0}

                                hit_count = 0
                                for i in states:
                                    if i in ground_truth_for_subgoals:
                                        hit_count += 1
                                precision = float(hit_count) / float(len(states))
                                recall = float(hit_count) / float(len(ground_truth_for_subgoals))
                                f1 = 2 * float(precision) * float(recall) / (float(precision) + float(recall))

                                precision_cell.append(precision)
                                recall_cell.append(recall)
                                f1_cell.append(f1)
                                instance_count_cell.append(len(elements))
                                dataset_cell.append(dataset_defs[DATASET])
                                search_cell.append(SEARCH_SET)
                                method_cell.append(METHOD)
                                positive_count_cell.append(POSITIVE_BAG_COUNT)
                                negative_count_cell.append(NEGATIVE_BAG_COUNT)
                                json[algorithm][dataset_defs[DATASET]][METHOD][SEARCH_SET][str(SKIPPING_FACTOR)][
                                    str(POSITIVE_BAG_COUNT)][str(NEGATIVE_BAG_COUNT)]["Precision"] = precision

                                skip_cell.append(SKIPPING_FACTOR)
                                total_emdd_time_cell.append(emdd_total_time)
                                average_emdd_time_cell.append(emdd_average_time)
                                average_emdd_loop_cell.append(emdd_loop_average)
            pass
        elif algorithm == "DD":


                for POSITIVE_BAG_COUNT in POSITIVE_BAG_COUNT_ARRAY:
                    if not json[algorithm][dataset_defs[DATASET]].has_key(str(POSITIVE_BAG_COUNT)):
                        json[algorithm][dataset_defs[DATASET]][str(POSITIVE_BAG_COUNT)] = {}
                    for NEGATIVE_BAG_COUNT in NEGATIVE_BAG_COUNT_ARRAY:
                        if not json[algorithm][dataset_defs[DATASET]][str(POSITIVE_BAG_COUNT)].has_key(str(NEGATIVE_BAG_COUNT)):
                            json[algorithm][dataset_defs[DATASET]][str(POSITIVE_BAG_COUNT)][str(NEGATIVE_BAG_COUNT)] = {}


                        print("Dataset : ", dataset_defs[DATASET])
                        print("Algorithm : ", algorithm)
                        print("NEGATIVE BAG COUNT", NEGATIVE_BAG_COUNT)
                        if DATASET == STEP_LIMIT_EQUALLY_BALANCED:
                            data_version = "ActionNoise(0.9)StepLimit(400)"
                        elif DATASET == EQUALLY_BALANCED:
                            data_version = "ActionNoise(0.9)"

                        # Experiment folder
                        if algorithm == "EMDD":
                            experiment_folder = "AccuracyExperimentsFourRooms/" + data_version + "/" + dataset_defs[
                                DATASET] + "/" + algorithm + "/" + METHOD + "/" + SEARCH_SET + "/" + str(
                                SKIPPING_FACTOR)
                        else:
                            experiment_folder = "AccuracyExperimentsFourRooms/" + data_version + "/" + dataset_defs[
                                DATASET] + "/" + algorithm
                        t_folder = experiment_folder + "/%23"+str(POSITIVE_BAG_COUNT)+"Positive" + "%23" + str(NEGATIVE_BAG_COUNT) + "Negative"
                        experiment_folder += "/#"+str(POSITIVE_BAG_COUNT)+"Positive" + "#" + str(NEGATIVE_BAG_COUNT) + "Negative"

                        experiment_folder += "/"
                        t_folder += "/"

                        experiment_f = experiment_folder
                        run_file = open(experiment_f + "RUN.txt")
                        for line in run_file:
                            key, value = line.split(":")
                            json[algorithm][dataset_defs[DATASET]][str(POSITIVE_BAG_COUNT)][str(NEGATIVE_BAG_COUNT)][key] = value
                            if line.__contains__("Total DD run time"):
                                parts = line.split(":")
                                dd_total_time = float(parts[1])
                            elif line.__contains__("Average DD run time"):
                                parts = line.split(":")
                                dd_average_time = float(parts[1])
                        run_file.close()

                        # os.rename(image_file, image_file+".tga")
                        # img = Image.open(image_file)
                        # img.save(image_file+".png")

                        image_file = experiment_folder+data_version+dataset_defs[DATASET] \
                        +algorithm+"#"+str(POSITIVE_BAG_COUNT)+"Positive#"+str(NEGATIVE_BAG_COUNT) \
                        + "Negative.png"

                        img = Image.open(image_file)

                        cropped = img.crop((0, 0, 700, 700))
                        cropped.save(
                            image_file)


                        counts = states = pickle.load(
                            open(experiment_folder + algorithm + "SELECTEDSTATES.pickle", "rb"))
                        elements = set(states)
                        # 94, 115
                        distance_info = {}
                        for i in set(counts):
                            distance_info[i] = {"count": counts.count(i),
                                                "average_distance": float(G[5][i] + G[6][i]) / 2.0}

                        hit_count = 0
                        for i in states:
                            if i in ground_truth_for_subgoals:
                                hit_count += 1
                        precision = float(hit_count) / float(len(states))
                        recall = float(hit_count) / float(len(ground_truth_for_subgoals))
                        f1 = 2 * float(precision) * float(recall) / (float(precision) + float(recall))

                        precision_cell2.append(precision)
                        recall_cell2.append(recall)
                        f1_cell2.append(f1)
                        json[algorithm][dataset_defs[DATASET]][str(POSITIVE_BAG_COUNT)][str(NEGATIVE_BAG_COUNT)][
                            "Precision"] = precision

                        dataset_cell2.append(dataset_defs[DATASET])

                        positive_count_cell2.append(POSITIVE_BAG_COUNT)
                        negative_count_cell2.append(NEGATIVE_BAG_COUNT)

                        dd_total_cell.append(dd_total_time)
                        dd_average_cell.append(dd_average_time)

        elif algorithm == "DDCF":

                for POSITIVE_BAG_COUNT in POSITIVE_BAG_COUNT_ARRAY:
                    if not str(POSITIVE_BAG_COUNT) in  json[algorithm][dataset_defs[DATASET]]:
                        json[algorithm][dataset_defs[DATASET]][str(POSITIVE_BAG_COUNT)] = {}
                    for NEGATIVE_BAG_COUNT in NEGATIVE_BAG_COUNT_ARRAY:
                        if not str(NEGATIVE_BAG_COUNT) in json[algorithm][dataset_defs[DATASET]][str(POSITIVE_BAG_COUNT)]:
                            json[algorithm][dataset_defs[DATASET]][str(POSITIVE_BAG_COUNT)][str(NEGATIVE_BAG_COUNT)] = {}

                        for k_param in K_PARAMETER_ARRAY:
                            print("Dataset : ", dataset_defs[DATASET])
                            print("Algorithm : ", algorithm)
                            print("NEGATIVE BAG COUNT", NEGATIVE_BAG_COUNT)
                            if DATASET == STEP_LIMIT_EQUALLY_BALANCED:
                                data_version = "ActionNoise(0.9)StepLimit(400)"
                            elif DATASET == EQUALLY_BALANCED:
                                data_version = "ActionNoise(0.9)"

                            experiment_folder = "AccuracyExperimentsFourRooms/" + data_version + "/" + dataset_defs[
                                    DATASET] + "/" + algorithm + "/K("+str(k_param)+")/"
                            t_folder = experiment_folder + "/%23"+str(POSITIVE_BAG_COUNT)+"Positive" + "%23" + str(NEGATIVE_BAG_COUNT) + "Negative"
                            experiment_folder += "/#"+str(POSITIVE_BAG_COUNT)+"Positive" + "#" + str(NEGATIVE_BAG_COUNT) + "Negative"

                            experiment_folder += "/"
                            t_folder += "/"

                            experiment_f = experiment_folder
                            run_file = open(experiment_f + "RUN.txt")
                            for line in run_file:
                                key, value = line.split(":")
                                json[algorithm][dataset_defs[DATASET]][str(POSITIVE_BAG_COUNT)][str(NEGATIVE_BAG_COUNT)][key] = value
                                if line.__contains__("Total DDCF run time"):
                                    parts = line.split(":")
                                    dd_total_time = float(parts[1])
                                elif line.__contains__("Average DDCF run time"):
                                    parts = line.split(":")
                                    dd_average_time = float(parts[1])

                            run_file.close()

                            # os.rename(image_file, image_file+".tga")
                            # img = Image.open(image_file)
                            # img.save(image_file+".png")



                            counts = states = pickle.load(
                                open(experiment_folder + algorithm + "SELECTEDSTATES.pickle", "rb"))
                            elements = set(states)
                            print("Counts : ", counts)
                            # 94, 115
                            distance_info = {}
                            for i in set(counts):
                                distance_info[i] = {"count": counts.count(i),
                                                    "average_distance": float(G[5][i] + G[6][i]) / 2.0}
                            hit_count = 0
                            for i in states:
                                if i in ground_truth_for_subgoals:
                                    hit_count += 1

                            print("States : ", states)
                            print("Ground truth : ", ground_truth_for_subgoals)

                            precision = float(hit_count) / float(len(states))
                            recall = float(hit_count) / float(len(ground_truth_for_subgoals))
                            if -0.00000001 < precision < 0.0000000001 and -0.00000001 < recall < 0.0000000001:
                                pass
                                f1 = 0
                            else :
                                f1 = 2 * float(precision) * float(recall) / (float(precision) + float(recall))
                            json[algorithm][dataset_defs[DATASET]][str(POSITIVE_BAG_COUNT)][str(NEGATIVE_BAG_COUNT)][
                                "Precision"] = precision
                            precision_cell2.append(precision)
                            recall_cell2.append(recall)
                            f1_cell2.append(f1)
                            k_param_cell.append(k_param)
                            dataset_cell2.append(dataset_defs[DATASET])

                            positive_count_cell2.append(POSITIVE_BAG_COUNT)
                            negative_count_cell2.append(NEGATIVE_BAG_COUNT)

                            dd_total_cell.append(dd_total_time)
                            dd_average_cell.append(dd_average_time)


import json as js

with open('AccuracyExperimentVisualizationFourRooms/AccuracyExperiment.json', 'w') as fp:
    js.dump(json, fp)


import pandas as pd

EXCEL_FILE_NAME = "FourRoomsAccuracyExperimentEMDDResult.xlsx"
if "EMMD" in ALGORITHM_ARRAY:
    try:
        df = pd.DataFrame({'Data Set': dataset_cell,
                           'Search Set': search_cell,
                           "Method": method_cell,
                           "Skipping Factor": skip_cell,
                           "Total EMDD Run Time": total_emdd_time_cell,
                            "Average EMDD Run Time": average_emdd_time_cell,
                            "Average Loop": average_emdd_loop_cell,
                           "Positive": positive_count_cell,
                           "Negative": negative_count_cell,
                           "Selected Instance Count": instance_count_cell,
                           "Precision": precision_cell,
                           "Recall": recall_cell,
                           "F1": f1_cell})
    except Exception as err:
        print("Error :", err)
        exit()
    # name the result excel file as Result
    result_file = pd.ExcelWriter(EXCEL_FILE_NAME, engine='xlsxwriter')

    # embed data frame to excel file...
    df.to_excel(result_file, sheet_name='Sheet1', index=False)
    result_file.save()



import pandas as pd
if "DD" in ALGORITHM_ARRAY:

    EXCEL_FILE_NAME = "FourRoomsAccuracyExperimentDDResult.xlsx"
    try:
        df = pd.DataFrame({'Data Set': dataset_cell2,
                           "Total DD Run Time": dd_total_cell,
                            "Average DD Run Time": dd_average_cell,
                           "Positive": positive_count_cell2,
                           "Negative": negative_count_cell2,
                           "Precision": precision_cell2,
                           "Recall": recall_cell2,
                           "F1": f1_cell2})
    except Exception as err:
        print("Error :", err)
        exit()
    # name the result excel file as Result
    result_file = pd.ExcelWriter(EXCEL_FILE_NAME, engine='xlsxwriter')

    # embed data frame to excel file...
    df.to_excel(result_file, sheet_name='Sheet1', index=False)
    result_file.save()

import pandas as pd

if "DDCF" in ALGORITHM_ARRAY:

    EXCEL_FILE_NAME = "FourRoomsAccuracyExperimentDDCFResult.xlsx"
    try:
        df = pd.DataFrame({'Data Set': dataset_cell2,
                           "Total DD Run Time": dd_total_cell,
                           "Average DD Run Time": dd_average_cell,
                           "Positive": positive_count_cell2,
                           "Negative": negative_count_cell2,
                           "K": k_param_cell,
                           "Precision": precision_cell2,
                           "Recall": recall_cell2,
                           "F1": f1_cell2})
    except Exception as err:
        print("Error :", err)
        exit()
    # name the result excel file as Result
    result_file = pd.ExcelWriter(EXCEL_FILE_NAME, engine='xlsxwriter')

    # embed data frame to excel file...
    df.to_excel(result_file, sheet_name='Sheet1', index=False)
    result_file.save()
print("Okay...")
