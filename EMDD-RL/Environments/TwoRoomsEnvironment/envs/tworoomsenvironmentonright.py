import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

import pygame

class TwoRoomsEnvironmentOnRight(gym.Env):
    metadata = {'render.modes': ['human']}
    def __init__(self, **karguments):
        """
            And set the following attributes:
        action_space: The Space object corresponding to valid actions
        observation_space: The Space object corresponding to valid observations
        reward_range: A tuple corresponding to the min and max possible rewards
    Note: a default reward range set to [-inf,+inf] already exists. Set it if you want a narrower range.
        """
        # for each non-goal state the reward is -0.000001
        spec = None

        self.tile_width = 25  # px
        self.tile_height = 25  # px

        self.row_tile_count = 41  # number of tiles in a row...
        self.column_tile_count = 10  # number of tiles in a column

        self.screen_width = 1235
        self.screen_height = 310




        # Set these in ALL subclasses
        # Four actions, forward, left, right, down
        # 2/3 intended 1/9 for other directions...
        self.action_space = spaces.Discrete(4)


        # reward that is received when agent travels a non goal states...
        # papers might define same enviroment with different reward and goal states....

        self.free_travelling_reward = karguments["free_travelling_reward"]

        # Some goal states might produce negative reward, it will be a dictionary {state: reward}
        self.goal_reward = karguments["goal_reward"]

        minimum_reward = min(self.goal_reward.values())
        max_reward = max(self.goal_reward.values())

        minimum_reward = min(self.free_travelling_reward, minimum_reward)
        max_reward = max(self.free_travelling_reward, max_reward)


        print("minimum reward "+str(minimum_reward)+ " max reward "+str(max_reward))

        # self.reward_range = (-0.000001, 1.0)
        self.reward_range= (minimum_reward, max_reward)


        self.observation_space = spaces.Discrete(self.row_tile_count*self.column_tile_count)

        # some configs require no goal states to collect some statistic for the environment
        # RN (Simsek) example
        self.terminal_states = karguments["terminal_states"] # [209] # goal and unwanted states that delivers negative reward...
        self.unused_states = [] # walls...

        # actions
        self.UP = 3
        self.LEFT = 0
        self.RIGHT = 2
        self.DOWN = 1
        self.FORWARD = 4

        self.action_set = [self.LEFT, self.DOWN, self.RIGHT, self.UP]
        self.action_symbol = ['<', 'v', '>', '^']

        # 0.9 in intended direction, 0.1 uniform any direction
        self.action_probabilities = [0.9, 0.1]

        self.states = np.zeros((self.column_tile_count * self.row_tile_count), dtype=np.int32)
        for i in range(self.column_tile_count * self.row_tile_count):
            self.states[i] = 0

        self.states = self.states.reshape((self.column_tile_count, self.row_tile_count))

        # agent can start in west room in any state
        self.starting_state = []
        for x_ in range(0, 10):
            for y_ in range(10):
                self.starting_state.append(x_+ y_*self.row_tile_count)

        # to keep track of the agent...
        self.environment_current_state = None


        # only when agent reaches the goal then it receives the reward...
        self.reward = 1.0
        self.forward_probability = 0.9 # 0.9
        self.WINDOW_SIZE = [self.screen_width, self.screen_height]


        # 0 empty state , 1 goal state, 2 wall
        for y in range(self.column_tile_count):
            for x in [30]:
                self.unused_states.append(y*self.row_tile_count+x)
                self.states[y][x] = 2

        self.states[4][30] = 0
        self.unused_states.remove(4*self.row_tile_count+30)

        self.states[5][30] = 0
        self.unused_states.remove(5 * self.row_tile_count + 30)

        for h in self.terminal_states:
            y = h // self.row_tile_count
            x = h % self.row_tile_count
            self.states[y][x] = 1

        self.is_window_created = False

        self.display_policy = False
        self.policy_to_display = None
        # print(self.states[0])

        self.diplay_value = False
        self.value_to_display = None

        self.display_subgoal = False
        self.subgoal_to_display = None

        self.display_options = False
        self.options_to_display = None

        self.display_segments = False
        self.segments_to_display = None

        self.path_display = False
        self.path_data = []
        # state: (x, y, w, h)
        self.state_coordinate_data = {}

        self.relation_display = False
        self.relation_data = []
        self.relation_color_data = {}

        self.color_states = False
        self.color_data = {}


    def setEnableColorState(self, val):
        self.color_states = val
    # state: color
    def setColorData(self, dictionary):
        self.color_data = dictionary

    def setEnableRelationDisplay(self, val):
        self.relation_display = val

        # color  = {local peak: color1, local_peak2: color2 ....}

    def setRelationData(self, data, color={}):
        self.relation_data = data
        self.relation_color_data = color

    def setEnablePathDisplay(self, val):
        self.path_display = val

    def setPathData(self, instance_bag, color=(0, 0, 150)):
        self.path_data = instance_bag

    def setEnableSegmentDisplay(self, val):
        self.display_segments = val

    def setDisplaySegment(self, val):
        self.segments_to_display = val

    def getStartingStates(self):
        return self.starting_state

    def getGoalState(self):
        return self.terminal_states

    def setEnableOptionDisplay(self, val):
        self.display_options = val

    def setDisplayOption(self, init_set):
        self.options_to_display = init_set
    def setEnablePolicyDisplay(self, val):
        self.display_policy = val
    def setDisplayPolicy(self, policy):
        self.policy_to_display = policy

    def setEnableValueDisplay(self ,val):
        self.display_value = val
    def setDisplayValue(self, value):
        self.value_to_display = value

    def setEnableSubgoalDisplay(self, val):
        self.display_subgoal = val
    def setDisplaySubgoal(self, subgoal):
        self.subgoal_to_display = subgoal

    # it returns only adjancency dictiory of every state
    def getEnvironmentGraph(self):

        adjancency_dict = {}

        for state in range(self.row_tile_count*self.column_tile_count):
            # exclude wall states from graph...
            if state in self.unused_states:
                continue
            adjancency_dict[state] = []

            state_x = state % self.row_tile_count
            state_y = state // self.row_tile_count


            for action in range(4):
                next_state = self.get_next_state_and_reward(state, action)[0]
                if next_state != state:
                    adjancency_dict[state].append(next_state)



        return adjancency_dict



    def get_next_state_and_reward(self, current_state, current_action):
        curr_y = current_state // self.row_tile_count
        curr_x = current_state % self.row_tile_count
        reward = self.free_travelling_reward # if not goal then all zero

        if current_action == self.UP:

            next_state = (curr_y-1)*self.row_tile_count+curr_x
            if next_state in self.unused_states:
                next_state = current_state

            if curr_y - 1 < 0:
                next_state = current_state


            # only when agent reaches the goal then it receives the reward...
            if next_state in self.terminal_states:
                reward = self.goal_reward[next_state]

            return next_state, reward

        if current_action == self.LEFT:

            next_state = (curr_y) * self.row_tile_count + curr_x-1
            if next_state in self.unused_states:
                next_state = current_state

            if curr_x - 1  < 0:
                next_state = current_state

            # only when agent reaches the goal then it receives the reward...
            if next_state in self.terminal_states:
                reward = self.goal_reward[next_state]

            return next_state, reward

        if current_action == self.RIGHT:

            next_state = (curr_y) * self.row_tile_count + curr_x+1
            if next_state in self.unused_states:
                next_state = current_state

            if curr_x + 1  >= self.row_tile_count:
                next_state = current_state

            # only when agent reaches the goal then it receives the reward...
            if next_state in self.terminal_states:
                reward = self.goal_reward[next_state]

            return next_state, reward

        if current_action == self.DOWN:

            next_state = (curr_y+1) * self.row_tile_count + curr_x
            if next_state in self.unused_states:
                next_state = current_state

            if curr_y + 1  >= self.column_tile_count:
                next_state = current_state

            # only when agent reaches the goal then it receives the reward...
            if next_state in self.terminal_states:
                reward = self.goal_reward[next_state]

            return next_state, reward

    def step(self, action):
        """Run one timestep of the environment's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this environment's state.
        Accepts an action and returns a tuple (observation, reward, done, info).
        Args:
            action (object): an action provided by the agent
        Returns:
            observation (object): agent's observation of the current environment
            reward (float) : amount of reward returned after previous action
            done (bool): whether the episode has ended, in which case further step() calls will return undefined results
            info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning)
        """



        real_move = np.random.choice([0, 1],
                                     p=[self.forward_probability, 1.0-self.forward_probability])

        selected_action = action
        if real_move == 0:
            real_move = selected_action
        else:
            actions = [j for j in self.action_set]
            real_move = np.random.choice(actions,
                                     p = [1.0/4.0, 1.0/4.0, 1.0/4.0, 1.0/4.0])

        next_state, reward = self.get_next_state_and_reward(self.environment_current_state, real_move)
        self.environment_current_state = next_state
        done = False
        finished_successfully = False
        if next_state in self.terminal_states:
            if reward > 0: # assumes successfull states emits positive reward...
                self.has_finished_successfully = True
                finished_successfully = True
            done = True
        # every action costs little

        # for observation last part will be used...
        return next_state, reward, done, {"issuccesful": finished_successfully}

    def reset(self):
        """Resets the state of the environment and returns an initial observation.
        Returns:
            observation (object): the initial observation.
        """
        # sample uniformly among
        self.environment_current_state = np.random.choice(self.starting_state)
        return self.environment_current_state


    def render(self, mode='human', close=False):
        """Renders the environment.
                The set of supported modes varies per environment. (And some
                environments do not support rendering at all.) By convention,
                if mode is:
                - human: render to the current display or terminal and
                  return nothing. Usually for human consumption.
                - rgb_array: Return an numpy.ndarray with shape (x, y, 3),
                  representing RGB values for an x-by-y pixel image, suitable
                  for turning into a video.
                - ansi: Return a string (str) or StringIO.StringIO containing a
                  terminal-style text representation. The text can include newlines
                  and ANSI escape sequences (e.g. for colors).
                Note:
                    Make sure that your class's metadata 'render.modes' key includes
                      the list of supported modes. It's recommended to call super()
                      in implementations to use the functionality of this method.
                Args:
                    mode (str): the mode to render with
                Example:
                class MyEnv(Env):
                    metadata = {'render.modes': ['human', 'rgb_array']}
                    def render(self, mode='human'):
                        if mode == 'rgb_array':
                            return np.array(...) # return RGB frame suitable for video
                        elif mode == 'human':
                            ... # pop up a window and render
                        else:
                            super(MyEnv, self).render(mode=mode) # just raise an exception
                """
        if(self.is_window_created == False):
            pygame.init()
            self.screen = pygame.display.set_mode(self.WINDOW_SIZE)

            pygame.display.set_caption("2 Rooms")
            self.screen.fill((0, 0, 0))
            self.is_window_created = True
            self.font = pygame.font.SysFont("comicsansms", 48)
            self.font2 = pygame.font.SysFont("comicsansms", 8)

        MARGIN = 5
        for y in range(self.column_tile_count):
            for x in range(self.row_tile_count):
                coord = [(MARGIN + self.tile_width) * x + MARGIN,
                 (MARGIN + self.tile_height) * y + MARGIN,
                 self.tile_width, self.tile_height]

                s = self.states[y][x]

                state = y*self.row_tile_count+x;
                self.state_coordinate_data[state] = coord

                color = (255, 255, 255)
                # print("Display Subgoal . ", self.display_subgoal)
                if self.display_subgoal == True:
                    if state in self.subgoal_to_display.keys():
                        a = self.subgoal_to_display[state]
                        if a > 255:
                            a = 255

                        if a < 0:
                            a= 0
                        color = (10, a, 10)


                if self.display_segments:
                    for segment in self.segments_to_display.keys():
                        segment_nodes = self.segments_to_display[segment]["graph"].nodes;
                        if state in segment_nodes:
                            color = self.segments_to_display[segment]["color"]

                if self.path_display:
                    if state in self.path_data:
                        color = (200, 0, 0)
                if self.color_states:
                    if state in self.color_data:
                        color = self.color_data[state]

                if s == 2:
                    color = (50, 50, 50)
                elif s == 1:
                    color = (0, 255, 0)

                # print("Color : ", color)
                pygame.draw.rect(self.screen, color, coord)
                text2 = self.font2.render(str(state), True, (0, 0, 0))
                self.screen.blit(text2, ((MARGIN + self.tile_width) * x + MARGIN + 3,
                                         (MARGIN + self.tile_height) * y + MARGIN - 8 + 25))

        if self.relation_display:
            for instance in self.relation_data:
                start_point = self.state_coordinate_data[instance]
                end_point = self.state_coordinate_data[self.relation_data[instance]]
                # color is determined via the local peak
                color = self.relation_color_data[self.relation_data[instance]]
                pygame.draw.line(self.screen, color, (start_point[0] + 20, start_point[1] + 20),
                                 (end_point[0] + 20, end_point[1] + 20))

                pygame.draw.circle(self.screen, color, (end_point[0] + 20, end_point[1] + 20), 12, 1)

        agent_coord_x = self.environment_current_state % self.row_tile_count
        agent_coord_y = self.environment_current_state // self.row_tile_count

        pygame.draw.circle(self.screen, (255, 0, 0), ((MARGIN + self.tile_width) * agent_coord_x +20+ MARGIN,
                 (MARGIN + self.tile_height) * agent_coord_y + MARGIN+20), 15, 15)


        if self.display_policy:
            for st in self.policy_to_display:
                x_ = st % self.row_tile_count
                y_ = st // self.row_tile_count
                text = self.font.render(self.action_symbol[self.policy_to_display[st]], True, (0, 128, 0))
                self.screen.blit(text, ((MARGIN +    self.tile_width) * x_ + MARGIN+8,
                     (MARGIN + self.tile_height) * y_ + MARGIN-13))

                text2 = self.font2.render(str(st), True, (0, 0, 0))
                self.screen.blit(text2, ((MARGIN + self.tile_width) * x_ + MARGIN + 3,
                                         (MARGIN + self.tile_height) * y_ + MARGIN - 8 + 25))

        if self.display_options:
            for opt in self.options_to_display.keys():
                option_states = self.options_to_display[opt]["initiation_set"]
                for st in option_states:
                    x_ = st % self.row_tile_count
                    y_ = st // self.row_tile_count

                    coord = [(MARGIN + self.tile_width) * x_ + MARGIN + 8,
                             (MARGIN + self.tile_height) * y_ + MARGIN + 8,
                             10, 10]

                    pygame.draw.rect(self.screen, self.options_to_display[opt]["color"], coord)

                st = self.options_to_display[opt]["subgoal"]
                x_ = st % self.row_tile_count
                y_ = st // self.row_tile_count

                coord = [(MARGIN + self.tile_width) * x_ + MARGIN + 8,
                         (MARGIN + self.tile_height) * y_ + MARGIN + 8,
                         10, 10]

                pygame.draw.rect(self.screen, (0, 0, 0), coord)

                # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()



    def close(self):
           """Override close in your subclass to perform any necessary cleanup.
           Environments will automatically close() themselves when
           garbage collected or when the program exits.
           """
           pass

    def seed(self, seed=None):
        """Sets the seed for this env's random number generator(s).
        Note:
            Some environments use multiple pseudorandom number generators.
            We want to capture all such seeds used in order to ensure that
            there aren't accidental correlations between multiple generators.
        Returns:
            list<bigint>: Returns the list of seeds used in this env's random
              number generators. The first value in the list should be the
              "main" seed, or the value which a reproducer should pass to
              'seed'. Often, the main seed equals the provided 'seed', but
              this won't be true if seed=None, for example.
        """
        return super(TwoRoomsEnvironmentOnRight, self).seed()

    def saveEnvironmentImage(self, file_name):
        if self.is_window_created:
            pygame.image.save(self.screen, file_name)

            pass

    def setEnvironmentImageTitle(self, name):
        pygame.display.set_caption(name)

 #18/07/2020
    # data = {state1 : val, state2: val2 ....}
    def getSurfaceValueData(self, data):
        x_array, y_array, z_array = [], [], []
        for y in range(self.column_tile_count):
            for x in range(self.row_tile_count):
                x_array.append(x)
                y_array.append(y)
                state = y * self.row_tile_count + x;
                s = self.states[y][x]
                if s == 1 or s == 2:
                    z_array.append(0.0)
                else:
                    if state in data:
                        z_array.append(data[state])
                    else:
                        z_array.append(0.0)

        return x_array, y_array, z_array
