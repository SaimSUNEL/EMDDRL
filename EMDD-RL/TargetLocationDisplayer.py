from Environments import RLFourRoomsEnvironment, RLPOMDPFourRoomsEnvironment
from Environments import RLTwoRoomsEnvironment, RLPOMDPTwoRoomsEnvironment

# candidate states for subgoals...
ground_truth_for_subgoals_fourrooms = [71,72,74,75,
                             92,93,94,95,96,
                             113, 114, 116, 117,

                             171,172,173,
                             192,193,194,
                                       214,
                             234, 235, 236,
                             255, 256, 257,

                             302,303,305,306,
                             323,324,325,326,327,
                             344,345,347,348,

                             # aroun goal state
                             161,162,163,164,165,
                             182,186,
                             203,207,

                             245,249,
                             266,270,
                             287,288,289,290,291

                             ]

ground_truth_for_subgoals_tworooms = [71, 72,74,75,
                             92, 93, 94, 95, 96,
                             113, 114, 115, 116, 117,
                             134,135, 137, 138]

pomdp_two_v3_ground_truth_for_subgoals = [(1,3),(0,3),
                             (8,4),(9,4),(10,0)]

pomdp_two_rooms_env_v3 = RLPOMDPTwoRoomsEnvironment.RLPOMDPTwoRoomsEnvironment('v3', is_step_restricted=True, step_limit=500)

four_rooms = RLFourRoomsEnvironment.RLFourRoomsEnvironment('v2', is_step_restricted=True, step_limit=500)
two_rooms_env_v2 = RLTwoRoomsEnvironment.RLTwoRoomsEnvironment('v2', is_step_restricted=True, step_limit=500)



pomdp_four_v3_ground_truth_for_subgoals = [(1,3),(0,3),
                             (8,4), (9,4),(10,0), (1, 4), (0, 4), (13, 12), (14, 12), (14, 17), (13, 12), (12, 12)]
pomdp_four_rooms_env_v3 = RLPOMDPFourRoomsEnvironment.RLPOMDPFourRoomsEnvironment('v3', is_step_restricted=True, step_limit=500)


# candidate states for subgoals...
pomdp_four_v4_ground_truth_for_subgoals = [(1,3),(0,3),
                             (8,4), (9,4),(10,0), (1, 4), (0, 4), (13, 12), (14, 12), (14, 17), (13, 12), (12, 12),
                                           (20, 0)]

pomdp_four_rooms_env_v4 = RLPOMDPFourRoomsEnvironment.RLPOMDPFourRoomsEnvironment('v4', is_step_restricted=True, step_limit=500)


four_rooms_color_info = {}
two_rooms_color_info = {}

pomdp_two_rooms_v3_color_info  = {}
pomdp_four_rooms_v3_color_info = {}
pomdp_four_rooms_v4_color_info = {}

for state in ground_truth_for_subgoals_fourrooms:
    four_rooms_color_info[state] = (250, 250, 0)

for state in ground_truth_for_subgoals_tworooms:
    two_rooms_color_info[state] = (250, 250, 0)

for state in pomdp_two_v3_ground_truth_for_subgoals:
    pomdp_two_rooms_v3_color_info[state] = (250, 250, 0)

for state in pomdp_four_v3_ground_truth_for_subgoals:
    pomdp_four_rooms_v3_color_info[state] = (250, 250, 0)

for state in pomdp_four_v4_ground_truth_for_subgoals:
    pomdp_four_rooms_v4_color_info[state] = (250, 250, 0)

two_rooms_env_v2.setColorData(two_rooms_color_info)
two_rooms_env_v2.setEnableColorState(True)

four_rooms.setColorData(four_rooms_color_info)
four_rooms.setEnableColorState(True)

pomdp_two_rooms_env_v3.setColorData(pomdp_two_rooms_v3_color_info)
pomdp_two_rooms_env_v3.setEnableColorState(True)
pomdp_two_rooms_env_v3.renderEnvironment()
pomdp_two_rooms_env_v3.saveEnvironmentImage("POMDPTWOROOMSV3.png")

pomdp_four_rooms_env_v3.setColorData(pomdp_four_rooms_v3_color_info)
pomdp_four_rooms_env_v3.setEnableColorState(True)
pomdp_four_rooms_env_v3.renderEnvironment()
pomdp_four_rooms_env_v3.saveEnvironmentImage("POMDPFOURROOMSV3.png")


pomdp_four_rooms_env_v4.setColorData(pomdp_four_rooms_v4_color_info)
pomdp_four_rooms_env_v4.setEnableColorState(True)
pomdp_four_rooms_env_v4.renderEnvironment()
pomdp_four_rooms_env_v4.saveEnvironmentImage("POMDPFOURROOMSV4.png")




two_rooms_env_v2.renderEnvironment()
two_rooms_env_v2.saveEnvironmentImage("tworoomstarget.png")

four_rooms.renderEnvironment()
four_rooms.saveEnvironmentImage("fourroomstarget.png")



raw_input()