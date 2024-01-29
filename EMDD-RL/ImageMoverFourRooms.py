# -*- coding: utf-8 -*-

import os
import time
from PIL import Image
class EMDD:
    DISTANCE_METRIC_STANDARDIZATION = 1
    DISTANCE_METRIC_GRAPH = 2
    DISTANCE_METRIC_NONE = 3
    LINEAR = "LINEAR"
    DD_MODEL = "DDMODEL"
    EXPONENTIAL = "EXPONENTIAL"
    M_MODEL = LINEAR

    # on maximization step which states will be checked for maximum h
    # all positive instances
    H_ALL = "H_ALL"
    # or only h's neightbor hood.
    H_NEIGHBOR = "H_NEIGHBOR"
    H_SET = "H_SET"




STEP_LIMIT_EQUALLY_BALANCED = 1
STEP_LIMIT_ONLY_POSITIVE = 2
EQUALLY_BALANCED = 3
ONLY_POSITIVE = 4
dataset_defs  = {STEP_LIMIT_EQUALLY_BALANCED: "STEPLIMITEQUALLYBALANCED",
                                 STEP_LIMIT_ONLY_POSITIVE: "STEPLIMITONLYPOSITIVE",
                                 EQUALLY_BALANCED: "EQUALLYBALANCED",
                                 ONLY_POSITIVE: "ONLYPOSITIVE"}

dataset_array = [STEP_LIMIT_EQUALLY_BALANCED, STEP_LIMIT_ONLY_POSITIVE, EQUALLY_BALANCED, ONLY_POSITIVE]

algorithm = "EMDD" # "EMDD

# EMDD.H_SET, EMDD.H_NEIGHBOR, EMDD.H_ALL

search_set_array = [EMDD.H_SET, EMDD.H_ALL]

# EMDD.EXPONENTIAL
method_array = [EMDD.LINEAR, EMDD.EXPONENTIAL]

# 1, 2, 3, 4
skipping_factor_array = [1, 2,3,4]


if algorithm == "EMDD":
    for DATASET in dataset_array:

        for SEARCH_SET in search_set_array:


            for METHOD in method_array:

                for SKIPPING_FACTOR in skipping_factor_array:



                    if DATASET == STEP_LIMIT_EQUALLY_BALANCED or DATASET == STEP_LIMIT_ONLY_POSITIVE:
                        data_version = "ActionNoise(0.9)StepLimit(400)"
                    elif DATASET == EQUALLY_BALANCED or DATASET == ONLY_POSITIVE:
                        data_version = "ActionNoise(0.9)"
               # Experiment folder
                    if algorithm == "EMDD":
                        experiment_folder = "SpeedExperimentsFourRooms/"+data_version+"/"+dataset_defs[DATASET]+"/"+algorithm+"/"+METHOD+"/"+SEARCH_SET+"/"+str(SKIPPING_FACTOR)


                    dates = os.listdir(experiment_folder)
                    for ll in os.listdir(experiment_folder):
                        if not ll.__contains__(".png"):
                            dates=ll
                            break

                    image_folder = experiment_folder + "/" + dates

                    image_file = image_folder+"/"+data_version+dataset_defs[DATASET]+algorithm+SEARCH_SET+METHOD

                    # os.rename(image_file, image_file+".tga")
                    tga_exist = False
                    for files in os.listdir(image_folder):
                        if files.__contains__(".tga"):
                            tga_exist= True
                    print("Image file : ", image_file)
                    if not tga_exist:
                        os.rename(image_file, image_file+".tga")

                    img = Image.open(image_file+".tga")
                    #img.save(experiment_folder+"/" + data_version+dataset_defs[DATASET]+algorithm+SEARCH_SET+METHOD+".png")

                    cropped = img.crop((0, 0, 700, 700))
                    cropped.save(experiment_folder + "/" + data_version + dataset_defs[
                       DATASET] + algorithm + SEARCH_SET + METHOD + ".png")



elif algorithm == "DD":
    for DATASET in dataset_array:

        if DATASET == STEP_LIMIT_EQUALLY_BALANCED or DATASET == STEP_LIMIT_ONLY_POSITIVE:
            data_version = "ActionNoise(0.9)StepLimit(400)"
        elif DATASET == EQUALLY_BALANCED or DATASET == ONLY_POSITIVE:
            data_version = "ActionNoise(0.9)"
        # Experiment folder
        if algorithm == "DD":
            experiment_folder = "SpeedExperimentsFourRooms/" + data_version + "/" + dataset_defs[
                DATASET] + "/" + algorithm


        for ll in os.listdir(experiment_folder):
            if not ll.__contains__(".png"):
                dates = ll
                break

        image_folder = experiment_folder + "/" + dates

        image_file = image_folder + "/" + data_version + dataset_defs[DATASET] + algorithm
        print(image_file)
        # os.rename(image_file, image_file + ".tga")
        tga_exist = False
        for files in os.listdir(image_folder):
            if files.__contains__(".tga"):
                tga_exist = True

        if not tga_exist:
            os.rename(image_file, image_file + ".tga")
        img = Image.open(image_file + ".tga")
        #img.save(
        #    experiment_folder + "/" + data_version + dataset_defs[DATASET] + algorithm +".png")

        cropped = img.crop((0, 0, 700, 700))
        cropped.save(
            experiment_folder + "/" + data_version + dataset_defs[DATASET] + algorithm +".png")


