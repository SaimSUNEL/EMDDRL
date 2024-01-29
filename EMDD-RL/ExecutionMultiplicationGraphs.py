import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import difflib

dd_file_dict = {210: "SPEEDExperimentDDResultAveraged.xlsx",
                310: "SPEEDExperimentDDTwoRooms1XResult.xlsx",
                410: "SPEEDExperimentDDTwoRooms2XResult.xlsx",
                510: "SPEEDExperimentDDTwoRooms3XResultAveraged.xlsx",
                610: "SPEEDExperimentDDTwoRooms4XResultAveraged.xlsx",
                710: "SPEEDExperimentDDTwoRooms5XResultAveraged.xlsx"}

emdd_file_dict = {210: "SPEEDExperimentEMDDResultAveraged.xlsx",
                  310: "SPEEDExperimentEMDDTwoRooms1XResultAveraged.xlsx",
                  410: "SPEEDExperimentEMDDTwoRooms2XResultAveraged.xlsx",
                  510:"SPEEDExperimentEMDDTwoRooms3XResultAveraged.xlsx",
                  610:"SPEEDExperimentEMDDTwoRooms4XResultAveraged.xlsx",
                  710:"SPEEDExperimentEMDDTwoRooms5XResultAveraged.xlsx"}


best_times = {"DD": {}, "EMDD": {}}

for key in dd_file_dict:

    dd_result = pd.read_excel(dd_file_dict[key])
    emdd_result = pd.read_excel(emdd_file_dict[key])
    best_times["DD"][key] = {}
    best_times["EMDD"][key] = {}
    # print(dd_result.keys())
    dd_data_set = dd_result["Data Set"]
    emdd_data_set = emdd_result["Data Set"]
    dd_accuracy = dd_result["Precision"]
    emdd_accuracy = emdd_result["Precision"]
    emdd_time = emdd_result["Total EMDD Run Time"]
    for i in range(len(dd_data_set)):
        if dd_data_set[i] == "EQUALLYBALANCED":
            continue
        dd_time = dd_result["Total EMDD Run Time"][i]
        best_times["DD"][key][dd_data_set[i]] = {"time": float(dd_time), "Precision": dd_accuracy[i] }
        best_times["EMDD"][key][dd_data_set[i]] = {}
        fastest_emdd_time = 10000000000
        best_model = None
        best_k = None
        best_search = None
        emdd_ac = None
        for k in range(len(emdd_data_set)):
            if emdd_data_set[k] == dd_data_set[i]:
                if float(dd_accuracy[i]) <= float(emdd_accuracy[k]):
                    if float(emdd_time[k]) < fastest_emdd_time:
                        fastest_emdd_time = float(emdd_time[k])
                        best_model = emdd_result["Method"][k]
                        best_search = emdd_result["Search Set"][k]
                        best_k = emdd_result["Skipping Factor"][k]
                        emdd_ac = emdd_result["Precision"][k]

        best_times["EMDD"][key][dd_data_set[i]]["time"] = fastest_emdd_time
        best_times["EMDD"][key][dd_data_set[i]]["model"] = best_model
        best_times["EMDD"][key][dd_data_set[i]]["search"] = best_search
        best_times["EMDD"][key][dd_data_set[i]]["k"] = best_k
        best_times["EMDD"][key][dd_data_set[i]]["Precision"] = emdd_ac


# print(best_times)

directory = "StateScaleAffectGraphs"

data_convert = {"STEPLIMITEQUALLYBALANCED": "STEPBALANCED",
                "STEPLIMITONLYPOSITIVE":"STEPPOSITIVE", "ONLYPOSITIVE": "POSITIVE"}

dd_bar = {}

info_dd = {}
info_emdd = {}
GRAPH_DATA = {}

for d_set in best_times["DD"][210]:
    print(d_set)
    indices = []
    run_times = []
    run2_times = []
    GRAPH_DATA[d_set] = {"DD": dict(), "EMDD": dict()}
    for run in [210 , 310, 410, 510, 610, 710]:
        indices.append(run)
        run_times.append(best_times["DD"][run][d_set]["time"])
        print("DD %s - %d - A:%%%.2f - T:%f" % (d_set, run, best_times["DD"][run][d_set]["Precision"]*100.0, best_times["DD"][run][d_set]["time"]))
        run2_times.append(best_times["EMDD"][run][d_set]["time"])
        print("EMDD %s - %d - A:%%%.2f - T:%f" % (d_set, run, best_times["EMDD"][run][d_set]["Precision"]*100.0, best_times["EMDD"][run][d_set]["time"]))
        # print("SDD\t")
        GRAPH_DATA[d_set]["DD"][run] = best_times["DD"][run][d_set]["time"]
        GRAPH_DATA[d_set]["EMDD"][run] = best_times["EMDD"][run][d_set]["time"]


    info_dd[data_convert[d_set]] = run_times
    info_emdd[data_convert[d_set]] = run2_times;

    # point graph
    # plt.plot(indices, run_times, 'o', indices, run2_times, 'o')
    # plt.xlabel("Environment State Count")
    # plt.ylabel("Running Time (sec)")
    # plt.title(data_convert[d_set])
    # plt.legend(["DD", "Adapted EMDD"])
    # plt.savefig("StateScaleAffectGraphs/"+data_convert[d_set]+".png")
    # plt.show()
    n_groups = 6
    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8
    rects1 = plt.bar(index, run_times, bar_width,
                      alpha=opacity,
                      label='DD')
    rects2 = plt.bar(index + bar_width, run2_times, bar_width,
                      alpha=opacity,
                      label='EMDD-RL')
    plt.xlabel('Environment State Count')
    plt.ylabel('Running Time (sec)')
    plt.title(data_convert[d_set])
    plt.xticks(index + bar_width, [210 , 310, 410, 510, 610, 710])
    plt.legend()

    plt.tight_layout()
    plt.savefig("StateScaleAffectGraphs/BARCHART"+data_convert[d_set]+".png")
    # plt.show()


#
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
#
# df = pd.DataFrame(np.random.rand(6, 4),
#                  index=['one', 'two', 'three', 'four', 'five', 'six'],
#                  columns=pd.Index(['A', 'B', 'C', 'D'],
#                  name='Genus')).round(2)
#
#
# df.plot(kind='bar',figsize=(10,4))
#
# ax = plt.gca()
# pos = []
# for bar in ax.patches:
#     pos.append(bar.get_x()+bar.get_width()/2.)
#
# ax.set_xticks(pos,minor=True)
# lab = []
# for i in range(len(pos)):
#     l = df.columns.values[i//len(df.index.values)]
#     lab.append(l)
#
# ax.set_xticklabels(lab,minor=True)
# ax.tick_params(axis='x', which='major', pad=15, size=0)
# plt.setp(ax.get_xticklabels(), rotation=0)

# plt.show()




ind = [210, 310, 410, 510,610,710]
labels = []
dd_data = []
emdd_data = []
for dataset in info_dd:
    labels.append(dataset)
    for k in range(len(info_dd[dataset])):
        dd_data.append(info_dd[dataset][k])
        emdd_data.append(info_emdd[dataset][k])



import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import functools

x = np.arange(len(dd_data))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, dd_data, width, label='DD')
rects2 = ax.bar(x + width/2, emdd_data, width, label='EMDD-RL')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Scores')
ax.set_title('Running Time and State Space Size')
ax.set_xticks(x)
ax.set_xticklabels(ind+ind+ind)
# Labels for the rectangles

for i in info_dd:
    print(i)
    for k in info_dd[i]:
        print(k,end="\t")
    print("\n\n")

ax.legend()

fig.tight_layout()

# plt.show()
print(GRAPH_DATA)

for method in ["DD", "EMDD"]:
    print(method, end="\t")
    for dataset in ["STEPLIMITEQUALLYBALANCED", "STEPLIMITONLYPOSITIVE", "ONLYPOSITIVE"]:
        for size in [210, 310, 410, 510,610,710]:
            print(GRAPH_DATA[dataset][method][size], end="\t")
    print()
