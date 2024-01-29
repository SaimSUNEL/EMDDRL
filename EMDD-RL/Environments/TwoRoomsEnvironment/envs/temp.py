from tworoomsenvironmentv2 import TwoRoomsEnvironmentV2

import pygame

GOAL_STATE = 209
environment = TwoRoomsEnvironmentV2(**{'free_travelling_reward': 0.0,
                                                                               'goal_reward': {209: 1.0}, 'terminal_states': [209]})
ground_truth_for_subgoals = [71, 72,74,75,
                             92, 93, 94, 95, 96,
                             113, 114, 115, 116, 117,
                             134,135, 137, 138]

eliminated_states = [188, 187, 208, 207, 186, 165, 166, 167, 206, 186, 164, 143, 144, 145, 146, 205, 184, 185,
                     163, 142, 143, 144, 145, 146]

expected_locations = {}
for s in ground_truth_for_subgoals:
    expected_locations[s] = (255, 255, 0)


for s in eliminated_states:
    expected_locations[s] = (0, 0, 255)

environment.setColorData(expected_locations)
environment.setEnableColorState(True)
environment.reset()
environment.render()
environment.saveEnvironmentImage("../../../EnvironmentImages/"+"tworoom"+".png")
input()