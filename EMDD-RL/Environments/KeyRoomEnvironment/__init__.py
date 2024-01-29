from gym.envs.registration import register

GOAL_STATE = 103
register(id='KeyRoomEnvironment-v0',
         entry_point='Environments.KeyRoomEnvironment.envs:KeyRoomEnvironmentV0', kwargs = {'free_travelling_reward': -0.001, 'goal_reward': {GOAL_STATE: 1.0}, 'terminal_states': [GOAL_STATE], "key state": 7}
         )
register(id='KeyRoomEnvironment-v1',
         entry_point='Environments.KeyRoomEnvironment.envs:KeyRoomEnvironmentV1', kwargs = {'free_travelling_reward': -0.1, 'goal_reward': {38: 5.0}, 'terminal_states': [38], "key state": 4}
         )
register(id='KeyRoomEnvironment-v2',
         entry_point='Environments.KeyRoomEnvironment.envs:KeyRoomEnvironmentV2', kwargs = {'free_travelling_reward': -0.1, 'goal_reward': {38: 5.0}, 'terminal_states': [38], "key state": 4}
         )
print("KeyRoom v0 has been registered...")
print("KeyRoom v1 has been registered...")
print("KeyRoom v2 has been registered...")
