from gym.envs.registration import register

register(id='FourRoomsEnvironment-v0',
         entry_point='Environments.FourRoomsEnvironment.envs:FourRoomsEnvironment', kwargs = {'free_travelling_reward': 0.0,
                                                                               'goal_reward': {226: 1.0}, 'terminal_states': [226]}
         )

print("Four rooms has been registered...")
