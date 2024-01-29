import Mediator
import gym
import numpy as np
from Environments import RLTwoRoomsEnvironment, RLFourRoomsEnvironment, RLZigzagEnvironment, RLTrapEnvironment, RLKeyRoomEnvironment
from Environments import RLPOMDPTwoRoomsEnvironment, RLPOMDPFourRoomsEnvironment
from Environments import RLSampleEnvironment
from Environments import RLDDEnvironment

from Agents import RLEMDDWithOptionQAgent, RLQAgent, RLSarsaAgent, \
    RLEMDDWithOptionQAgent, RLPOMDPFixedMemoryQAgent, RLPOMDPFixedMemorySarsaAgent, RLPOMDPFixedMemorySarsaLamdaAgent
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

zigzag_room_env = RLZigzagEnvironment.RLZigzagEnvironment("v0",is_step_restricted=True, step_limit=1000)
sample_room_env_v0 = RLSampleEnvironment.RLSampleEnvironment("v0", is_step_restricted=True, step_limit=50)
sample_room_env_v1 = RLSampleEnvironment.RLSampleEnvironment("v1", is_step_restricted=True, step_limit=50)
dd_room_env_v0 = RLDDEnvironment.RLDDEnvironment("v0", is_step_restricted=True, step_limit=100)
trap_room_env_v0 = RLTrapEnvironment.RLTrapEnvironment("v0", is_step_restricted=True, step_limit=200)
trap_room_env_v1 = RLTrapEnvironment.RLTrapEnvironment("v1", is_step_restricted=False, step_limit=200)
key_room_env = RLKeyRoomEnvironment.RLKeyRoomEnvironment("v0", is_step_restricted=False, step_limit=50)
key_room_env_v1 = RLKeyRoomEnvironment.RLKeyRoomEnvironment("v1", is_step_restricted=False, step_limit=50)
key_room_env_v2 = RLKeyRoomEnvironment.RLKeyRoomEnvironment("v2", is_step_restricted=False, step_limit=50)




pomdp_two_rooms_env = RLPOMDPTwoRoomsEnvironment.RLPOMDPTwoRoomsEnvironment('v1', is_step_restricted=False, step_limit=100)
pomdp_two_rooms_env_2 = RLPOMDPTwoRoomsEnvironment.RLPOMDPTwoRoomsEnvironment('v2', is_step_restricted=False, step_limit=400)
pomdp_two_rooms_env_3 = RLPOMDPTwoRoomsEnvironment.RLPOMDPTwoRoomsEnvironment('v3', is_step_restricted=False, step_limit=400)


pomdp_four_rooms_env_3 = RLPOMDPFourRoomsEnvironment.RLPOMDPFourRoomsEnvironment('v3', is_step_restricted=False, step_limit=800)
pomdp_four_rooms_env_4 = RLPOMDPFourRoomsEnvironment.RLPOMDPFourRoomsEnvironment('v4', is_step_restricted=True, step_limit=800)

# pomdp_two_rooms_env.renderEnvironment()
print(pomdp_two_rooms_env.environment.getObservation(4))

environment = key_room_env_v2 # key_room_env_v1 # trap_room_env_v1 # two_rooms_env_v2 # dd_room_env_v0 # zigzag_room_env # sample_room_env_v0 # zigzag_room_env # pomdp_four_rooms_env_4 # pomdp_four_rooms_env_3

# agent stores the trajectories in a file...
q_agent = RLQAgent.RLQAgent(environment, 0.05, 0.1, 0.9, saveTrajectory=True, trajectoryFileName="KeyRoomV2", fileNumber=fileCount)
# sarsa_agent = RLSarsaAgent.RLSarsaAgent(environment, 0.05, 0.1, 0.9, saveTrajectory=True, trajectoryFileName="SarsaTwoRoom", fileNumber=fileCount) #
# dd_agent = RLEMDDWithOptionQAgent.RLDiverseDensityWithOptionQAgent(environment, 0.1, 0.1, 0.95)
emdd_agent = RLEMDDWithOptionQAgent.RLEMDDWithOptionQAgent(environment, 0.1, 0.1, 0.95)

#pomdp_fixed_memory_q_agent = RLPOMDPFixedMemoryQAgent.RLPOMDPFixedMemoryQAgent(environment, 0.05, 0.1, 0.9, saveTrajectory=True, trajectoryFileName="POMDPFourRoomsv4", fixed_memory_structure={'O':[0, -1, -2], 'A': [0, -1]})
#pomdp_fixed_memory_sarsa_agent = RLPOMDPFixedMemorySarsaAgent.RLPOMDPFixedMemorySarsaAgent(environment, 0.05, 0.1, 0.9, saveTrajectory=False, trajectoryFileName="POMDPTwoRooms", fixed_memory_structure={'O':[0, -1], 'A': [0]})
#pomdp_fixed_memory_sarsa_lambda_agent = RLPOMDPFixedMemorySarsaLamdaAgent.RLPOMDPFixedMemorySarsaLamdaAgent(environment, 0.1, 0.1, 0.95, trace_factor=0.35, saveTrajectory=False, trajectoryFileName="", fixed_memory_structure={'O':[0, -1, -2, -3 ,-4, -5, -6], 'A': [0]})

agent = q_agent # q_agent # pomdp_fixed_memory_q_agent
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

