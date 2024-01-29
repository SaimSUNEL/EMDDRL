import json as js
with open('AccuracyExperimentVisualizationFourRooms/AccuracyExperiment.json', 'r') as fp:
    four_rooms_json = js.load(fp)


with open('AccuracyExperimentVisualization/AccuracyExperiment.json', 'r') as fp:
    two_rooms_json = js.load(fp)





# print(four_rooms_json)
# print(two_rooms_json)

NEGATIVE_ARRAY = [0,5,10,15,20]
POSITIVE_ARRAY = [5,10,15,20]
DATASETS = ["EQUALLYBALANCED", "STEPLIMITEQUALLYBALANCED"]

bests = {}
print("\n\n\nFour Rooms\n\n\n")
four_room_dataset = {"STEPLIMITEQUALLYBALANCED": "D7", "EQUALLYBALANCED": "D5" }

for DATASET in DATASETS:
    if not bests.has_key(DATASET):
        bests[DATASET] = {}
    for POSITIVE in POSITIVE_ARRAY:
        if not bests[DATASET].has_key(POSITIVE):
            bests[DATASET][POSITIVE] = {}
        for NEGATIVE in NEGATIVE_ARRAY:
            if not bests[DATASET][POSITIVE].has_key(NEGATIVE):
                bests[DATASET][POSITIVE][NEGATIVE] = {}


            dd_accuracy = four_rooms_json["DD"][DATASET][str(NEGATIVE)][str(POSITIVE)]
            bests[DATASET][POSITIVE][NEGATIVE]["DD"]=dd_accuracy




            best_emdd = {"Precision": -1.0}
            searches = {}

            for SEARCH in ["H_ALL", "H_SET"]:
                searches[SEARCH] = {"Precision": -1.0}
                for METHOD in ["EXPONENTIAL", "LINEAR"]:
                    for SKIP in [1, 2, 3]:
                        current_emdd_precision = four_rooms_json["EMDD"][DATASET][METHOD][SEARCH][str(SKIP)][str(NEGATIVE)][str(POSITIVE)]["Precision"]
                        # print(four_rooms_json["EMDD"][DATASET][METHOD][SEARCH][str(SKIP)][str(NEGATIVE)][str(POSITIVE)])
                        if current_emdd_precision > searches[SEARCH]["Precision"]:
                            searches[SEARCH]["Precision"] = current_emdd_precision
                            searches[SEARCH]["Method"] = METHOD
                            searches[SEARCH]["Skip"] = SKIP

                            searches[SEARCH]["config"] = \
                            four_rooms_json["EMDD"][DATASET][METHOD][SEARCH][str(SKIP)][str(NEGATIVE)][str(POSITIVE)]

                        if current_emdd_precision > best_emdd["Precision"]:
                            best_emdd["Precision"] = current_emdd_precision
                            best_emdd["Method"] = METHOD
                            best_emdd["Search"] = SEARCH
                            best_emdd["Skip"] = SKIP
                            best_emdd["config"] = four_rooms_json["EMDD"][DATASET][METHOD][SEARCH][str(SKIP)][str(NEGATIVE)][str(POSITIVE)]
                        #print(current_emdd_precision)
            bests[DATASET][POSITIVE][NEGATIVE]["EMDD"] = best_emdd["config"]
            bests[DATASET][POSITIVE][NEGATIVE]["EMDDDetailed"] = searches

            # print("DATASET: %s, P: %d, N: %d, DD: %f, EMDD(H_ALL): %f, (M:%s, k: %d) - EMDD(H_SET): %f, (M:%s, k:%d)" %
            #       (DATASET, POSITIVE, NEGATIVE, dd_accuracy["Precision"], searches["H_ALL"]["Precision"],
            #        searches["H_ALL"]["Method"],  searches["H_ALL"]["Skip"], searches["H_SET"]["Precision"],
            #        searches["H_SET"]["Method"], searches["H_SET"]["Skip"]))
            #
            print("%s & %d & %d & %.3f & %.3f & %.3f & %s & %d & %.3f & %.3f & %s & %d & %.3f\\\\" %
                  (four_room_dataset[DATASET], POSITIVE, NEGATIVE, dd_accuracy["Precision"],
                   float(dd_accuracy["Average DD run time "]),
                   searches["H_ALL"]["Precision"], searches["H_ALL"]["Method"][0:3], searches["H_ALL"]["Skip"],
                   float(searches["H_ALL"]["config"]["Average EMDD runtime "]),
                   searches["H_SET"]["Precision"], searches["H_SET"]["Method"][0:3], searches["H_SET"]["Skip"],
                   float(searches["H_SET"]["config"]["Average EMDD runtime "])))

print("\n\n\nTwo Rooms\n\n\n")
two_room_dataset = {"STEPLIMITEQUALLYBALANCED": "D3", "EQUALLYBALANCED": "D1" }
for DATASET in DATASETS:
    if not bests.has_key(DATASET):
        bests[DATASET] = {}
    for POSITIVE in POSITIVE_ARRAY:
        if not bests[DATASET].has_key(POSITIVE):
            bests[DATASET][POSITIVE] = {}
        for NEGATIVE in NEGATIVE_ARRAY:
            if not bests[DATASET][POSITIVE].has_key(NEGATIVE):
                bests[DATASET][POSITIVE][NEGATIVE] = {}


            dd_accuracy = two_rooms_json["DD"][DATASET][str(NEGATIVE)][str(POSITIVE)]
            bests[DATASET][POSITIVE][NEGATIVE]["DD"]=dd_accuracy


            best_emdd = {"Precision": -1.0}
            searches = {}

            for SEARCH in ["H_ALL", "H_SET"]:
                searches[SEARCH] = {"Precision": -1.0}
                for METHOD in ["EXPONENTIAL", "LINEAR"]:
                    for SKIP in [1, 2, 3]:
                        current_emdd_precision = two_rooms_json["EMDD"][DATASET][METHOD][SEARCH][str(SKIP)][str(NEGATIVE)][str(POSITIVE)]["Precision"]

                        if current_emdd_precision > searches[SEARCH]["Precision"]:
                            searches[SEARCH]["Precision"] = current_emdd_precision
                            searches[SEARCH]["Method"] = METHOD
                            searches[SEARCH]["Skip"] = SKIP

                            searches[SEARCH]["config"] = \
                            four_rooms_json["EMDD"][DATASET][METHOD][SEARCH][str(SKIP)][str(NEGATIVE)][str(POSITIVE)]

                        if current_emdd_precision > best_emdd["Precision"]:
                            best_emdd["Precision"] = current_emdd_precision
                            best_emdd["Method"] = METHOD
                            best_emdd["Search"] = SEARCH
                            best_emdd["Skip"] = SKIP
                            best_emdd["config"] = two_rooms_json["EMDD"][DATASET][METHOD][SEARCH][str(SKIP)][str(NEGATIVE)][str(POSITIVE)]
                        #print(current_emdd_precision)
            bests[DATASET][POSITIVE][NEGATIVE]["EMDD"] = best_emdd["config"]
            bests[DATASET][POSITIVE][NEGATIVE]["EMDDDetailed"] = searches

            # print("DATASET: %s, P: %d, N: %d, DD: %f, EMDD(H_ALL): %f, (M:%s, k: %d) - EMDD(H_SET): %f, (M:%s, k:%d)" %
            #       (DATASET, POSITIVE, NEGATIVE, dd_accuracy["Precision"], searches["H_ALL"]["Precision"],
            #        searches["H_ALL"]["Method"],  searches["H_ALL"]["Skip"], searches["H_SET"]["Precision"],
            #        searches["H_SET"]["Method"], searches["H_SET"]["Skip"]))

            print("%s & %d & %d & %.3f & %.3f & %.3f & %s & %d & %.3f & %.3f & %s & %d & %.3f\\\\" %
                  (two_room_dataset[DATASET], POSITIVE, NEGATIVE, dd_accuracy["Precision"], float(dd_accuracy["Average DD run time "]),
                   searches["H_ALL"]["Precision"], searches["H_ALL"]["Method"][0:3], searches["H_ALL"]["Skip"], float(searches["H_ALL"]["config"]["Average EMDD runtime "]),
                   searches["H_SET"]["Precision"], searches["H_SET"]["Method"][0:3], searches["H_SET"]["Skip"], float(searches["H_SET"]["config"]["Average EMDD runtime "])))

print("Okay...")