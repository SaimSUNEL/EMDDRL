# for each positive and negative bag count best EMDD-RL setting (the most accurate and the fastest) and the corresponding DD are compared...

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import difflib



emdd_file_dict = {"TwoRooms": "AccuracyExperimentEMDDResult.xlsx",
                "FourRooms" : "FourRoomsAccuracyExperimentEMDDResult.xlsx"}


data_convert = {"STEPLIMITEQUALLYBALANCED": "STEPBALANCED",
                "STEPLIMITONLYPOSITIVE": "STEPPOSITIVE",
                "ONLYPOSITIVE": "POSITIVE"}

strategy_convert = {"H_SET": "S1", "H_ALL": "S2"}

EMDD = {}
DD = {}

for key in ["TwoRooms"]:


    emdd_result = pd.read_excel(emdd_file_dict[key])
    emdd_data_set = emdd_result["Data Set"]
    emdd_accuracy = emdd_result["Precision"]
    average_emdd_run_time = emdd_result["Average EMDD Run Time"]
    emdd_positive = emdd_result["Positive"]
    emdd_negative = emdd_result["Negative"]
    emdd_loop = emdd_result["Average Loop"]
    emdd_model = emdd_result["Method"]
    emdd_strategy = emdd_result["Search Set"]
    emdd_skip = emdd_result["Skipping Factor"]

    for i in range(len(emdd_data_set)):
        # print(f"Model {emdd_model[i]}")
        if not emdd_data_set[i] in EMDD:
            EMDD[emdd_data_set[i]] = {}
            temp = EMDD[emdd_data_set[i]]
        if not emdd_positive[i] in EMDD[emdd_data_set[i]]:
            EMDD[emdd_data_set[i]][emdd_positive[i]] = {}
        if not emdd_negative[i] in EMDD[emdd_data_set[i]][emdd_positive[i]]:
            EMDD[emdd_data_set[i]][emdd_positive[i]][emdd_negative[i]] = {}

        if not emdd_model[i] in EMDD[emdd_data_set[i]][emdd_positive[i]][emdd_negative[i]]:
            EMDD[emdd_data_set[i]][emdd_positive[i]][emdd_negative[i]][emdd_model[i]] = {}
        if not emdd_strategy[i] in EMDD[emdd_data_set[i]][emdd_positive[i]][emdd_negative[i]][emdd_model[i]]:
            EMDD[emdd_data_set[i]][emdd_positive[i]][emdd_negative[i]][emdd_model[i]][emdd_strategy[i]] = {}

        #if not emdd_skip[i] in EMDD[emdd_data_set[i]][emdd_positive[i]][emdd_negative[i]][emdd_model[i]][emdd_strategy[i]]:
        #    EMDD[emdd_data_set[i]][emdd_positive[i]][emdd_negative[i]][emdd_model[i]][emdd_strategy[i]][emdd_skip[i]] = {}

        EMDD[emdd_data_set[i]][emdd_positive[i]][emdd_negative[i]][emdd_model[i]][emdd_strategy[i]][emdd_skip[i]] = {"Precision": emdd_accuracy[i],
                                                                                                                     "Average EMDD Run Time": average_emdd_run_time[i],
                                                                                                                     "Average Loop": emdd_loop[i]}








    break

print("Alg. & Pstv & Ngtv & Strg & Model & Skip & Precision & Time")
for dataset in EMDD:
                is_exponential_fastest = True
                is_s1_faster = True
                for skip in [1, 2, 3, 4]:
                    for strategy in ["H_SET"]:
                        for p in [5, 10, 15, 20]:
                            for n in [0, 5, 10, 15, 20]:
                                linear_time = EMDD[dataset][p][n]["LINEAR"][strategy][skip]["Average EMDD Run Time"]
                                linear_ac = EMDD[dataset][p][n]["LINEAR"][strategy][skip]["Precision"]
                                exponential_time = EMDD[dataset][p][n]["EXPONENTIAL"][strategy][skip]["Average EMDD Run Time"]
                                exponential_ac = EMDD[dataset][p][n]["EXPONENTIAL"][strategy][skip]["Precision"]
                                if linear_time < exponential_time:
                                    print(f"Linear {p} & {n}& {strategy_convert[strategy]} & LIN & {skip}& {linear_ac:0.2f}& {linear_time:0.4f}\\\\")
                                    print(f"Linear {p} & {n}& {strategy_convert[strategy]} & EXP & {skip}& {exponential_ac:0.2f}& {exponential_time:0.4f}\\\\")
                                    print("\n")

                                    is_exponential_fastest = False

                is_s1_fastest = True
                for skip in [1, 2, 3, 4]:
                    for model in ["EXPONENTIAL", "LINEAR"]:
                        for p in [5, 10, 15, 20]:
                            for n in [0, 5, 10, 15, 20]:
                                s1_time = EMDD[dataset][p][n][model]["H_SET"][skip]["Average EMDD Run Time"]
                                s1_ac = EMDD[dataset][p][n][model]["H_SET"][skip]["Precision"]
                                s2_time = EMDD[dataset][p][n][model]["H_ALL"][skip]["Average EMDD Run Time"]
                                s2_ac = EMDD[dataset][p][n][model]["H_ALL"][skip]["Precision"]
                                if s2_time < s1_time:
                                    print(
                                        f"S1 {p} & {n}& S1 & {model} & {skip}& {s1_ac:0.2f}& {s1_time:0.4f}\\\\")
                                    print(
                                        f"S2 {p} & {n}& S2 & {model} & {skip}& {s2_ac:0.2f}& {s2_time:0.4f}\\\\")
                                    print("\n")

                                    is_s1_fastest = False


print(f"Is exponential always faster {is_exponential_fastest}")

print(f"Is S1 always faster {is_s1_faster}")

