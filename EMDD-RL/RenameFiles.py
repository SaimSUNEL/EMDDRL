import os

data_directory_path ="MIL/data/POMDP/TwoRoomsV3QAgentTrajectories/ActionNoise(0.9)StepLimit(400)"
files = os.listdir(data_directory_path)
print("Files", files)

for file in files:
    os.rename(data_directory_path+"/"+file, data_directory_path+"/"+file.replace())