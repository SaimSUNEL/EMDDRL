import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import difflib

dd_file_dict = {"TwoRooms": "AccuracyExperimentDDResult.xlsx",
                "FourRooms" : "FourRoomsAccuracyExperimentDDResult.xlsx"}


data_convert = {"STEPLIMITEQUALLYBALANCED": "STEPBALANCED",
                "STEPLIMITONLYPOSITIVE": "STEPPOSITIVE",
                "ONLYPOSITIVE": "POSITIVE"}


for key in dd_file_dict:

    dd_result = pd.read_excel(dd_file_dict[key])
    dd_data_set = dd_result["Data Set"]
    dd_accuracy = dd_result["Precision"]
    average_dd_run_time = dd_result["Average DD Run Time"]
    dd_positive = dd_result["Positive"]
    dd_negative = dd_result["Negative"]
    print("*******************%s************************" % key)
    print("Dataset & Positive & Negative & Precision & Average Run Time\\\\\n\\hline")
    for i in range(len(dd_data_set)):
        print("{data_set_name} & {posit} & {negat} & {pres:0.2f} & {average_run:0.4f}\\\\\n\\hline".format(data_set_name=data_convert[dd_data_set[i]],
                                                                           posit=dd_positive[i],
                                                                           negat=dd_negative[i],
                                                                           average_run=average_dd_run_time[i],
                                                                                    pres=dd_accuracy[i]
                                                                                    ))
    print("**********************************************")