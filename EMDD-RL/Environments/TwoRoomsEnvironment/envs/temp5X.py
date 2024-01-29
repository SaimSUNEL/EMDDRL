from tworoomsenvironment5x import TwoRoomsEnvironment5X

import pygame

GOAL_STATE = 709
environment = TwoRoomsEnvironment5X(**{'free_travelling_reward': 0.0,
                                                                               'goal_reward': {GOAL_STATE: 1.0}, 'terminal_states': [GOAL_STATE]})
ground_truth_for_subgoals =  [246,247,249,250,
                             317,318,319,320,321,
                             388,389,390,391,392,
                             459,460,462,463
                             ]

eliminated_states = [492,493,494,495,496,
                     563,564,565,566,567,
                     634,635,636,637,638,
                     705,706,707,708
                     ]

expected_locations = {}
for s in ground_truth_for_subgoals:
    expected_locations[s] = (255, 255, 0)


for s in eliminated_states:
    expected_locations[s] = (0, 0, 255)

environment.setColorData(expected_locations)
environment.setEnableColorState(True)
environment.reset()
environment.render()
environment.saveEnvironmentImage("../../../EnvironmentImages/"+"tworoom5X"+".png")
input()