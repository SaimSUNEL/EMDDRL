from tworoomsenvironment1x import TwoRoomsEnvironment1X

import pygame

GOAL_STATE = 309
environment = TwoRoomsEnvironment1X(**{'free_travelling_reward': 0.0,
                                                                               'goal_reward': {GOAL_STATE: 1.0}, 'terminal_states': [GOAL_STATE]})
ground_truth_for_subgoals =  [106,107,109,110,
                             137,138,139,140,141,
                             168,169,170,171,172,
                             199,200,202,203]

eliminated_states = [212, 213, 214, 215, 216,
                     243, 244, 245, 246, 247,
                     274, 275, 276, 277, 278,
                     305, 306, 307, 308]

expected_locations = {}
for s in ground_truth_for_subgoals:
    expected_locations[s] = (255, 102, 0)


for s in eliminated_states:
    expected_locations[s] = (0, 0, 255)

environment.setColorData(expected_locations)
environment.setEnableColorState(True)
environment.reset()
environment.render()
environment.saveEnvironmentImage("../../../EnvironmentImages/"+"tworoom1X"+".png")
input()