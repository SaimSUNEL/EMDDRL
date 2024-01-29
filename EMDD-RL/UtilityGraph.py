import matplotlib.pyplot as plt
import numpy as np
import os

option_episodes = []


def getData(agent_name, environment_name):
    max_33 = 0
    max_file = None
    data_directory = "UtilityExperiments/"+agent_name+"/"+environment_name
    data_files = os.listdir(data_directory)
    # first 200 episodes are considered....
    EPISODE_COUNT = 60
    step_array = np.zeros(EPISODE_COUNT, dtype=np.float32)

    step_matrix =  []

    file_count = 0

    for file_name in data_files:
        file_count += 1
        dosya = open(data_directory+"/"+file_name, "r")
        lines = dosya.readlines()
        dosya.close()
        reward_array = lines[0]
        if file_name.__contains__("EMDD"):
            episode = lines[3][1:-1]
            option_episodes.append(episode)

        steps = lines[1]
        arr = []
        parts = steps.split(",")
        for part in parts:
            d = part

            if part.__contains__("["):
                d = part[1:]

            if part.__contains__("]"):
                if part.__contains__("\n"):
                    d = part[:-2]
                else:
                    d = part[:-1]

            arr.append(int(d))
        print("%s Array" % file_name)
        print(arr)
        step_matrix.append(arr)
        if step_array[28] > max_33:
            max_33 = step_array[28]
            max_file = file_name
        for i in range(len(step_array)):
            step_array [i] += arr[i]

        # print(arr)
        # exit()
    step_matrix = np.array(step_matrix,dtype=np.float32)
    mean_values = step_matrix.mean(axis=0)[:EPISODE_COUNT]
    std_deviation = step_matrix.std(axis=0)[:EPISODE_COUNT]
    variance = np.sqrt(step_matrix.var(axis=0)[:EPISODE_COUNT])
    print("Step matrix shape : ", step_matrix.shape)
    step_array /= float(file_count)
    print("File count : ", file_count)
    print("Max 33 : ", max_33)
    print("Max file : ", max_file,)

    return mean_values, std_deviation, step_matrix

q_mean_values, q_std_deviation, q_step_matrix = getData("QAgent", "TwoRooms")
emdd_mean_values, emdd_std_deviation, emdd_step_matrix = getData("EMDDQAgent", "TwoRooms")
sarsa_mean_values, sarsa_std_deviation, sarsa_step_matrix = getData("Sarsa", "TwoRooms")

print("\n\nDeneme")
# print(q_step_matrix)
# print(type(q_step_matrix))

q_batch_mean = []
q_batch_low = []
q_batch_upper = []

emdd_batch_mean = []
emdd_batch_low = []
emdd_batch_upper = []

sarsa_batch_mean = []
sarsa_batch_low = []
sarsa_batch_upper = []

for u in range(40):
    print("Episode : ", u)

    q_information = {}
    emdd_information = {}
    sarsa_information = {}

    for episode_count in range(60):
        samples_q = q_step_matrix[:, episode_count:episode_count+1]
        samples_q = samples_q.reshape((len(samples_q)))

        samples_emdd = emdd_step_matrix[:, episode_count: episode_count+1]
        samples_emdd = samples_emdd.reshape(len(samples_emdd))

        samples_sarsa = sarsa_step_matrix[:, episode_count: episode_count+1]
        samples_sarsa = samples_sarsa.reshape(len(samples_sarsa))


        times = 1000
        array_q = []
        array_emdd = []
        array_sarsa = []
        for i in range(times):
            sampled_q = np.random.choice(samples_q, 32, replace=True)
            array_q.append(sampled_q.mean())

            sampled_emdd = np.random.choice(samples_emdd, 32, replace=True)
            array_emdd.append(sampled_emdd.mean())

            sampled_sarsa = np.random.choice(samples_sarsa, 32, replace=True)
            array_sarsa.append(sampled_sarsa.mean())

        array_q = sorted(array_q)
        array_emdd = sorted(array_emdd)
        array_sarsa = sorted(array_sarsa)

        alpha = 0.95
        p = ((1.0 - alpha) / 2.0) * 100
        lower_q = np.percentile(array_q, p)
        lower_emdd = np.percentile(array_emdd, p)
        lower_sarsa = np.percentile(array_sarsa, p)

        upper_q = np.percentile(array_q, (alpha+(1.0 - alpha) / 2.0)*100)
        upper_emdd = np.percentile(array_emdd, (alpha+(1.0 - alpha) / 2.0)*100)
        upper_sarsa = np.percentile(array_sarsa, (alpha+(1.0 - alpha) / 2.0)*100)

        q_information[episode_count+1] = [lower_q, np.mean(array_q),upper_q]
        emdd_information[episode_count + 1] = [lower_emdd, np.mean(array_emdd), upper_emdd]
        sarsa_information[episode_count+1] = [lower_sarsa, np.mean(array_sarsa), upper_sarsa]


    q_mean_values = []
    q_low_values = []
    q_upper_values = []

    emdd_mean_values = []
    emdd_low_values = []
    emdd_upper_values = []

    sarsa_mean_values = []
    sarsa_low_values = []
    sarsa_upper_values = []

    start_episode = 20

    for i in range(start_episode, 56):
        print("i = %d" % i)
        q_mean_values.append(q_information[i][1])
        print("len mean %d\n" % len(q_mean_values))
        q_low_values.append(q_information[i][0])
        q_upper_values.append(q_information[i][2])

        emdd_mean_values.append(emdd_information[i][1])
        emdd_low_values.append(emdd_information[i][0])
        emdd_upper_values.append(emdd_information[i][2])

        sarsa_mean_values.append(sarsa_information[i][1])
        sarsa_low_values.append(sarsa_information[i][0])
        sarsa_upper_values.append(sarsa_information[i][2])

        print(emdd_information[i][2])
        print(emdd_information[i][0])

    print("q mean values size : ", len(q_mean_values))
    q_mean_values = np.array(q_mean_values, dtype=np.float32)
    q_low_values = np.array(q_low_values, dtype=np.float32)
    q_upper_values = np.array(q_upper_values, dtype=np.float32)

    emdd_mean_values = np.array(emdd_mean_values, dtype=np.float32)
    emdd_low_values = np.array(emdd_low_values, dtype=np.float32)
    emdd_upper_values = np.array(emdd_upper_values, dtype=np.float32)

    q_batch_mean.append(q_mean_values)
    q_batch_low.append(q_low_values)
    q_batch_upper.append(q_upper_values)

    emdd_batch_mean.append(emdd_mean_values)
    emdd_batch_low.append(emdd_low_values)
    emdd_batch_upper.append(emdd_upper_values)

    sarsa_batch_mean.append(sarsa_mean_values)
    sarsa_batch_low.append(sarsa_low_values)
    sarsa_batch_upper.append(sarsa_upper_values)

q_mean_values = np.array(q_batch_mean, dtype=np.float32).mean(axis=0)
q_low_values = np.array(q_batch_low , dtype=np.float32).mean(axis=0)
q_upper_values = np.array(q_batch_upper, dtype=np.float32).mean(axis=0)

emdd_mean_values = np.array(emdd_batch_mean, dtype=np.float32).mean(axis=0)
emdd_low_values = np.array(emdd_batch_low, dtype=np.float32).mean(axis=0)
emdd_upper_values = np.array(emdd_batch_upper, dtype=np.float32).mean(axis=0)


print("\n\nEqual\nEMDD")
print(emdd_mean_values)
print("\nEMDD upper")
print(upper_emdd)

x = range(start_episode, 56)
fig, ax = plt.subplots()
ax.plot(x, q_mean_values, label="QAgent", color="blue")
ax.plot(x, emdd_mean_values, label="Options+EMDD-RLAgent", color="#ff8800")
ax.plot(x, sarsa_mean_values, label="SarsaAgent", color="red")





ax.fill_between(x, q_low_values, q_upper_values ,alpha=0.2,color="blue")
ax.fill_between(x, emdd_low_values, emdd_upper_values ,alpha=0.2, color="#ff8800")
ax.fill_between(x, sarsa_low_values, sarsa_upper_values, alpha=0.2, color="green")

plt.xlabel('Episode Number')
plt.ylabel('Step Count')


print("Option episodes : ", option_episodes, min(option_episodes), max(option_episodes))

ax.legend()
print("STD val : ")
print(q_std_deviation)
plt.savefig("utility.png")
plt.show()



exit()








# Normal graphing...


x = range(1, len(mean_values)+1)
fig, ax = plt.subplots()
ax.plot(x, mean_values, label="QAgent", color="blue")
ax.plot(x, emdd_mean_values, label="EMDDQAgent", color="red")

ax.fill_between(x, mean_values-std_deviation, mean_values+std_deviation ,alpha=0.2,color="blue")
ax.fill_between(x, emdd_mean_values-emdd_std_deviation, emdd_mean_values+emdd_std_deviation ,alpha=0.2, color="red")



print("Option episodes : ", option_episodes, min(option_episodes), max(option_episodes))

ax.legend()
print("STD val : ")
print(std_deviation)
plt.show()

