from keyroomenvironmentv2 import KeyRoomEnvironmentV2

import pygame

environment = KeyRoomEnvironmentV2(**{'free_travelling_reward': -0.001, 'goal_reward': {38: 5.0}, 'terminal_states': [38], "key state": 4})
# environment = SampleEnvironmentV1(**{'free_travelling_reward': 0.0, 'goal_reward': {GOAL_STATE: 1.0}, 'terminal_states': [GOAL_STATE]})
ground_truth_for_subgoals = []

expected_locations = {}
for s in ground_truth_for_subgoals:
    expected_locations[s] = (255, 255, 0)# orange -> (255, 102, 0)

eliminated_states = [31,32,37,38]

# for s in eliminated_states:
#    expected_locations[s] = (0, 0, 255)

environment.setColorData(expected_locations)
environment.setEnableColorState(True)
environment.reset()
environment.render()
environment.saveEnvironmentImage("../../../EnvironmentImages/"+"keyv2forpaper"+".png")

input()