import os
from termcolor import colored

file_names = []
files = os.listdir(".")
positive_bag_counts = set()
negative_bag_counts = set()
for file in files:
    if ".py" in file:
        continue
    file_names.append(file)
    # print(file)

    positive_episode_count = 0
    negative_episode_count = 0

    with open(file, "r") as dosya:
        for line in dosya:
            if len(line) < 4:
                continue
            parts = line.split(",")
            if parts[0] == "1":
                positive_episode_count += 1
            elif parts[0] == "0":
                negative_episode_count += 1

    if positive_episode_count < 21 or negative_episode_count < 21:
        print(colored("File %s is problematic" % file, "red"))
        # raise Exception("Insufficient number of positive or negative bags")
    positive_bag_counts.add(positive_episode_count)
    negative_bag_counts.add(negative_episode_count)

print("Total number of files %d" % (len(file_names)))
print("Positive bag counts : ", positive_bag_counts)
print("Negative bag counts : ", negative_bag_counts)