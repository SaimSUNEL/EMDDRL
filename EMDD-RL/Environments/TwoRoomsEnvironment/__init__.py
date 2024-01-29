from gym.envs.registration import register


register(id='TwoRoomsEnvironment-v0',
         entry_point='Environments.TwoRoomsEnvironment.envs:TwoRoomsEnvironment', kwargs = {'free_travelling_reward': 0.0,
                                                                               'goal_reward': {209: 1.0}, 'terminal_states': [209]}
         )
register(id='TwoRoomsEnvironment-v2',
         entry_point='Environments.TwoRoomsEnvironment.envs:TwoRoomsEnvironmentV2', kwargs = {'free_travelling_reward': 0.0,
                                                                               'goal_reward': {209: 1.0}, 'terminal_states': [209]}
         )

register(id='TwoRoomsEnvironment-v3',
         entry_point='Environments.TwoRoomsEnvironment.envs:TwoRoomsEnvironmentOnLeft', kwargs = {'free_travelling_reward': 0.0,
                                                                               'goal_reward': {409: 1.0}, 'terminal_states': [409]}
         )

register(id='TwoRoomsEnvironment-v4',
         entry_point='Environments.TwoRoomsEnvironment.envs:TwoRoomsEnvironmentOnRight', kwargs = {'free_travelling_reward': 0.0,
                                                                               'goal_reward': {409: 1.0}, 'terminal_states': [409]}
         )

register(id='TwoRoomsEnvironment-v6',
         entry_point='Environments.TwoRoomsEnvironment.envs:TwoRoomsEnvironment1X', kwargs = {'free_travelling_reward': 0.0,
                                                                               'goal_reward': {309: 1.0}, 'terminal_states': [309]}
         )

register(id='TwoRoomsEnvironment-v7',
         entry_point='Environments.TwoRoomsEnvironment.envs:TwoRoomsEnvironment2X', kwargs = {'free_travelling_reward': 0.0,
                                                                               'goal_reward': {409: 1.0}, 'terminal_states': [409]}
         )

register(id='TwoRoomsEnvironment-v8',
         entry_point='Environments.TwoRoomsEnvironment.envs:TwoRoomsEnvironment3X', kwargs = {'free_travelling_reward': 0.0,
                                                                               'goal_reward': {509: 1.0}, 'terminal_states': [509]}
         )

register(id='TwoRoomsEnvironment-v9',
         entry_point='Environments.TwoRoomsEnvironment.envs:TwoRoomsEnvironment4X', kwargs = {'free_travelling_reward': 0.0,
                                                                               'goal_reward': {609: 1.0}, 'terminal_states': [609]}
         )

register(id='TwoRoomsEnvironment-v10',
         entry_point='Environments.TwoRoomsEnvironment.envs:TwoRoomsEnvironment5X', kwargs = {'free_travelling_reward': 0.0,
                                                                               'goal_reward': {709: 1.0}, 'terminal_states': [709]}
         )
register(id='TwoRoomsEnvironment-v200',
         entry_point='Environments.TwoRoomsEnvironment.envs:TwoRoomsEnvironmentV2VisualFull', kwargs = {'free_travelling_reward': 0.0,
                                                                               'goal_reward': {209: 1.0}, 'terminal_states': [209]}
         )
print("Two rooms v0 has been registered...")
print("Two rooms v2 has been registered...")
