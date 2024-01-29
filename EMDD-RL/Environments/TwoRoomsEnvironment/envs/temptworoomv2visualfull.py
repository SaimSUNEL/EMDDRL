import torch
import math
import numpy as np
import torch.nn as nn

import pyautogui
import cv2
import time
from Environments import RLTwoRoomsEnvironment

# 100 for POMDP, 200 for MDP
two_rooms_visual = RLTwoRoomsEnvironment.RLTwoRoomsEnvironment('v200', is_step_restricted=True, step_limit=500)

two_rooms_visual.reset()
current_state = two_rooms_visual.getCurrentState()

print("State vector size : ", current_state.shape[0]*current_state.shape[1])
# 83 -> right key
# 81 -> left  key
# 82 -> up    key
# 84 -> down  key
# 27 -> esc
while True:
    cv2.imshow("State", current_state)
    two_rooms_visual.renderEnvironment()
    key = cv2.waitKey(0)
    # actions
    # self.UP = 3
    # self.LEFT = 0
    # self.RIGHT = 2
    # self.DOWN = 1
    # self.FORWARD = 4
    if key == 83:
        current_state, reward = two_rooms_visual.applyAction(2)
    if key == 81:
        current_state, reward = two_rooms_visual.applyAction(0)
    if key == 82:
        current_state, reward = two_rooms_visual.applyAction(3)
    if key == 84:
        current_state, reward = two_rooms_visual.applyAction(1)

    if key == 27:
        break
exit()