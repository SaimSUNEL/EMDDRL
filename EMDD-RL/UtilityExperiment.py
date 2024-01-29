import Mediator
from Agents import RLEMDDWithOptionQAgent, RLQAgent, RLSarsaAgent
from Environments import RLTwoRoomsEnvironment, RLFourRoomsEnvironment

four_rooms_env = RLFourRoomsEnvironment.RLFourRoomsEnvironment(is_step_restricted=False, step_limit=400)
two_rooms_env_v2 = RLTwoRoomsEnvironment.RLTwoRoomsEnvironment('v2', is_step_restricted=False, step_limit=200)

environment = two_rooms_env_v2

# agent agent stores the trajectories in a file...
q_agent = RLQAgent.RLQAgent(environment, 0.05, 0.1, 0.9, saveTrajectory=False, trajectoryFileName="")
sarsa_agent = RLSarsaAgent.RLSarsaAgent(environment, 0.05, 0.1, 0.9, saveTrajectory=False, trajectoryFileName="")
# dd_agent = RLEMDDWithOptionQAgent.RLDiverseDensityWithOptionQAgent(environment, 0.1, 0.1, 0.95)
emdd_agent = RLEMDDWithOptionQAgent.RLEMDDWithOptionQAgent(environment, 0.1, 0.1, 0.95)
agent = sarsa_agent # q_agent


mediator = Mediator.Mediator(agent, environment, 120, render_learning = False)
mediator.experiment()

#agent.plotConvergence()
#agent.plotAccumulatedReward()
#agent.plotStepPerEpisode()

step_array = agent.getStepPerEpisode()
reward_array = agent.getRewardPerEpisode()

print("Step array \n")
print(step_array)
print("Reward array")
print(reward_array)

agent_name = "Sarsa" # "EMDDQAgent"
environment_name = "TwoRooms"
import os


if not agent_name in os.listdir("UtilityExperiments"):
    os.mkdir("UtilityExperiments/"+agent_name)
if not environment_name in os.listdir("UtilityExperiments/"+agent_name):
    os.mkdir("UtilityExperiments/"+agent_name+"/"+environment_name)

previous_files = os.listdir("UtilityExperiments/"+agent_name+"/"+environment_name)

file_number = 1
current_file = agent_name+environment_name+"["+str(file_number)+"].txt"
while current_file in previous_files:
    file_number += 1
    current_file = agent_name + environment_name + "[" + str(file_number) + "].txt"

file_path = "UtilityExperiments/"+agent_name+"/"+environment_name+"/"
file_path += current_file
dosya = open(file_path, "w")
dosya.write(str(reward_array))
dosya.write("\n")
dosya.write(str(step_array)+"\n")
# dosya.write(str(agent.subgoals)+"\n")
# dosya.write(str(agent.option_creation_history))
dosya.close()






