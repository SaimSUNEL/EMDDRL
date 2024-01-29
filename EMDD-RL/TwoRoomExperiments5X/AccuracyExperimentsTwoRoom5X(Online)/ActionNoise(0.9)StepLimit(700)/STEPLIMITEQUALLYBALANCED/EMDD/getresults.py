import os
import pickle
import copy
import numpy as np
import numpy as np
import scipy.stats as st

hyperparameters = []
valid_experiment_count = 0

RESULTS = dict()

for dirpath, subdirs, files in os.walk("."):
    for x in files:
        if x  == "RUN.txt":

            model, S, k = dirpath.split("/")[1:-1]
            print(dirpath, x)
            print(model, S, k)

            if model not in RESULTS:
                RESULTS[model] = dict()

            if S not in RESULTS[model]:
                RESULTS[model][S] = dict()

            if k not in RESULTS[model][S]:
                RESULTS[model][S][k] = dict()


            prev = RESULTS[model][S][k]


            result_file = open(dirpath+"/"+x, "r")
            prev["accuracy"] = 0.0
            prev["average time"] = 0.0
            prev["prediction count"] = 0.0

            for line in result_file:
                line = line.strip("\n\r")
                if len(line) < 3:
                    continue
                if "Average" in line and "run time" in line:
                    valid_experiment_count += 1
                    run_time = float(line.split(": ")[1])
                    prev["average time"] = run_time
                if "Prediction Count" in line:
                    prediction_count = int(line.split(": ")[1])
                    prev["prediction count"] = prediction_count
                if "Precision" in line:
                    accuracy = float(line.split(": ")[1])
                    prev["accuracy"] = accuracy

            result_file.close()

            # predictions = pickle.load(open(dirpath+"/EMMD"+"SELECTEDSTATES.pickle", "rb"))

            # if len(predictions) > 0:
            #     key_state_count = 0
            #     for i in predictions:
            #         if i in GROUND_TRUTH:
            #             key_state_count += 1
            #     prev["accuracy"] = key_state_count/len(predictions)*100.0
            #     # print(len(predictions), predictions)
            #     # print(dirpath, x)

print(RESULTS)


values = []

for model in RESULTS:
    for S in RESULTS[model]:
        for k in RESULTS[model][S]:
            print(f"{model, S, k} : {RESULTS[model][S][k]['accuracy']}")
            values.append(RESULTS[model][S][k]['accuracy'])

print(len(values))
print(np.mean(values), np.std(values))
interval = st.t.interval(0.95, len(values) - 1, loc=np.mean(values),
                         scale=st.sem(values))
print("Interval : ", interval)


