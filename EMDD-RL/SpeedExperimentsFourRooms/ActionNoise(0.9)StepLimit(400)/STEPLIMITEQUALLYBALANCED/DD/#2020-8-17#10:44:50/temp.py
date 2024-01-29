import pickle

predictions = pickle.load(open("DDSELECTEDSTATES.pickle", "rb"))
GROUND_TRUTH = [71,72,74,75,
                             92,93,94,95,96,
                             113, 114, 116, 117,

                             171,172,173,
                             192,193,194,
                                       214,
                             234, 235, 236,
                             255, 256, 257,

                             302,303,305,306,
                             323,324,325,326,327,
                             344,345,347,348

                             ## aroun goal state
                             #161,162,163,164,165,
                             #182,186,
                             #203,207,
#
                             #245,249,
                             #266,270,
                             #287,288,289,290,291

                             ]
key_state_count = 0
for i in predictions:
    if i in GROUND_TRUTH:
        key_state_count += 1
accuracy = key_state_count/len(predictions)*100.0
print(len(predictions), accuracy)
# print(dirpath, x)