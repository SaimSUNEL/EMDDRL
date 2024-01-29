from keyroomenvironment import KeyRoomEnvironmentV0

import pygame

GOAL_STATE = 103
environment = KeyRoomEnvironmentV0(**{'free_travelling_reward': -0.001, 'goal_reward': {GOAL_STATE: 1.0}, 'terminal_states': [GOAL_STATE], "key state": 7})
# environment = SampleEnvironmentV1(**{'free_travelling_reward': 0.0, 'goal_reward': {GOAL_STATE: 1.0}, 'terminal_states': [GOAL_STATE]})
ground_truth_for_subgoals = []

expected_locations = {}
for s in ground_truth_for_subgoals:
    expected_locations[s] = (255, 255, 0)# orange -> (255, 102, 0)

eliminated_states = [91, 92, 102,80,81,90,101]

# for s in eliminated_states:
#    expected_locations[s] = (0, 0, 255)

environment.setColorData(expected_locations)
environment.setEnableColorState(True)
environment.reset()
environment.render()
environment.saveEnvironmentImage("../../../EnvironmentImages/"+"keyv0forpaper"+".png")

input()