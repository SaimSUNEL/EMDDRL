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

for key in ["FourRooms"]:


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


            for model in ["EXPONENTIAL"]:
                for skip in [1, 2, 3, 4]:
                    for strategy in ["H_SET"]:
                        for p in [5, 10, 15, 20]:
                            for n in [0, 5, 10, 15, 20]:

                                emdd_ac = EMDD[dataset][p][n][model][strategy][skip]["Precision"]
                                emdd_time = EMDD[dataset][p][n][model][strategy][skip]["Average EMDD Run Time"]

                                print(f"{p} & {n}& {strategy_convert[strategy]} & {model[0:3]}& {skip}& {emdd_ac:0.2f}& {emdd_time:0.4f}\\\\")
                            print("\\hline")
                    print("\\hline")






