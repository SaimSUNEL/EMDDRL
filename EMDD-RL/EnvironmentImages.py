
import os
import time

from Environments import RLTwoRoomsEnvironment
from MIL.Methods.DD import DiverseDensity
from MIL.Methods.EMDD import EMDD
import sys
from Environments import RLFourRoomsEnvironment
from Environments import RLZigzagEnvironment



name = ""
# two_rooms_env_v2 = RLTwoRoomsEnvironment.RLTwoRoomsEnvironment('v10', is_step_restricted=True, step_limit=500)
# two_rooms_env_v2.renderEnvironment()
# two_rooms_env_v2.saveEnvironmentImage("EnvironmentImages/tworoom710.png")
# four_rooms = RLFourRoomsEnvironment.RLFourRoomsEnvironment('v2', is_step_restricted=True, step_limit=500)
# four_rooms.renderEnvironment()
# four_rooms.saveEnvironmentImage("EnvironmentImages/fourroomoriginal.png")
zigzag = RLZigzagEnvironment.RLZigzagEnvironment('v0', is_step_restricted=True, step_limit=500)
zigzag.renderEnvironment()
zigzag.saveEnvironmentImage("EnvironmentImages/zigzag.png")
input()


