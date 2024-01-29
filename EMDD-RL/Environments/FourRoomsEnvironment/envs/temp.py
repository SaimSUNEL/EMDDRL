from fourroomsenvironment import FourRoomsEnvironment

import pygame

GOAL_STATE = 209
environment = FourRoomsEnvironment(**{'free_travelling_reward': 0.0,
                                                                               'goal_reward': {226: 1.0}, 'terminal_states': [226]})
ground_truth_for_subgoals = [71,72,74,75,
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

eliminated_states = [183,184, 185,
                     204,205,206,
                     246, 247, 248,
                     267,268,269]

expected_locations = {}
for s in ground_truth_for_subgoals:
    expected_locations[s] = (255, 255, 0) # (255, 102, 0)


for s in eliminated_states:
    expected_locations[s] = (0, 0, 255)

environment.setColorData(expected_locations)
environment.setEnableColorState(True)
environment.reset()
environment.render()
environment.saveEnvironmentImage("../../../EnvironmentImages/"+"fourroom"+".png")
input()