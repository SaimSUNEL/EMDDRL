import os

NUMBER = 1

files = os.listdir(".")
for file_name in files:

    if "KeyRoom" in file_name:
        os.rename(file_name, "KeyRoomBagExperiment["+str(NUMBER)+"].txt")
        NUMBER += 1