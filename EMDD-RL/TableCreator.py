import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import difflib

dd_file_dict = {"TwoRooms": "SPEEDExperimentDDResultAveraged.xlsx",
                "FourRooms": "FourRoomsSPEEDExperimentDDResultAveraged.xlsx"}

emdd_file_dict = {"TwoRooms": "SPEEDExperimentEMDDResultAveraged.xlsx",
                  "FourRooms": "FourRoomsSPEEDExperimentEMDDResultAveraged.xlsx"}


best_times = {"DD": {}, "EMDD": {}}

emdd_info = {}
best_emdd_accuracy = {}

data_convert = {"STEPLIMITEQUALLYBALANCED": "STEPBALANCED",
                "STEPLIMITONLYPOSITIVE": "STEPPOSITIVE",
                "ONLYPOSITIVE": "POSITIVE"}
strategy_convert = {"H_SET": "S1", "H_ALL": "S2"}

for key in dd_file_dict:

    dd_result = pd.read_excel(dd_file_dict[key])
    emdd_result = pd.read_excel(emdd_file_dict[key])
    best_times["DD"][key] = {}
    best_times["EMDD"][key] = {}
    emdd_info[key] = {"Data Set": emdd_result["Data Set"], "Precision": emdd_result["Precision"], "Skipping Factor": emdd_result["Skipping Factor"],
                                                 "Time": emdd_result["Average EMDD Run Time"], "Method": emdd_result["Method"],
                                                 "Search Set": emdd_result["Search Set"]}
    # print(dd_result.keys())
    best_emdd_accuracy[key] = {}
    dd_data_set = dd_result["Data Set"]
    emdd_data_set = emdd_result["Data Set"]
    dd_accuracy = dd_result["Precision"]
    emdd_accuracy = emdd_result["Precision"]
    emdd_time = emdd_result["Average EMDD Run Time"]


    for i in range(len(dd_data_set)):
        if dd_data_set[i] == "EQUALLYBALANCED":
            continue
        dd_time = dd_result["Average EMDD Run Time"][i]
        best_times["DD"][key][dd_data_set[i]] = {"time": float(dd_time), "Precision": dd_accuracy[i]}
        best_times["EMDD"][key][dd_data_set[i]] = {}
        best_emdd_accuracy[key][dd_data_set[i]] = {}
        fastest_emdd_time = 10000000000
        most_accurate_emdd = 0.0

        best_model = None
        best_k = None
        best_search = None
        best_loop = None
        emdd_ac = None


        most_accurate_k = None
        most_accurate_strategy = None
        most_accurate_model = None
        most_accuracy_loop = None
        most_accurate_time = None


        for k in range(len(emdd_data_set)):
            if emdd_data_set[k] == dd_data_set[i]:
                if float(dd_accuracy[i]) <= float(emdd_accuracy[k]):
                    if float(emdd_time[k]) < fastest_emdd_time:
                        fastest_emdd_time = float(emdd_time[k])
                        best_model = emdd_result["Method"][k]
                        best_search = emdd_result["Search Set"][k]
                        best_k = emdd_result["Skipping Factor"][k]
                        best_loop = emdd_result["Average Loop"][k]
                        emdd_ac = emdd_result["Precision"][k]

                if float(emdd_accuracy[k]) > most_accurate_emdd:
                    most_accurate_emdd = float(emdd_accuracy[k])
                    most_accurate_k = emdd_result["Skipping Factor"][k]
                    most_accurate_strategy = emdd_result["Search Set"][k]
                    most_accurate_model = emdd_result["Method"][k]
                    most_accuracy_loop = best_loop = emdd_result["Average Loop"][k]
                    most_accurate_time = float(emdd_time[k])
                if float(emdd_accuracy[k]) == most_accurate_emdd:
                    if float(emdd_time[k]) < most_accurate_time:
                        most_accurate_emdd = float(emdd_accuracy[k])
                        most_accurate_k = emdd_result["Skipping Factor"][k]
                        most_accurate_strategy = emdd_result["Search Set"][k]
                        most_accurate_model = emdd_result["Method"][k]
                        most_accurate_time = float(emdd_time[k])
                        most_accuracy_loop = best_loop = emdd_result["Average Loop"][k]

        best_emdd_accuracy[key][dd_data_set[i]]["time"] = most_accurate_time
        best_emdd_accuracy[key][dd_data_set[i]]["model"] = most_accurate_model
        best_emdd_accuracy[key][dd_data_set[i]]["search"] = most_accurate_strategy
        best_emdd_accuracy[key][dd_data_set[i]]["k"] = most_accurate_k
        best_emdd_accuracy[key][dd_data_set[i]]["Precision"] = most_accurate_emdd
        best_emdd_accuracy[key][dd_data_set[i]]["Loop"] = most_accuracy_loop


        best_times["EMDD"][key][dd_data_set[i]]["time"] = fastest_emdd_time
        best_times["EMDD"][key][dd_data_set[i]]["model"] = best_model
        best_times["EMDD"][key][dd_data_set[i]]["search"] = best_search
        best_times["EMDD"][key][dd_data_set[i]]["k"] = best_k
        best_times["EMDD"][key][dd_data_set[i]]["Precision"] = emdd_ac
        best_times["EMDD"][key][dd_data_set[i]]["Loop"] = best_loop


for env in best_times["EMDD"]:
    for dataset in best_times["EMDD"][env]:
        print("%s : %s DD Precision : %f, Time : %f - EMDD Precision : %f, Time : %f, k : %d, Strategy : %s, Model : %s, Loop : %f (Speed gain : %.2f)" % \
              (env, dataset, best_times["DD"][env][dataset]["Precision"], best_times["DD"][env][dataset]["time"],
               best_times["EMDD"][env][dataset]["Precision"], best_times["EMDD"][env][dataset]["time"],
               best_times["EMDD"][env][dataset]["k"], best_times["EMDD"][env][dataset]["search"],
               best_times["EMDD"][env][dataset]["model"], best_times["EMDD"][env][dataset]["Loop"], float( best_times["DD"][env][dataset]["time"])/ float( best_times["EMDD"][env][dataset]["time"])))
        print("%s&%s&%s&%d&%.2f&%.2f&%.4f\\\\" % (
        data_convert[dataset], strategy_convert[best_times["EMDD"][env][dataset]["search"]], best_times["EMDD"][env][dataset]["model"][:3],
        best_times["EMDD"][env][dataset]["k"],
        best_times["EMDD"][env][dataset]["Loop"], best_times["EMDD"][env][dataset]["Precision"], best_times["EMDD"][env][dataset]["time"]))

        emdd_data = emdd_info[env]
        d = emdd_data["Data Set"]
        p = emdd_data["Precision"]
        t = emdd_data["Time"]
        k = emdd_data["Skipping Factor"]
        m = emdd_data["Method"]
        s = emdd_data["Search Set"]
        # print(s)
        print("HSET EXPONENTIAL")
        for v in range(len(d)):

            if d[v] == dataset and k[v] ==  best_times["EMDD"][env][dataset]["k"] and m[v] == "EXPONENTIAL" and s[v] == "H_SET":
                print("EMDD Precision : %f, Time : %f, k : %d, Strategy : %s, Model : %s (Speed gain : %.2f)" % (p[v], t[v],
                    best_times["EMDD"][env][dataset]["k"], s[v],
                    m[v], float( best_times["DD"][env][dataset]["time"])/ float( t[v])))
                print()
                print("%s&%s&%s&%d&%.2f&%.2f&%.4f\\\\" % (data_convert[dataset], strategy_convert[s[v]], m[v][0:3], best_times["EMDD"][env][dataset]["k"], best_times["EMDD"][env][dataset]["Loop"], p[v], t[v]))

        print("the Fastest Most Accurate EMDD")
        print("EMDD Precision : %f, Time : %f, k : %d, Strategy : %s, Model : %s, Loop : %f (Speed gain : %.2f)" %
              (best_emdd_accuracy[env][dataset]["Precision"],
               best_emdd_accuracy[env][dataset]["time"],
               best_emdd_accuracy[env][dataset]["k"],
               best_emdd_accuracy[env][dataset]["search"],
               best_emdd_accuracy[env][dataset]["model"],
               best_emdd_accuracy[env][dataset]["Loop"]
               , float(best_times["DD"][env][dataset]["time"]) / float(best_emdd_accuracy[env][dataset]["time"])))
        print("%s&%s&%s&%d&%.2f&%.2f&%.4f\\\\" % (
            data_convert[dataset], strategy_convert[best_emdd_accuracy[env][dataset]["search"]], best_emdd_accuracy[env][dataset]["model"][:3],
            best_emdd_accuracy[env][dataset]["k"],
            best_emdd_accuracy[env][dataset]["Loop"], best_emdd_accuracy[env][dataset]["Precision"],
            best_emdd_accuracy[env][dataset]["time"]))

        print("\n\n\n")

