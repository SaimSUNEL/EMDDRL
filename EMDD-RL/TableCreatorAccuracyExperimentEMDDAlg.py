import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import difflib

emdd_file_dict = {#"TwoRooms": "AccuracyExperimentEMDDResult.xlsx"}
                "FourRooms" : "FourRoomsAccuracyExperimentEMDDResult.xlsx"}


data_convert = {"STEPLIMITEQUALLYBALANCED": "STEPBALANCED",
                "STEPLIMITONLYPOSITIVE": "STEPPOSITIVE",
                "ONLYPOSITIVE": "POSITIVE"}

strategy_convert = {"H_SET": "S1", "H_ALL": "S2"}


for key in emdd_file_dict.keys():

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
    print("*******************%s************************" % key)
    print("Positive & Negative & Strategy & Model & Skip Factor & Average Loop & Precision & Average Run Time\\\\\n\\hline")
    for i in range(len(emdd_data_set)):
        print("{posit} & {negat} & {strateg} & {mod} & {ski} & {loop} & {pres:0.2f} & {average_run:0.4f}\\\\\n\\hline".format(
                                                                           data_set_name=data_convert[emdd_data_set[i]],
                                                                           posit=emdd_positive[i],
                                                                           negat=emdd_negative[i],
                                                                           average_run=average_emdd_run_time[i],
                                                                           pres=emdd_accuracy[i],
                                                                           strateg=strategy_convert[emdd_strategy[i]],
                                                                           mod=emdd_model[i][0:3],
                                                                           ski=emdd_skip[i],
                                                                           loop=emdd_loop[i]
                                                                                    ))
    print("**********************************************")