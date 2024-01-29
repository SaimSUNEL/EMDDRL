import pickle
import os
# candidate states for subgoals...
ground_truth_for_subgoals = [246,247,249,250,
                             317,318,319,320,321,
                             388,389,390,391,392,
                             459,460,462,463
                             ]




CONFIGS = dict()

for root, dirs, files in os.walk(".", topdown=False):
   for name in files:

      if name == "EMDDSELECTEDSTATES.pickle":
        print(root, name)
        _, model, selection, k_value, dataset_size = root.split("/")
        if model not in CONFIGS:
            CONFIGS[model] = dict()
        if selection not in CONFIGS[model]:
            CONFIGS[model][selection] = dict()
        k = k_value # .split("(")[1].split(")")[0]
        if k not in CONFIGS[model][selection]:
            CONFIGS[model][selection][k] = dict()

        positive_bags = dataset_size.split("#")[1].split("Positive")[0]
        negative_bags = dataset_size.split("#")[2].split("Negative")[0]

        if positive_bags not in CONFIGS[model][selection][k]:
            CONFIGS[model][selection][k][positive_bags] = dict()
        if negative_bags not in CONFIGS[model][selection][k][positive_bags]:
            CONFIGS[model][selection][k][positive_bags][negative_bags] = dict()


        states = pickle.load(open(root+"/EMDDSELECTEDSTATES.pickle", "rb"))


        hit_count = 0
        for i in states:
            if i in ground_truth_for_subgoals:
                hit_count += 1
        precision = float(hit_count) / float(len(states))
        recall = float(hit_count) / float(len(ground_truth_for_subgoals))
        if recall == 0 and precision == 0:
            recall=1
        f1 = 2 * float(precision) * float(recall) / (float(precision) + float(recall))
        print("Precision : ", precision)

        CONFIGS[model][selection][k][positive_bags][negative_bags]["Precision"] = precision
        CONFIGS[model][selection][k][positive_bags][negative_bags]["Recall"] = recall
        CONFIGS[model][selection][k][positive_bags][negative_bags]["F1"] = f1
best_configs = []
highest_value = -float('inf')

for model in CONFIGS:
    for selection in CONFIGS[model]:
        for k in CONFIGS[model][selection]:
            for positive_count in CONFIGS[model][selection][k]:
                for negative_bags in CONFIGS[model][selection][k][positive_count]:
                    precision = CONFIGS[model][selection][k][positive_count][negative_bags]["Precision"]
                    if precision>highest_value:
                        highest_value = precision

for model in CONFIGS:
    for selection in CONFIGS[model]:
        for k in CONFIGS[model][selection]:
            for positive_count in CONFIGS[model][selection][k]:
                for negative_bags in CONFIGS[model][selection][k][positive_count]:
                    precision = CONFIGS[model][selection][k][positive_count][negative_bags]["Precision"]
                    if highest_value-0.0000001 < precision < highest_value + 0.0000001:
                        highest_value = precision
                        best_configs.append((model, selection, k, positive_count, negative_bags))


print("Best value : ", highest_value)
print(best_configs)