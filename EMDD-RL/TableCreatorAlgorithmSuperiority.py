# for each positive and negative bag count best EMDD-RL setting (the most accurate and the fastest) and the corresponding DD are compared...

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import difflib



emdd_file_dict = {"TwoRooms": "AccuracyExperimentEMDDResult.xlsx",
                "FourRooms" : "FourRoomsAccuracyExperimentEMDDResult.xlsx"}

dd_file_dict = {"TwoRooms": "AccuracyExperimentDDResult.xlsx",
                "FourRooms" : "FourRoomsAccuracyExperimentDDResult.xlsx"}

data_convert = {"STEPLIMITEQUALLYBALANCED": "STEPBALANCED",
                "STEPLIMITONLYPOSITIVE": "STEPPOSITIVE",
                "ONLYPOSITIVE": "POSITIVE"}

strategy_convert = {"H_SET": "S1", "H_ALL": "S2"}

EMDD = {}
DD = {}

for key in ["FourRooms"]:
    dd_result = pd.read_excel(dd_file_dict[key])
    dd_data_set = dd_result["Data Set"]
    dd_accuracy = dd_result["Precision"]
    average_dd_run_time = dd_result["Average DD Run Time"]
    dd_positive = dd_result["Positive"]
    dd_negative = dd_result["Negative"]

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
    for i in range(len(dd_data_set)):

        if not dd_data_set[i] in DD:
            DD[dd_data_set[i]] = {}
        if not dd_positive[i] in DD[dd_data_set[i]]:
            DD[dd_data_set[i]][dd_positive[i]] = {}
        #if not dd_negative[i] in DD[dd_data_set[i]][dd_positive[i]]:
        #    DD[dd_data_set[i]][dd_positive[i]][dd_negative[i]] = {}

        DD[dd_data_set[i]][dd_positive[i]][dd_negative[i]] = {"Precision": dd_accuracy[i],
                                                              "Average DD Run Time": average_dd_run_time[i]}









    break

print("Alg. & Pstv & Ngtv & Strg & Model & Skip & Precision & Time")
for dataset in EMDD:
    for p in [5, 10,15,20]:
        for n in [0, 5, 10, 15, 20]:
            dd_ac = DD[dataset][p][n]["Precision"]
            dd_time = DD[dataset][p][n]["Average DD Run Time"]

            best_emdd_skip = None
            best_emdd_model = None
            best_emdd_strategy = None
            best_emdd_accuracy = -1.0
            best_emdd_time = None

            for model in ["EXPONENTIAL", "LINEAR"]:
                for skip in [1, 2, 3, 4]:
                    for strategy in ["H_ALL", "H_SET"]:
                        emdd_ac = EMDD[dataset][p][n][model][strategy][skip]["Precision"]
                        emdd_time = EMDD[dataset][p][n][model][strategy][skip]["Average EMDD Run Time"]

                        if emdd_ac > best_emdd_accuracy:
                            best_emdd_accuracy = emdd_ac
                            best_emdd_skip = skip
                            best_emdd_time = emdd_time
                            best_emdd_model = model
                            best_emdd_strategy = strategy
                        elif abs(emdd_ac - best_emdd_accuracy) < 0.000001:
                            if emdd_time < best_emdd_time:
                                best_emdd_accuracy = emdd_ac
                                best_emdd_skip = skip
                                best_emdd_time = emdd_time
                                best_emdd_model = model
                                best_emdd_strategy = strategy


            message = "Better" if best_emdd_accuracy > dd_ac else ""
            message = "EQUAL" if abs(best_emdd_accuracy-dd_ac) < 0.0000001 else message
            row_color = None
            if message == "Better":
                row_color = "\\cellcolor{green}"
            elif message == "EQUAL":
                row_color = "" # white
            else:
                row_color = "\\cellcolor{red}"
            print(f"DD & \\multirow{{2}}{{2em}}{{ {p} }} & \\multirow{{2}}{{2em}}{{ {n} }} & & & & {dd_ac:0.2f} & {dd_time:0.4f}\\\\ \n {row_color} EMDDRL & & & {strategy_convert[best_emdd_strategy]} & {best_emdd_model[0:3]}& {best_emdd_skip}& {best_emdd_accuracy:0.2f}& {best_emdd_time:0.4f}\\\\ \\hline")








