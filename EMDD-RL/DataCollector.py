import Mediator
import gym
import numpy as np
from Environments import RLTwoRoomsEnvironment, RLFourRoomsEnvironment, RLKeyRoomEnvironment

from Agents import RLEMDDWithOptionQAgent, RLQAgent, RLSarsaAgent, \
    RLEMDDWithOptionQAgent
import sys
if len(sys.argv) > 1:
    fileCount = int(sys.argv[1])
else:
    fileCount = -1



env = gym.make('CartPole-v0').env
state = env.reset()
print(env.observation_space)
print(env.action_space)
print(env.observation_space.high)
print(env.observation_space.low)
print(state)

four_rooms_env = RLFourRoomsEnvironment.RLFourRoomsEnvironment(is_step_restricted=True, step_limit=100)
two_rooms_env_v2 = RLTwoRoomsEnvironment.RLTwoRoomsEnvironment('v2', is_step_restricted=False, step_limit=200)
two_rooms_env_v3 = RLTwoRoomsEnvironment.RLTwoRoomsEnvironment('v3', is_step_restricted=True, step_limit=1200)
two_rooms_env_v4 = RLTwoRoomsEnvironment.RLTwoRoomsEnvironment('v4', is_step_restricted=True, step_limit=1200)

two_rooms_env_1x = RLTwoRoomsEnvironment.RLTwoRoomsEnvironment('v6', is_step_restricted=True, step_limit=300)
two_rooms_env_2x = RLTwoRoomsEnvironment.RLTwoRoomsEnvironment('v7', is_step_restricted=False, step_limit=400)
two_rooms_env_3x = RLTwoRoomsEnvironment.RLTwoRoomsEnvironment('v8', is_step_restricted=False, step_limit=500)
two_rooms_env_4x = RLTwoRoomsEnvironment.RLTwoRoomsEnvironment('v9', is_step_restricted=True, step_limit=600)
two_rooms_env_5x = RLTwoRoomsEnvironment.RLTwoRoomsEnvironment('v10', is_step_restricted=True, step_limit=700)

key_room_env = RLKeyRoomEnvironment.RLKeyRoomEnvironment("v0", is_step_restricted=False, step_limit=50)
key_room_env_v1 = RLKeyRoomEnvironment.RLKeyRoomEnvironment("v1", is_step_restricted=False, step_limit=50)
key_room_env_v2 = RLKeyRoomEnvironment.RLKeyRoomEnvironment("v2", is_step_restricted=False, step_limit=50)




environment = key_room_env_v2 

# agent stores the trajectories in a file...
q_agent = RLQAgent.RLQAgent(environment, 0.05, 0.1, 0.9, saveTrajectory=True, trajectoryFileName="KeyRoomV2", fileNumber=fileCount)
# sarsa_agent = RLSarsaAgent.RLSarsaAgent(environment, 0.05, 0.1, 0.9, saveTrajectory=True, trajectoryFileName="SarsaTwoRoom", fileNumber=fileCount) #
# dd_agent = RLEMDDWithOptionQAgent.RLDiverseDensityWithOptionQAgent(environment, 0.1, 0.1, 0.95)
emdd_agent = RLEMDDWithOptionQAgent.RLEMDDWithOptionQAgent(environment, 0.1, 0.1, 0.95)

agent = q_agent # q_agent
mediator = Mediator.Mediator(agent, environment, 1000, render_learning=False)
mediator.experiment()

# print(agent.getVisualPolicy())
# agent.plotStepPerEpisode()
# agent.plotConvergence()
print("\n\n")
# agent.renderAgent()
# print(agent.getQTable())
print(len(agent.getQTable()))
for a in range(len(agent.getQTable())):
    pass
    #print(a, ": ", agent.getQTable()[a])
# raw_input()
if environment.getEnvironmentType() == environment.RLENVIRONMENT_DISCRETE and len(environment.getStateSpaceDimensions()) == 1:
    #print(agent.getVisualPolicy())
    pass

