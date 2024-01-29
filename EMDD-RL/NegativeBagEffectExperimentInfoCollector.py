from Environments import RLTwoRoomsEnvironment
from MIL.Methods.DD import DiverseDensity
from MIL.Methods.EMDD import EMDD
import os
from PIL import Image
import cv2
STEP_LIMIT_EQUALLY_BALANCED = 1
EQUALLY_BALANCED = 3
import pickle

G = pickle.load(open("MIL/data/TwoRoomsEnvironmentDistanceDict.pck", "rb"))

algorithm = "EMDD" # "EMDD

DATASET = STEP_LIMIT_EQUALLY_BALANCED

NEGATIVE_BAG_COUNT = 5

# EMDD.H_SET, EMDD.H_NEIGHBOR, EMDD.H_ALL
SEARCH_SET = EMDD.H_SET

ALGORITHM_ARRAY = ["EMDD", "DD"]
DATASET_ARRAY = [STEP_LIMIT_EQUALLY_BALANCED, EQUALLY_BALANCED]
METHOD_ARRAY = [EMDD.LINEAR, EMDD.EXPONENTIAL]
SEARCH_ARRAY = [EMDD.H_ALL, EMDD.H_SET]
SKIP_ARRAY = [1, 2, 3, 4]
NEGATIVE_BAG_COUNT_ARRAY = [0, 5, 10, 15, 20]

# EMDD.EXPONENTIAL
METHOD = EMDD.EXPONENTIAL

# 1, 2, 3, 4
SKIPPING_FACTOR = 1


dataset_defs  = {STEP_LIMIT_EQUALLY_BALANCED: "STEPLIMITEQUALLYBALANCED",
                 EQUALLY_BALANCED: "EQUALLYBALANCED"}

html_text = """
<html>
<head>
<title></title>
</head>
<body>

"""


for algorithm in ALGORITHM_ARRAY:
    for DATASET in DATASET_ARRAY:
        if algorithm == "EMDD":
            for METHOD in METHOD_ARRAY:
                for SEARCH_SET in SEARCH_ARRAY:
                    for SKIPPING_FACTOR in SKIP_ARRAY:
                        for NEGATIVE_BAG_COUNT in NEGATIVE_BAG_COUNT_ARRAY:
                            print("Dataset : ", dataset_defs[DATASET])
                            print("Algorithm : ", algorithm)
                            print("SEARCH :", SEARCH_SET)
                            print("METHOD : ", METHOD)
                            print("SKIP : ", SKIPPING_FACTOR)
                            print("NEGATIVE BAG COUNT", NEGATIVE_BAG_COUNT)
                            if DATASET == STEP_LIMIT_EQUALLY_BALANCED:
                                data_version = "ActionNoise(0.9)StepLimit(200)"
                            elif DATASET == EQUALLY_BALANCED:
                                data_version = "ActionNoise(0.9)"

                            included_experiment_count = 0

                            total_dd_time = 0

                            total_emdd_time = 0

                            # Experiment folder
                            if algorithm == "EMDD":
                                experiment_folder = "NegativeBagEffectExperiments/" + data_version + "/" + dataset_defs[
                                    DATASET] + "/" + algorithm + "/" + METHOD + "/" + SEARCH_SET + "/" + str(
                                    SKIPPING_FACTOR)
                            else:
                                experiment_folder = "NegativeBagEffectExperiments/" + data_version + "/" + dataset_defs[
                                    DATASET] + "/" + algorithm
                            t_folder = experiment_folder +  "/%2320Positive" + "%23" + str(NEGATIVE_BAG_COUNT) + "Negative"
                            experiment_folder += "/#20Positive" + "#" + str(NEGATIVE_BAG_COUNT) + "Negative"

                            experiment_folder += "/"
                            t_folder += "/"


                            image_file = experiment_folder +data_version + "" + dataset_defs[
                                        DATASET] + "" + algorithm + SEARCH_SET + METHOD + "#20Positive#" + str(
                                        NEGATIVE_BAG_COUNT) + "Negative"

                            img_file =  t_folder +data_version + "" + dataset_defs[
                                        DATASET] + "" + algorithm + SEARCH_SET + METHOD + "%2320Positive%23" + str(
                                        NEGATIVE_BAG_COUNT) + "Negative"

                            # os.rename(image_file, image_file+".tga")
                            # img = Image.open(image_file+".tga")
                            # img.save(image_file+".png")

                            print(image_file)
                            html_text += """
                                        <h1>%s</h1>
                                        """ % (data_version + "" + dataset_defs[
                                        DATASET] + "" + algorithm + SEARCH_SET + METHOD + "#"+str(SKIPPING_FACTOR)+"#20Positive#" + str(
                                        NEGATIVE_BAG_COUNT) + "Negative")
                            html_text += """<img src=\"%s\" height=600 width=800 />""" % (img_file+".png")

                            counts = states = pickle.load(
                                open(experiment_folder + algorithm + "SELECTEDSTATES.pickle", "rb"))
                            elements = set(states)
                            # 94, 115
                            distance_info = {}
                            for i in set(counts):
                                distance_info[i] = {"count": counts.count(i),
                                                    "average_distance": float(G[94][i] + G[115][i]) / 2.0}
                        html_text +="<hr><hr>"
            pass
        elif algorithm == "DD":
            for NEGATIVE_BAG_COUNT in NEGATIVE_BAG_COUNT_ARRAY:
                print("Dataset : ", dataset_defs[DATASET])
                print("Algorithm : ", algorithm)
                print("NEGATIVE BAG COUNT", NEGATIVE_BAG_COUNT)
                if DATASET == STEP_LIMIT_EQUALLY_BALANCED:
                    data_version = "ActionNoise(0.9)StepLimit(200)"
                elif DATASET == EQUALLY_BALANCED:
                    data_version = "ActionNoise(0.9)"

                # Experiment folder
                if algorithm == "EMDD":
                    experiment_folder = "NegativeBagEffectExperiments/" + data_version + "/" + dataset_defs[
                        DATASET] + "/" + algorithm + "/" + METHOD + "/" + SEARCH_SET + "/" + str(
                        SKIPPING_FACTOR)
                else:
                    experiment_folder = "NegativeBagEffectExperiments/" + data_version + "/" + dataset_defs[
                        DATASET] + "/" + algorithm
                t_folder = experiment_folder + "/%2320Positive" + "%23" + str(NEGATIVE_BAG_COUNT) + "Negative"
                experiment_folder += "/#20Positive" + "#" + str(NEGATIVE_BAG_COUNT) + "Negative"

                experiment_folder += "/"
                t_folder += "/"

                image_file = experiment_folder + data_version + "" + dataset_defs[
                    DATASET] + "" + algorithm + "#20Positive#" + str(
                    NEGATIVE_BAG_COUNT) + "Negative"

                img_file = t_folder + data_version + "" + dataset_defs[
                    DATASET] + "" + algorithm + "%2320Positive%23" + str(
                    NEGATIVE_BAG_COUNT) + "Negative"

                # os.rename(image_file, image_file+".tga")
                # img = Image.open(image_file)
                # img.save(image_file+".png")

                print(image_file)
                html_text += """
                            <h1>%s</h1>
                            """ % (data_version + "" + dataset_defs[
                    DATASET] + "" + algorithm + SEARCH_SET + METHOD + "#" + str(SKIPPING_FACTOR) + "#20Positive#" + str(
                    NEGATIVE_BAG_COUNT) + "Negative")
                html_text += """<img src=\"%s\" height=600 width=800 />""" % (img_file + ".png")

                counts = states = pickle.load(
                    open(experiment_folder + algorithm + "SELECTEDSTATES.pickle", "rb"))
                elements = set(states)
                # 94, 115
                distance_info = {}
                for i in set(counts):
                    distance_info[i] = {"count": counts.count(i),
                                        "average_distance": float(G[94][i] + G[115][i]) / 2.0}
            html_text += "<hr><hr>"
            pass


html_text += """
</body>
</html>
"""

html = open("NegativeBagEffectExperimentTwoRoomsResults.html", "w")
html.write(html_text)
html.close()