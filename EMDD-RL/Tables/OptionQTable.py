import numpy as np
import random

class Option(object):
    def __init__(self, option_name, option_id, initiation_set, termination_function, policy, primitive_actions=None, goal_rewards = None, is_primitive=False):

        self.epsilon = 0.2 # e of e greedy for exploration during learning...


        self.option_name = option_name
        self.option_id = option_id # int option id to be used while indexing...
        # for learning internal policy... this information will be retrieved from Environment variable
        self.primitive_actions = primitive_actions
        # for checking option policy convergence, but for now it is not used...
        self.policy_update_count = 0


        self.initiation_set = initiation_set

        self.termination_function = termination_function

        self.policy = policy # defines an action policy over initiation set...

        self.inner_policy_value_table = None

        self.is_primitive = is_primitive

        self.goal_rewards = goal_rewards

        self.inner_q_table = {}
        # for checking policy convergence, but not used for now
        self.policy_change_count = 0
        self.has_any_policy_changed = True

        # we are not learning on primitive options
        if self.is_primitive == True:
            self.is_learning = False
        else:
            self.is_learning = True

        if not self.is_primitive:
            for st in self.initiation_set:
                self.inner_q_table[st] = [0] * len(self.primitive_actions)

            # no policy is defined by the option on termination function...
            for term in self.termination_function:
               self.inner_q_table[term] = [0] * len(self.primitive_actions)

            # during learning policy should be stochastic for exploration...



    def getInnerQTable(self, state):
        return self.getInnerQTable([state])


    def printPolicy(self):
        print(self.policy)

    def getGoalRewards(self, state):
        return self.goal_rewards[state]

    def getTerminationFunctionValue(self, state):
        """
        returns the termination function of the option for the given state
        :param state: int state number
        :return: [0-1] float number
        """
        if state in self.termination_function:
            return 1 # self.termination_function[state]
        else:
            return 0

    def isOptionTerminates(self, state):
        return True if state in self.termination_function or (not state in self.initiation_set) else False

    def isPrimitive(self):
        return self.is_primitive

    def getOptionId(self):
        return self.option_id

    def getOptionName(self):
        return self.option_name

    def getOptionPolicy(self, state):
        # primitive action returns it exact policy not random...
        # during learning for exploration, policy is chosen as e greedy
        if self.is_learning == True:
            return self.getStochasticPolicy(state)

        if self.is_primitive:
            return self.policy[0]
        return self.policy[state]

    # this method is only used while learning option policy...
    # it selects the actions as e greedy for exploration...
    # primitive option does not need any policy learning...
    def getStochasticPolicy(self, state):
        if random.random() < self.epsilon:
            return np.random.choice(self.primitive_actions)
        else:
            # print(self)
            # print("state : "+str(state))
            # print("init : "+str(self.initiation_set))
            # print("terimation : "+ str(self.termination_function))
            # print("policy : ", self.policy)
            return self.policy[state]

    def __str__(self):
        return "Option name : "+self.option_name + " Option Id : "+str(self.option_id)

    def isConsistenWith(self, state, action):
        """
        for checking whether requested option is consistent with given state and action,
        if the option uses the same action for the given state, we assume that it is consistent...
        :param state: int state number
        :param action: int action number
        :return: boolean
        """
        if self.is_primitive:
            if self.policy[0] == action:
                return True
            else:
                return False

        return True if state in self.initiation_set and action == self.getOptionPolicy(state) else False

    def isOptionDefineOverState(self, state):
        if self.is_primitive:
            return True
        return state in self.initiation_set

    # for updating policy...
    def setPolicy(self, state, action):
        self.policy[state] = action
    def getTerminationStates(self):
        return self.termination_function



    def __eq__(self, other):
        return True if self.option_id == other.option_id else False








class OptionTable(object):

    def __init__(self, state_space_dimension, option_space_size, learning_rate, discount, epsilon,
                 eligibility_trace=False, trace_factor=0.35):


        LEFT, RIGHT, UP, DOWN = 0, 2, 3,1
        POLICY = {'<': LEFT, '^': UP, '>': RIGHT, 'V': DOWN}


        # self.action_set = [self.LEFT, self.DOWN, self.RIGHT, self.UP]
        # self.action_symbol = ['<', 'v', '>', '^']

        r1_op1_init = [14,15,16,17,18,
                       27,28,29,30,31,
                       40,41,42,43,44,
                       53,54,55,56,57,
                       66,67,68,69,70,
                          80           ]
        r1_op1_policy = ['>', '>', '>', '>', 'V',
                         '>', '>', '>', 'V', 'V',
                         '>', '>', '>', '>', '>',
                         '>', '>' ,'>', '>', '^',
                         '>', '>', '>', '^', '^',
                              '^'                ]

        r1_op2_init = [14,15,16,17,18,
                       27,28,29,30,31,
                       40,41,42,43,44, 45,
                       53,54,55,56,57,
                       66,67,68,69,70  ]


        r1_op2_policy = ['V', 'V', '<', '<', '<',
                         'V', 'V', '<', '<', '<',
                         'V', 'V', '<', '<', '<', '<',
                         '>', 'V', '<', '<', '<',
                         '>', 'V', '<', '<', '<'      ]

        # room 2 option 1

        r2_op1_init = [20, 21, 22, 23, 24,
                       33, 34, 35, 36, 37,
                   45, 46, 47, 48, 49, 50,
                       59, 60, 61, 62, 63,
                       72, 73, 74, 75, 76,
                       85, 86, 87, 88, 89
                                       ]

        r2_op1_policy = ['V', 'V', 'V', 'V', 'V',
                         'V', 'V', 'V', 'V', 'V',
                    '>', 'V', 'V', 'V', 'V', 'V',
                         'V', 'V', 'V', 'V', 'V',
                         '>', '>', 'V', '<', '<',
                         '>', '>', 'V', '<', '<'   ]

        # room 2 option 2

        r2_op2_init = [20, 21, 22, 23, 24,
                       33, 34, 35, 36, 37,
                       46, 47, 48, 49, 50,
                       59, 60, 61, 62, 63,
                       72, 73, 74, 75, 76,
                       85, 86, 87, 88, 89,
                               100           ]

        r2_op2_policy = ['V', 'V', '<', '<', '<',
                         'V', 'V', '<', '<', '<',
                         '<', '<', '<', '<', '<',
                         '^', '^', '<', '<', '<',
                         '^', '^', '^', '<', '<',
                         '^', '^', '^', '^', '^',
                                   '^'            ]

        # room 3 option 1

        r3_op1_init = [    80,
                       92, 93, 94, 95, 96,
                       105,106,107,108,109,
                       118,119,120,121,122,
                       131,132,133,134,135,
                       144,145,146,147,148  ]

        r3_op1_policy = [     'V',
                         '>', '>', '>', 'V', 'V',
                         '>', '>', '>', 'V', 'V',
                         '>', '>', '>', 'V', 'V',
                         '>', '>', '>', '>', '>',
                         '>', '>', '^', '^', '^'   ]

        # room 3 option 2

        r3_op2_init = [
                       92, 93, 94, 95, 96,
                       105, 106, 107, 108, 109,
                       118, 119, 120, 121, 122,
                       131, 132, 133, 134, 135, 136,
                       144, 145, 146, 147, 148]

        r3_op2_policy = [
                         '>', '^', '<', '<', '<',
                         '>', '^', '<', '<', '<',
                         '>', '^', '<', '<', '<',
                         '^', '^', '<', '<', '<', '<',
                         '^', '^', '<', '<', '<']

        # room 4 option 1

        r4_op1_init = [
                        111,112,113,114,115,
                        124,125,126,127,128,
                    136,137,138,139,140,141,
                        150,151,152,153,154  ]

        r4_op1_policy = [
                        '>', '>', '^', '<', '<',
                        '>', '>', '^', '<', '<',
                   '>', '>', '>', '^', '^', '<',
                        '>', '>', '^', '^', '<' ]


        # room 4 option 2

        r4_op2_init = [         100,
                        111,112,113,114,115,
                        124,125,126,127,128,
                        137,138,139,140,141,
                        150,151,152,153,154  ]

        r4_op2_policy = [         'V',
                        'V', 'V', 'V', 'V', 'V',
                        'V', 'V', 'V', '<', '<',
                        '<', '<', '<', '<', '<',
                        '^', '^', '<', '<', '<' ]




        r1_op1_terminate = [45]
        r1_op2_terminate = [80]

        r2_op1_terminate = [100]
        r2_op2_terminate = [45]

        r3_op1_terminate = [136]
        r3_op2_terminate = [80]

        r4_op1_terminate = [100, 126]
        r4_op2_terminate = [136, 126]


        r1_op1_policy = {r1_op1_init[a]: POLICY[r1_op1_policy[a]] for a in range(len(r1_op1_init))}
        r1_op2_policy = {r1_op2_init[a]: POLICY[r1_op2_policy[a]] for a in range(len(r1_op2_init))}

        r2_op1_policy = {r2_op1_init[a]: POLICY[r2_op1_policy[a]] for a in range(len(r2_op1_init))}
        r2_op2_policy = {r2_op2_init[a]: POLICY[r2_op2_policy[a]] for a in range(len(r2_op2_init))}

        r3_op1_policy = {r3_op1_init[a]: POLICY[r3_op1_policy[a]] for a in range(len(r3_op1_init))}
        r3_op2_policy = {r3_op2_init[a]: POLICY[r3_op2_policy[a]] for a in range(len(r3_op2_init))}

        r4_op1_policy = {r4_op1_init[a]: POLICY[r4_op1_policy[a]] for a in range(len(r4_op1_init))}
        r4_op2_policy = {r4_op2_init[a]: POLICY[r4_op2_policy[a]] for a in range(len(r4_op2_init))}

        primitive_actions = [0, 1, 2, 3]

        room1_option1 = Option("room1_op1", 0, r1_op1_init, r1_op1_terminate, r1_op1_policy,
                               primitive_actions=primitive_actions)
        room1_option2 = Option("room1_op2", 1, r1_op2_init, r1_op2_terminate, r1_op2_policy,
                               primitive_actions=primitive_actions)

        room2_option1 = Option("room2_op1", 2, r2_op1_init, r2_op1_terminate, r2_op1_policy,
                               primitive_actions=primitive_actions)
        room2_option2 = Option("room2_op2", 3, r2_op2_init, r2_op2_terminate, r2_op2_policy,
                               primitive_actions=primitive_actions)

        room3_option1 = Option("room3_op1", 4, r3_op1_init, r3_op1_terminate, r3_op1_policy,
                               primitive_actions=primitive_actions)
        room3_option2 = Option("room3_op2", 5, r3_op2_init, r3_op2_terminate, r3_op2_policy,
                               primitive_actions=primitive_actions)

        room4_option1 = Option("room4_op1", 6, r4_op1_init, r4_op1_terminate, r4_op1_policy, primitive_actions=primitive_actions)
        room4_option2 = Option("room4_op2", 7, r4_op2_init, r4_op2_terminate, r4_op2_policy, primitive_actions=primitive_actions        )

        # on goal state every option should end...
        primitive_op1 = Option("primitive_op_left", 8, [], [126], [LEFT], is_primitive=True)
        primitive_op2 = Option("primitive_op_right", 9, [], [126], [RIGHT], is_primitive=True)
        primitive_op3 = Option("primitive_op_up", 10, [], [126], [UP], is_primitive=True)
        primitive_op4 = Option("primitive_op_down", 11, [], [126], [DOWN], is_primitive=True)


        self.options = []
        self.options.append(room1_option1)
        self.options.append(room1_option2)
        self.options.append(room2_option1)
        self.options.append(room2_option2)
        self.options.append(room3_option1)
        self.options.append(room3_option2)
        self.options.append(room4_option1)
        self.options.append(room4_option2)

        # we are adding primitive options...
        self.options.append(primitive_op1)
        self.options.append(primitive_op2)
        self.options.append(primitive_op3)
        self.options.append(primitive_op4)


        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.discount_rate = discount
        self.option_space_size = option_space_size # how many options exist
        self.state_space_dimension = [a for a in state_space_dimension]
        # state space combine with option space
        self.state_space_dimension.append(option_space_size)
        self.Q_Table = np.zeros(self.state_space_dimension, dtype=np.float32)

        # for know we are applying option to one dimensional state space...
        for option in self.options:
            for state in range(self.state_space_dimension[0]):
                # if option is not defined over state
                if not option.isOptionDefineOverState(state):
                    self.Q_Table[state][option.getOptionId()] = -float('inf')


        if eligibility_trace == True:
            self.Eligibily_Trace = np.zeros(self.state_space_dimension, dtype=np.float32)
            self.trace_factor = trace_factor



        # if an option is not defined on a state then its corresponding table value is -infinity

    # option step is the number of time steps the option has been applied...
    def updateQTable(self, current_state, current_option, terminated_state, accumulated_reward, option_step):
        if len(self.state_space_dimension) == 2:
            self.Q_Table[current_state][current_option.getOptionId()] += \
                (self.learning_rate) * (accumulated_reward + (self.discount_rate**option_step) * self.getMaxOptionValue(terminated_state) -
                                      self.Q_Table[current_state][current_option.getOptionId()])

        elif len(self.state_space_dimension) == 3:
            self.Q_Table[current_state[0]][current_state[1]][current_option] += \
                (self.learning_rate) * (accumulated_reward + (self.discount_rate**option_step) * self.getMaxOptionValue(terminated_state) -
                                      self.Q_Table[current_state[0]][current_state[1]][current_option])

    # for now only 1D states are considered...
    def updateSarsaTable(self, current_state, current_option, terminated_state, next_option, accumulated_reward, option_step):

        if len(self.state_space_dimension) == 2:
            print("current state ", self.Q_Table[current_state])
            print("next state ", self.Q_Table[terminated_state])
            print("Current option ", str(current_option))
            print("Next option ", str(next_option)),
            print("q(current, current_option) : ", self.Q_Table[current_state][current_option.getOptionId()])
            print("q(next, next_state) : ", self.Q_Table[terminated_state][next_option.getOptionId()])

            self.Q_Table[current_state][current_option.getOptionId()] += \
                (self.learning_rate) * (accumulated_reward + (self.discount_rate**option_step) * self.Q_Table[terminated_state][next_option.getOptionId()] -
                                      self.Q_Table[current_state][current_option.getOptionId()])

        elif len(self.state_space_dimension) == 3:
            self.Q_Table[current_state[0]][current_state[1]][current_option] += \
                (self.learning_rate) * (
                            accumulated_reward + (self.discount_rate**option_step) * self.Q_Table[terminated_state[0]][terminated_state[1]][next_option] -
                            self.Q_Table[current_state[0]][current_state[1]][current_option])

    def updateSarsaLambdaTable(self, current_state, current_option, terminated_state, next_option, accumulated_reward, option_step):
        if len(self.state_space_dimension) == 2:
            TD_Error = accumulated_reward + (self.discount_rate**option_step) * self.Q_Table[terminated_state][next_option.getOptionId()] - \
                       self.Q_Table[current_state][current_option.getOptionId()]

            self.Eligibily_Trace[current_state][current_option.getOptionId()] += 1.0

            self.Q_Table += self.learning_rate * TD_Error * self.Eligibily_Trace

            self.Eligibily_Trace *= self.trace_factor

        elif len(self.state_space_dimension) == 3:
            TD_Error = accumulated_reward + self.discount_rate * \
                       self.Q_Table[terminated_state[0]][terminated_state[1]][next_option] \
                       - self.Q_Table[current_state[0]][current_state[1]][current_option]

            self.Eligibily_Trace[current_state[0]][current_state[1]][current_option] += 1.0

            self.Q_Table += self.learning_rate * TD_Error * self.Eligibily_Trace

            self.Eligibily_Trace *= self.trace_factor

        # Watkins Q. if selected option is the max option (not exploratory) then normal decay
        # else eligibility is zeroed

    def updateQLambdaTable(self, current_state, current_option, terminated_state, accumulated_reward):
        if len(self.state_space_dimension) == 2:
            TD_Error = accumulated_reward + self.discount_rate * self.getMaxOptionValue(terminated_state) - \
                       self.Q_Table[current_state][current_option]

            self.Eligibily_Trace[current_state][current_option] += 1.0
            max_option = self.getMaxOption(current_state)
            self.Q_Table += self.learning_rate * TD_Error * self.Eligibily_Trace

            # if non-greedy chosen stop learning...
            if current_option == max_option:
                self.Eligibily_Trace *= self.trace_factor
            else:
                self.Eligibily_Trace = np.zeros(self.state_space_dimension, dtype=np.float32)

        elif len(self.state_space_dimension) == 3:
            TD_Error = accumulated_reward + self.discount_rate * \
                       self.getMaxOptionValue(terminated_state) \
                       - self.Q_Table[current_state[0]][current_state[1]][current_option]

            self.Eligibily_Trace[current_state[0]][current_state[1]][current_option] += 1.0
            max_option = self.getMaxOption(current_state)

            self.Q_Table += self.learning_rate * TD_Error * self.Eligibily_Trace

            # if non-greedy chosen stop learning...
            if current_option == max_option:
                self.Eligibily_Trace *= self.trace_factor
            else:
                self.Eligibily_Trace = np.zeros(self.state_space_dimension, dtype=np.float32)

    def getMaxOptionValue(self, state):
        if len(self.state_space_dimension) == 2:
            return np.max(self.Q_Table[state])
        elif len(self.state_space_dimension) == 3:
            return np.max(self.Q_Table[state[0]][state[1]])

    def getMaxOption(self, state):
        chosen_option = None
        if len(self.state_space_dimension) == 2:
            chosen_option = np.argmax(self.Q_Table[state])
        elif len(self.state_space_dimension) == 3:
            chosen_option = np.argmax(self.Q_Table[state[0]][state[1]])

        #print("chosen option : ", chosen_option)
        chosen_option = self.getOption(chosen_option)
        return chosen_option

    def getOption(self, option_id):
        #print("getOption : ", len(self.options))
        for op in self.options:
            #print("op : ", op.getOptionId())
            if option_id == op.getOptionId():
                return op


    # Only defined options should be returned over state...
    def sampleOption(self, current_state):
        if len(self.state_space_dimension) == 2:
            if random.random() < self.epsilon:
                defined_options = [op for op in self.options if op.isOptionDefineOverState(current_state)]
                #print("defined options : ", defined_options)
                return np.random.choice(defined_options)
            else:
                #print("MaxQOption")
                return self.getMaxOption(current_state)
        elif len(self.state_space_dimension) == 3:
            if random.random() < self.epsilon:
                return np.random.choice(range(self.option_space_size))
            else:
                return self.getMaxOption(current_state)

    def getVisualPolicy(self):
        character = np.zeros(self.state_space_dimension[0], dtype=np.str)
        way = ['<', 'V', '>', '^']
        for state in range(self.state_space_dimension[0]):
            character[state] = way[np.argmax(self.Q_Table[state])]
        return character.reshape((4, 4))

    def getQTable(self):
        return self.Q_Table

    def getLearnedOption(self, current_state):
        return self.getMaxOption(current_state)

    def getConvergenceMetric(self):
        return np.sqrt(np.square(np.ma.masked_invalid(self.Q_Table)).sum())

    # for debuggin purposes...
    def getImportantStatesLearnedOptions(self, state_list):
        for state in state_list:
            print("State "+str(state)+" Opt "+self.getLearnedOption(state).getOptionName())

    def getImportantStatesQValues(self, state_list):
        for state in state_list:
            print("q(state="+str(state)+")=", self.Q_Table[state])



# Intra-option learning methods are implemented...
class IntraOptionTable(object):

    def __init__(self, state_space_dimension, option_space_size, learning_rate, discount, epsilon,
                 eligibility_trace=False, trace_factor=0.35):


        LEFT, RIGHT, UP, DOWN = 0, 2, 3,1
        POLICY = {'<': LEFT, '^': UP, '>': RIGHT, 'V': DOWN}


        # self.action_set = [self.LEFT, self.DOWN, self.RIGHT, self.UP]
        # self.action_symbol = ['<', 'v', '>', '^']

        r1_op1_init = [14,15,16,17,18,
                       27,28,29,30,31,
                       40,41,42,43,44,
                       53,54,55,56,57,
                       66,67,68,69,70,
                          80           ]
        r1_op1_policy = ['>', '>', '>', '>', 'V',
                         '>', '>', '>', 'V', 'V',
                         '>', '>', '>', '>', '>',
                         '>', '>' ,'>', '>', '^',
                         '>', '>', '>', '^', '^',
                              '^'                ]

        r1_op2_init = [14,15,16,17,18,
                       27,28,29,30,31,
                       40,41,42,43,44, 45,
                       53,54,55,56,57,
                       66,67,68,69,70  ]


        r1_op2_policy = ['V', 'V', '<', '<', '<',
                         'V', 'V', '<', '<', '<',
                         'V', 'V', '<', '<', '<', '<',
                         '>', 'V', '<', '<', '<',
                         '>', 'V', '<', '<', '<'      ]

        # room 2 option 1

        r2_op1_init = [20, 21, 22, 23, 24,
                       33, 34, 35, 36, 37,
                   45, 46, 47, 48, 49, 50,
                       59, 60, 61, 62, 63,
                       72, 73, 74, 75, 76,
                       85, 86, 87, 88, 89
                                       ]

        r2_op1_policy = ['V', 'V', 'V', 'V', 'V',
                         'V', 'V', 'V', 'V', 'V',
                    '>', 'V', 'V', 'V', 'V', 'V',
                         'V', 'V', 'V', 'V', 'V',
                         '>', '>', 'V', '<', '<',
                         '>', '>', 'V', '<', '<'   ]

        # room 2 option 2

        r2_op2_init = [20, 21, 22, 23, 24,
                       33, 34, 35, 36, 37,
                       46, 47, 48, 49, 50,
                       59, 60, 61, 62, 63,
                       72, 73, 74, 75, 76,
                       85, 86, 87, 88, 89,
                               100           ]

        r2_op2_policy = ['V', 'V', '<', '<', '<',
                         'V', 'V', '<', '<', '<',
                         '<', '<', '<', '<', '<',
                         '^', '^', '<', '<', '<',
                         '^', '^', '^', '<', '<',
                         '^', '^', '^', '^', '^',
                                   '^'            ]

        # room 3 option 1

        r3_op1_init = [    80,
                       92, 93, 94, 95, 96,
                       105,106,107,108,109,
                       118,119,120,121,122,
                       131,132,133,134,135,
                       144,145,146,147,148  ]

        r3_op1_policy = [     'V',
                         '>', '>', '>', 'V', 'V',
                         '>', '>', '>', 'V', 'V',
                         '>', '>', '>', 'V', 'V',
                         '>', '>', '>', '>', '>',
                         '>', '>', '^', '^', '^'   ]

        # room 3 option 2

        r3_op2_init = [
                       92, 93, 94, 95, 96,
                       105, 106, 107, 108, 109,
                       118, 119, 120, 121, 122,
                       131, 132, 133, 134, 135, 136,
                       144, 145, 146, 147, 148]

        r3_op2_policy = [
                         '>', '^', '<', '<', '<',
                         '>', '^', '<', '<', '<',
                         '>', '^', '<', '<', '<',
                         '^', '^', '<', '<', '<', '<',
                         '^', '^', '<', '<', '<']

        # room 4 option 1

        r4_op1_init = [
                        111,112,113,114,115,
                        124,125,126,127,128,
                    136,137,138,139,140,141,
                        150,151,152,153,154  ]

        r4_op1_policy = [
                        '>', '>', '^', '<', '<',
                        '>', '>', '^', '<', '<',
                   '>', '>', '>', '^', '^', '<',
                        '>', '>', '^', '^', '<' ]


        # room 4 option 2

        r4_op2_init = [         100,
                        111,112,113,114,115,
                        124,125,126,127,128,
                        137,138,139,140,141,
                        150,151,152,153,154  ]

        r4_op2_policy = [         'V',
                        'V', 'V', 'V', 'V', 'V',
                        'V', 'V', 'V', '<', '<',
                        '<', '<', '<', '<', '<',
                        '^', '^', '<', '<', '<' ]




        r1_op1_terminate = [45]
        r1_op2_terminate = [80]

        r2_op1_terminate = [100]
        r2_op2_terminate = [45]

        r3_op1_terminate = [136]
        r3_op2_terminate = [80]

        r4_op1_terminate = [100, 126]
        r4_op2_terminate = [136, 126]


        r1_op1_policy = {r1_op1_init[a]: POLICY[r1_op1_policy[a]] for a in range(len(r1_op1_init))}
        r1_op2_policy = {r1_op2_init[a]: POLICY[r1_op2_policy[a]] for a in range(len(r1_op2_init))}

        r2_op1_policy = {r2_op1_init[a]: POLICY[r2_op1_policy[a]] for a in range(len(r2_op1_init))}
        r2_op2_policy = {r2_op2_init[a]: POLICY[r2_op2_policy[a]] for a in range(len(r2_op2_init))}

        r3_op1_policy = {r3_op1_init[a]: POLICY[r3_op1_policy[a]] for a in range(len(r3_op1_init))}
        r3_op2_policy = {r3_op2_init[a]: POLICY[r3_op2_policy[a]] for a in range(len(r3_op2_init))}

        r4_op1_policy = {r4_op1_init[a]: POLICY[r4_op1_policy[a]] for a in range(len(r4_op1_init))}
        r4_op2_policy = {r4_op2_init[a]: POLICY[r4_op2_policy[a]] for a in range(len(r4_op2_init))}

        primitive_actions = [0, 1, 2, 3]
        room1_option1 = Option("room1_op1", 0, r1_op1_init, r1_op1_terminate, r1_op1_policy,
                               primitive_actions=primitive_actions)
        room1_option2 = Option("room1_op2", 1, r1_op2_init, r1_op2_terminate, r1_op2_policy,
                               primitive_actions=primitive_actions)

        room2_option1 = Option("room2_op1", 2, r2_op1_init, r2_op1_terminate, r2_op1_policy,
                               primitive_actions=primitive_actions)
        room2_option2 = Option("room2_op2", 3, r2_op2_init, r2_op2_terminate, r2_op2_policy,
                               primitive_actions=primitive_actions)

        room3_option1 = Option("room3_op1", 4, r3_op1_init, r3_op1_terminate, r3_op1_policy,
                               primitive_actions=primitive_actions)
        room3_option2 = Option("room3_op2", 5, r3_op2_init, r3_op2_terminate, r3_op2_policy,
                               primitive_actions=primitive_actions)

        room4_option1 = Option("room4_op1", 6, r4_op1_init, r4_op1_terminate, r4_op1_policy,
                               primitive_actions=primitive_actions)
        room4_option2 = Option("room4_op2", 7, r4_op2_init, r4_op2_terminate, r4_op2_policy,
                               primitive_actions=primitive_actions)

        # on goal state every option should end...
        primitive_op1 = Option("primitive_op_left", 8, [], [126], [LEFT], is_primitive=True)
        primitive_op2 = Option("primitive_op_right", 9, [], [126], [RIGHT], is_primitive=True)
        primitive_op3 = Option("primitive_op_up", 10, [], [126], [UP], is_primitive=True)
        primitive_op4 = Option("primitive_op_down", 11, [], [126], [DOWN], is_primitive=True)


        self.options = []
        self.options.append(room1_option1)
        self.options.append(room1_option2)
        self.options.append(room2_option1)
        self.options.append(room2_option2)
        self.options.append(room3_option1)
        self.options.append(room3_option2)
        self.options.append(room4_option1)
        self.options.append(room4_option2)

        # we are adding primitive options...
        self.options.append(primitive_op1)
        self.options.append(primitive_op2)
        self.options.append(primitive_op3)
        self.options.append(primitive_op4)


        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.discount_rate = discount
        self.option_space_size = option_space_size # how many options exist
        self.state_space_dimension = [a for a in state_space_dimension]
        # state space combine with option space
        self.state_space_dimension.append(option_space_size)
        self.Q_Table = np.zeros(self.state_space_dimension, dtype=np.float32)

        # for know we are applying option to one dimensional state space...
        for option in self.options:
            for state in range(self.state_space_dimension[0]):
                # if option is not defined over state
                if not option.isOptionDefineOverState(state):
                    self.Q_Table[state][option.getOptionId()] = -float('inf')


        if eligibility_trace == True:
            self.Eligibily_Trace = np.zeros(self.state_space_dimension, dtype=np.float32)
            self.trace_factor = trace_factor



        # if an option is not defined on a state then its corresponding table value is -infinity

    # in each step consistent options are being updated...
    def updateQTable(self, current_state, current_option, reward, next_state):
        if len(self.state_space_dimension) == 2:
            # current performed action over current state
            c_act = current_option.getOptionPolicy(current_state)
            # get consistent options for the current state and action

            valid_options = self.getConsistentOptionsWithState(current_state, c_act)
            # then update related option values...
            # print("\n\nCurrent state : " +str(current_state))
            # print("Available options : ")
            # for k in valid_options:
            #     print(str(k))

            # print("\n\n")

            for c_option in valid_options:
                current_option = c_option

                # print("\n\nCurrent state : " + str(current_state))
                # print("Next state : " + str(next_state))
                # print("Current option : " + str(c_option))
                # print("Current option term in next state : " + str(current_option.getTerminationFunctionValue(next_state)))

                next_state_terminal_probability = current_option.getTerminationFunctionValue(next_state)
                if current_option.isOptionTerminates(next_state):
                    next_state_utility = self.getMaxOptionValue(next_state)
                else:
                    next_state_utililty = self.Q_Table[next_state][current_option.getOptionId()]


                #
                # print("next state utility :  "+ str(next_state_utility))
                # print("Before Update")
                # print("q(current_state) : ", self.Q_Table[current_state])
                # print("q(next state) : " , self.Q_Table[next_state])
                self.Q_Table[current_state][current_option.getOptionId()] += \
                    (self.learning_rate) * (reward + (self.discount_rate) * next_state_utility -
                                          self.Q_Table[current_state][current_option.getOptionId()])

                # print("After Update")
                # print("q(current_state) : ", self.Q_Table[current_state])
                # print("q(next state) : ", self.Q_Table[next_state])



        elif len(self.state_space_dimension) == 3:
            self.Q_Table[current_state[0]][current_state[1]][current_option] += \
                (self.learning_rate) * ( (self.discount_rate**option_step) * self.getMaxOptionValue(terminated_state) -
                                      self.Q_Table[current_state[0]][current_state[1]][current_option])

    # for now only 1D states are considered...
    def updateSarsaTable(self, current_state, current_option, terminated_state, next_option, accumulated_reward, option_step):

        if len(self.state_space_dimension) == 2:
            print("current state ", self.Q_Table[current_state])
            print("next state ", self.Q_Table[terminated_state])
            print("Current option ", str(current_option))
            print("Next option ", str(next_option)),
            print("q(current, current_option) : ", self.Q_Table[current_state][current_option.getOptionId()])
            print("q(next, next_state) : ", self.Q_Table[terminated_state][next_option.getOptionId()])

            self.Q_Table[current_state][current_option.getOptionId()] += \
                (self.learning_rate) * (accumulated_reward + (self.discount_rate**option_step) * self.Q_Table[terminated_state][next_option.getOptionId()] -
                                      self.Q_Table[current_state][current_option.getOptionId()])

        elif len(self.state_space_dimension) == 3:
            self.Q_Table[current_state[0]][current_state[1]][current_option] += \
                (self.learning_rate) * (
                            accumulated_reward + (self.discount_rate**option_step) * self.Q_Table[terminated_state[0]][terminated_state[1]][next_option] -
                            self.Q_Table[current_state[0]][current_state[1]][current_option])

    def updateSarsaLambdaTable(self, current_state, current_option, terminated_state, next_option, accumulated_reward, option_step):
        if len(self.state_space_dimension) == 2:
            TD_Error = accumulated_reward + (self.discount_rate**option_step) * self.Q_Table[terminated_state][next_option.getOptionId()] - \
                       self.Q_Table[current_state][current_option.getOptionId()]

            self.Eligibily_Trace[current_state][current_option.getOptionId()] += 1.0

            self.Q_Table += self.learning_rate * TD_Error * self.Eligibily_Trace

            self.Eligibily_Trace *= self.trace_factor

        elif len(self.state_space_dimension) == 3:
            TD_Error = accumulated_reward + self.discount_rate * \
                       self.Q_Table[terminated_state[0]][terminated_state[1]][next_option] \
                       - self.Q_Table[current_state[0]][current_state[1]][current_option]

            self.Eligibily_Trace[current_state[0]][current_state[1]][current_option] += 1.0

            self.Q_Table += self.learning_rate * TD_Error * self.Eligibily_Trace

            self.Eligibily_Trace *= self.trace_factor

        # Watkins Q. if selected option is the max option (not exploratory) then normal decay
        # else eligibility is zeroed

    def updateQLambdaTable(self, current_state, current_option, terminated_state, accumulated_reward):
        if len(self.state_space_dimension) == 2:
            TD_Error = accumulated_reward + self.discount_rate * self.getMaxOptionValue(terminated_state) - \
                       self.Q_Table[current_state][current_option]

            self.Eligibily_Trace[current_state][current_option] += 1.0
            max_option = self.getMaxOption(current_state)
            self.Q_Table += self.learning_rate * TD_Error * self.Eligibily_Trace

            # if non-greedy chosen stop learning...
            if current_option == max_option:
                self.Eligibily_Trace *= self.trace_factor
            else:
                self.Eligibily_Trace = np.zeros(self.state_space_dimension, dtype=np.float32)

        elif len(self.state_space_dimension) == 3:
            TD_Error = accumulated_reward + self.discount_rate * \
                       self.getMaxOptionValue(terminated_state) \
                       - self.Q_Table[current_state[0]][current_state[1]][current_option]

            self.Eligibily_Trace[current_state[0]][current_state[1]][current_option] += 1.0
            max_option = self.getMaxOption(current_state)

            self.Q_Table += self.learning_rate * TD_Error * self.Eligibily_Trace

            # if non-greedy chosen stop learning...
            if current_option == max_option:
                self.Eligibily_Trace *= self.trace_factor
            else:
                self.Eligibily_Trace = np.zeros(self.state_space_dimension, dtype=np.float32)

    def getMaxOptionValue(self, state):
        if len(self.state_space_dimension) == 2:
            return np.max(self.Q_Table[state])
        elif len(self.state_space_dimension) == 3:
            return np.max(self.Q_Table[state[0]][state[1]])

    # primitive actions are updated first later others...
    def getConsistentOptionsWithState(self, state, action):
        consistent_options = []
        #first primitive options
        for op in self.options:
            if op.isPrimitive():
                # print(op)
                if op.isConsistenWith(state, action):
                    consistent_options.append(op)

        # first primitive options
        for op in self.options:
            if not op.isPrimitive():
                if op.isConsistenWith(state, action):
                    consistent_options.append(op)
        return consistent_options


    def getMaxOption(self, state):
        chosen_option = None
        if len(self.state_space_dimension) == 2:
            chosen_option = np.argmax(self.Q_Table[state])
        elif len(self.state_space_dimension) == 3:
            chosen_option = np.argmax(self.Q_Table[state[0]][state[1]])

        #print("chosen option : ", chosen_option)
        chosen_option = self.getOption(chosen_option)
        return chosen_option

    def getOption(self, option_id):
        #print("getOption : ", len(self.options))
        for op in self.options:
            #print("op : ", op.getOptionId())
            if option_id == op.getOptionId():
                return op


    # Only defined options should be returned over state...
    def sampleOption(self, current_state):
        if len(self.state_space_dimension) == 2:
            if random.random() < self.epsilon:
                defined_options = [op for op in self.options if op.isOptionDefineOverState(current_state)]
                #print("defined options : ", defined_options)
                return np.random.choice(defined_options)
            else:
                #print("MaxQOption")
                return self.getMaxOption(current_state)
        elif len(self.state_space_dimension) == 3:
            if random.random() < self.epsilon:
                return np.random.choice(range(self.option_space_size))
            else:
                return self.getMaxOption(current_state)

    def getVisualPolicy(self):
        character = np.zeros(self.state_space_dimension[0], dtype=np.str)
        way = ['<', 'V', '>', '^']
        for state in range(self.state_space_dimension[0]):
            character[state] = way[np.argmax(self.Q_Table[state])]
        return character.reshape((4, 4))

    def getQTable(self):
        return self.Q_Table

    def getLearnedOption(self, current_state):
        return self.getMaxOption(current_state)

    def getConvergenceMetric(self):
        return np.sqrt(np.square(np.ma.masked_invalid(self.Q_Table)).sum())

    # for debuggin purposes...
    def getImportantStatesLearnedOptions(self, state_list):
        for state in state_list:
            print("State "+str(state)+" Opt "+self.getLearnedOption(state).getOptionName())

    def getImportantStatesQValues(self, state_list):
        for state in state_list:
            print("q(state="+str(state)+")=", self.Q_Table[state])



# Option policy is changed during interacting with the environment...
class PolicyLearningIntraOptionTable(object):

    def __init__(self, state_space_dimension, option_space_size, learning_rate, discount, epsilon,
                 eligibility_trace=False, trace_factor=0.35):


        LEFT, RIGHT, UP, DOWN = 0, 2, 3,1
        POLICY = {'<': LEFT, 'V': DOWN, '>': RIGHT, '^': UP  }
        self.POLICY = ['<', 'V', '>', '^']

        # self.action_set = [self.LEFT, self.DOWN, self.RIGHT, self.UP]
        # self.action_symbol = ['<', 'v', '>', '^']

        r1_op1_init = [14,15,16,17,18,
                       27,28,29,30,31,
                       40,41,42,43,44,
                       53,54,55,56,57,
                       66,67,68,69,70,
                          80           ]
        # random policy at the beginning...
        r1_op1_policy = [np.random.choice(POLICY.keys()) for l in range(len(r1_op1_init))]

        r1_op2_init = [14,15,16,17,18,
                       27,28,29,30,31,
                       40,41,42,43,44, 45,
                       53,54,55,56,57,
                       66,67,68,69,70  ]


        r1_op2_policy = [np.random.choice(POLICY.keys()) for l in range(len(r1_op2_init))]

        # room 2 option 1

        r2_op1_init = [20, 21, 22, 23, 24,
                       33, 34, 35, 36, 37,
                   45, 46, 47, 48, 49, 50,
                       59, 60, 61, 62, 63,
                       72, 73, 74, 75, 76,
                       85, 86, 87, 88, 89
                                       ]

        r2_op1_policy = [np.random.choice(POLICY.keys()) for l in range(len(r2_op1_init))]

        # room 2 option 2

        r2_op2_init = [20, 21, 22, 23, 24,
                       33, 34, 35, 36, 37,
                       46, 47, 48, 49, 50,
                       59, 60, 61, 62, 63,
                       72, 73, 74, 75, 76,
                       85, 86, 87, 88, 89,
                               100           ]

        r2_op2_policy = [np.random.choice(POLICY.keys()) for l in range(len(r2_op2_init))]

        # room 3 option 1

        r3_op1_init = [    80,
                       92, 93, 94, 95, 96,
                       105,106,107,108,109,
                       118,119,120,121,122,
                       131,132,133,134,135,
                       144,145,146,147,148  ]

        r3_op1_policy = [np.random.choice(POLICY.keys()) for l in range(len(r3_op1_init))]

        # room 3 option 2

        r3_op2_init = [
                       92, 93, 94, 95, 96,
                       105, 106, 107, 108, 109,
                       118, 119, 120, 121, 122,
                       131, 132, 133, 134, 135, 136,
                       144, 145, 146, 147, 148]

        r3_op2_policy = [np.random.choice(POLICY.keys()) for l in range(len(r3_op2_init))]

        # room 4 option 1

        r4_op1_init = [
                        111,112,113,114,115,
                        124,125,126,127,128,
                    136,137,138,139,140,141,
                        150,151,152,153,154  ]

        r4_op1_policy = [np.random.choice(POLICY.keys()) for l in range(len(r4_op1_init))]


        # room 4 option 2

        r4_op2_init = [         100,
                        111,112,113,114,115,
                        124,125,126,127,128,
                        137,138,139,140,141,
                        150,151,152,153,154  ]

        r4_op2_policy = [np.random.choice(POLICY.keys()) for l in range(len(r4_op2_init))]




        r1_op1_terminate = [45]
        r1_op1_goal_rewards = {45: 1}

        r1_op2_terminate = [80]
        r1_op2_goal_rewards = {80: 1}

        r2_op1_terminate = [100]
        r2_op1_goal_rewards = {100: 1}

        r2_op2_terminate = [45]
        r2_op2_goal_rewards = {45: 1}

        r3_op1_terminate = [136]
        r3_op1_goal_rewards = {136: 1}

        r3_op2_terminate = [80]
        r3_op2_goal_rewards = {80: 1}

        r4_op1_terminate = [100, 126]
        r4_op1_goal_rewards = {100: 1, 126: 1}

        r4_op2_terminate = [136, 126]
        r4_op2_goal_rewards = {136: 1, 126: 1}


        primitive_actions = [0, 1, 2, 3]


        r1_op1_policy = {r1_op1_init[a]: POLICY[r1_op1_policy[a]] for a in range(len(r1_op1_init))}
        r1_op2_policy = {r1_op2_init[a]: POLICY[r1_op2_policy[a]] for a in range(len(r1_op2_init))}

        r2_op1_policy = {r2_op1_init[a]: POLICY[r2_op1_policy[a]] for a in range(len(r2_op1_init))}
        r2_op2_policy = {r2_op2_init[a]: POLICY[r2_op2_policy[a]] for a in range(len(r2_op2_init))}

        r3_op1_policy = {r3_op1_init[a]: POLICY[r3_op1_policy[a]] for a in range(len(r3_op1_init))}
        r3_op2_policy = {r3_op2_init[a]: POLICY[r3_op2_policy[a]] for a in range(len(r3_op2_init))}

        r4_op1_policy = {r4_op1_init[a]: POLICY[r4_op1_policy[a]] for a in range(len(r4_op1_init))}
        r4_op2_policy = {r4_op2_init[a]: POLICY[r4_op2_policy[a]] for a in range(len(r4_op2_init))}

        room1_option1 = Option("room1_op1", 0, r1_op1_init, r1_op1_terminate, r1_op1_policy, primitive_actions=primitive_actions,
                               goal_rewards=r1_op1_goal_rewards)
        room1_option2 = Option("room1_op2", 1, r1_op2_init, r1_op2_terminate, r1_op2_policy, primitive_actions=primitive_actions,
                               goal_rewards=r1_op2_goal_rewards)

        room2_option1 = Option("room2_op1", 2, r2_op1_init, r2_op1_terminate, r2_op1_policy, primitive_actions=primitive_actions,
                               goal_rewards=r2_op1_goal_rewards)
        room2_option2 = Option("room2_op2", 3, r2_op2_init, r2_op2_terminate, r2_op2_policy, primitive_actions=primitive_actions,
                               goal_rewards=r2_op2_goal_rewards)

        room3_option1 = Option("room3_op1", 3, r3_op1_init, r3_op1_terminate, r3_op1_policy, primitive_actions=primitive_actions,
                               goal_rewards=r3_op1_goal_rewards)
        room3_option2 = Option("room3_op2", 5, r3_op2_init, r3_op2_terminate, r3_op2_policy, primitive_actions=primitive_actions,
                               goal_rewards=r3_op2_goal_rewards)


        #room4_option1 = Option("room4_op1", 6, r4_op1_init, r4_op1_terminate, r4_op1_policy, primitive_actions=primitive_actions,
        #                       goal_rewards=r4_op1_goal_rewards)
        #room4_option2 = Option("room4_op2", 7, r4_op2_init, r4_op2_terminate, r4_op2_policy, primitive_actions=primitive_actions,
        #                       goal_rewards=r4_op2_goal_rewards)



        west_room_op1_init = []

        for y in range(10):
            for x in range(10):
                west_room_op1_init.append(x+y*21)
        west_room_op1_init.remove(9+4*21)

        west_room_op1_policy = [np.random.choice(POLICY.keys()) for l in range(len(west_room_op1_init))]

        west_room_op1_terminate = [9+4*21]
        west_room_op1_goal_rewards = {9+4*21: 5}


        west_room_op1_policy = {west_room_op1_init[a]: POLICY[west_room_op1_policy[a]] for a in range(len(west_room_op1_init))}

        west_room_op1 = Option("west_room_op1", 0, west_room_op1_init, west_room_op1_terminate, west_room_op1_policy,
                               primitive_actions=primitive_actions,
                               goal_rewards=west_room_op1_goal_rewards)

        # on goal state every option should end...
        two_room_primitive_op1 = Option("primitive_op_left", 1, [], [209], [LEFT], is_primitive=True)
        two_room_primitive_op2 = Option("primitive_op_right", 2, [], [209], [RIGHT], is_primitive=True)
        two_room_primitive_op3 = Option("primitive_op_up", 3, [], [209], [UP], is_primitive=True)
        two_room_primitive_op4 = Option("primitive_op_down", 4, [], [209], [DOWN], is_primitive=True)


        # on goal state every option should end...
        primitive_op1 = Option("primitive_op_left", 4, [], [126], [LEFT], is_primitive=True)
        primitive_op2 = Option("primitive_op_right", 5, [], [126], [RIGHT], is_primitive=True)
        primitive_op3 = Option("primitive_op_up", 6, [], [126], [UP], is_primitive=True)
        primitive_op4 = Option("primitive_op_down", 7, [], [126], [DOWN], is_primitive=True)


        self.options = []

        # Two rooms options...
        self.options.append(west_room_op1)
        self.options.append(two_room_primitive_op1)
        self.options.append(two_room_primitive_op2)
        self.options.append(two_room_primitive_op3)
        self.options.append(two_room_primitive_op4)


        # option paper
        # self.options.append(room1_option1)
        # self.options.append(room1_option2)
        # self.options.append(room2_option1)
        # #self.options.append(room2_option2)
        # self.options.append(room3_option1)
        # #self.options.append(room3_option2)
        # #self.options.append(room4_option1)
        # #self.options.append(room4_option2)
        #
        # # we are adding primitive options...
        # self.options.append(primitive_op1)
        # self.options.append(primitive_op2)
        # self.options.append(primitive_op3)
        # self.options.append(primitive_op4)




        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.discount_rate = discount
        self.option_space_size = option_space_size # how many options exist
        self.state_space_dimension = [a for a in state_space_dimension]
        # state space combine with option space
        self.state_space_dimension.append(option_space_size)
        self.Q_Table = np.zeros(self.state_space_dimension, dtype=np.float32)
        # for learning internal policies...
        primitive_action_size = 4

        # do not define primitive options when a non-primitive exists
        primitive_options = []
        for opt in self.options:
            if opt.isPrimitive():
                primitive_options.append(opt)


        #print("total : "+str(len(primitive_options)))
        # for know we are applying option to one dimensional state space...
        for state in range(self.state_space_dimension[0]):
            #print("\n\nFirst state "+str(state)+"\n")
            #print(self.Q_Table[state])
            is_any_non_primitive = False
            for option in self.options:
                # if option is not defined over state
                #print("Option : "+ str(option))
                #print("Define : " +  str(option.isOptionDefineOverState(state)))



                if not option.isOptionDefineOverState(state):
                    #print("infinity")

                    self.Q_Table[state][option.getOptionId()] = -float('inf')

                else:
                    if not option.isPrimitive():
                        is_any_non_primitive = True
                    print(0)
                    self.Q_Table[state][option.getOptionId()] = 0

            if is_any_non_primitive:
                #print("one of them is non primitive")
                for pr in primitive_options:
                    #print(str(pr) + " state = infiniti\n")
                    self.Q_Table[state][pr.getOptionId()] = -float('inf')

            #print("Second\n")
            #print(self.Q_Table[state])





        if eligibility_trace == True:
            self.Eligibily_Trace = np.zeros(self.state_space_dimension, dtype=np.float32)
            self.trace_factor = trace_factor



        # if an option is not defined on a state then its corresponding table value is -infinity

    # in each step consistent options are being updated...
    def updateOptionPolicy(self, current_state, current_option, reward, next_state, current_action):

        terminal_states = current_option.getTerminationStates()
        # only when the option terminates on its terminal state than we are rewarding the option..
        if next_state in terminal_states:

            reward = current_option.getGoalRewards(next_state)
        else :
            reward = -0.001





        if (not next_state in current_option.getTerminationStates()) and (not next_state in current_option.initiation_set):

            return

        # print("reward : "+str(reward))

        next_state_utility = np.max(current_option.inner_q_table[next_state])

        current_option.inner_q_table[current_state][current_action] += \
            (self.learning_rate) * (reward + (self.discount_rate) * next_state_utility -
                                    current_option.inner_q_table[current_state][current_action])

        if reward > 0:
            print("inner Q : " + str(current_option.inner_q_table[current_state]))
            print("Q Table : " + str(self.Q_Table[current_state]))
            print("\n\ncurrent state : "+str(current_state))
            print("x : "+str(current_state%21))
            print("y : "+str(current_state/21))
            print("Q_Table 9+4*21 : "+ str(self.Q_Table[9+4*21]))
            print("Q_Table 10+4*21 : " + str(self.Q_Table[10+4*21]))

            print("\n\n")

            # print("\n\nTerminate r : " + str(reward))
            # print("Next state : " + str(next_state))
            # print("Current state : " + str(current_state) + " q = " + str(current_option.inner_q_table[current_state]))


        old_policy = current_option.policy[current_state]
        new_policy = np.argmax(current_option.inner_q_table[current_state])

        current_option.setPolicy(current_state, new_policy)

        if old_policy != new_policy:
            current_option.has_any_policy_changed = True
            current_option.policy_change_count = 0


        if reward > 0:
            if current_option.has_any_policy_changed == True:
                current_option.policy_change_count += 1
                if current_option.policy_change_count == 50000:
                    current_option.is_learning = False
                    # print("Option "+str(current_option) + " policy has converged...")





        # print("Current "+str(current_option) + " q table("+ str(current_state)+") : " +str(current_option.inner_q_table[current_state])     )


    def updateQTable(self, current_state, current_option, reward, next_state, current_action):
        if len(self.state_space_dimension) == 2:
            # current performed action over current state
            c_act = current_action # current_option.getOptionPolicy(current_state)
            # get consistent options for the current state and action

            valid_options = self.getConsistentOptionsWithState(current_state, c_act)
            # if current option is non primitive than do not update primitives...
            if not current_option.isPrimitive():
                is_any_primitive = False
                for o in valid_options:
                    if o.isPrimitive():
                        is_any_primitive = True

                if is_any_primitive:
                    return

            # print("Current state "+str(current_state))
            # print("Current action : " + str(self.POLICY[current_action]))
            # print("Valid options : ")
            # for o in valid_options:
            #     print(str(o))

            #print("\n\n")

           # exit()

            for c_option in valid_options:
                # if a non-primitive option exists do not update primitive options....

                # print("c option : "+str(c_option))
                current_option = c_option

                # print("\n\nCurrent state : " + str(current_state))
                # print("Next state : " + str(next_state))
                # print("Current option : " + str(c_option))
                # print("Current option term in next state : " + str(current_option.getTerminationFunctionValue(next_state)))

                next_state_terminal_probability = current_option.getTerminationFunctionValue(next_state)

                if current_option.isPrimitive() or current_option.isOptionTerminates(next_state):
                    next_state_utility = self.getMaxOptionValue(next_state)
                else:
                    next_state_utility = self.Q_Table[next_state][current_option.getOptionId()]


                # #
                # print("next state utility :  "+ str(next_state_utility))
                # print("Before Update")
                # print("q(current_state) : ", self.Q_Table[current_state])
                # print("q(next state) : " , self.Q_Table[next_state])
                self.Q_Table[current_state][current_option.getOptionId()] += \
                    (self.learning_rate) * (reward + (self.discount_rate) * next_state_utility -
                                          self.Q_Table[current_state][current_option.getOptionId()])

                # print("After Update")
                # print("q(current_state) : ", self.Q_Table[current_state])
                # print("q(next state) : ", self.Q_Table[next_state])





    # defined opptions are specified by assigning infinity values...

    def getMaxOptionValue(self, state):
        if len(self.state_space_dimension) == 2:
            return np.max(self.Q_Table[state])
        elif len(self.state_space_dimension) == 3:
            return np.max(self.Q_Table[state[0]][state[1]])

    # primitive actions are updated first later others...
    # If a non primitive option is defined over state then primitive one will not
    # be included ...
    def getConsistentOptionsWithState(self, state, action):

        #print("Requested State "+str(state))
        #print("Requested action : " + str(self.POLICY[action]))
        consistent_options = []
        #first primitive options
        for op in self.options:
            if op.isPrimitive():
                # print(op)
                if op.isConsistenWith(state, action):
                    consistent_options.append(op)

        non_primitives = []
        # first primitive options
        for op in self.options:
            if not op.isPrimitive():
                if op.isConsistenWith(state, action):
                    non_primitives.append(op)
        if len(non_primitives) == 0:
            pass
        else:
            consistent_options = non_primitives

        return consistent_options



    # defined opptions are specified by assigning infinity values...

    def getMaxOption(self, state):
        chosen_option = None
        if len(self.state_space_dimension) == 2:
            # print("Current state " + str(state)+ " " + str(self.Q_Table[state]))
            chosen_option = np.argmax(self.Q_Table[state])
        elif len(self.state_space_dimension) == 3:
            chosen_option = np.argmax(self.Q_Table[state[0]][state[1]])

        #print("chosen option : ", chosen_option)
        chosen_option = self.getOption(chosen_option)
        return chosen_option

    def getOption(self, option_id):
        #print("getOption : ", len(self.options))
        for op in self.options:
            #print("op : ", op.getOptionId())
            if option_id == op.getOptionId():
                return op

    # Only defined options should be returned over state...
    def sampleOption(self, current_state):
        if len(self.state_space_dimension) == 2:
            if random.random() < self.epsilon:
                defined_options = [op for op in self.options if op.isOptionDefineOverState(current_state)]
                #print("defined options : ", defined_options)

                # If a nonprimitive option is defined than choose it...
                non_primitive = [op for op in defined_options if not op.isPrimitive()]
                if len(non_primitive) == 0:
                    pass
                else:
                    defined_options = non_primitive

                ch = np.random.choice(defined_options)
                #print("random State : "+str(current_state)+" Chosen : "+str(ch))
                return ch
            else:
                #print("MaxQOption")
                mx = self.getMaxOption(current_state)
                #print("Current state : "+str(current_state)+" max chosen : "+str(mx))
                return mx
        elif len(self.state_space_dimension) == 3:
            if random.random() < self.epsilon:
                return np.random.choice(range(self.option_space_size))
            else:
                return self.getMaxOption(current_state)

    def getVisualPolicy(self):
        character = np.zeros(self.state_space_dimension[0], dtype=np.str)
        way = ['<', 'V', '>', '^']
        for state in range(self.state_space_dimension[0]):
            character[state] = way[np.argmax(self.Q_Table[state])]
        return character.reshape((4, 4))

    def getQTable(self):
        return self.Q_Table

    def getLearnedOption(self, current_state):
        return self.getMaxOption(current_state)

    def getConvergenceMetric(self):
        return np.sqrt(np.square(np.ma.masked_invalid(self.Q_Table)).sum())

    # for debuggin purposes...
    def getImportantStatesLearnedOptions(self, state_list):
        for state in state_list:
            print("State "+str(state)+" Opt "+self.getLearnedOption(state).getOptionName())

    def getImportantStatesQValues(self, state_list):
        for state in state_list:
            print("q(state="+str(state)+")=", self.Q_Table[state])


# both primitive and non primitive options are threaded equally.

class PolicyLearnerIntraOptionTable(object):

    def __init__(self, state_space_dimension, option_space_size, learning_rate, discount, epsilon,
                 eligibility_trace=False, trace_factor=0.35):


        LEFT, RIGHT, UP, DOWN = 0, 2, 3,1
        POLICY = {'<': LEFT, 'V': DOWN, '>': RIGHT, '^': UP  }
        self.POLICY = ['<', 'V', '>', '^']

        # self.action_set = [self.LEFT, self.DOWN, self.RIGHT, self.UP]
        # self.action_symbol = ['<', 'v', '>', '^']

        r1_op1_init = [14,15,16,17,18,
                       27,28,29,30,31,
                       40,41,42,43,44,
                       53,54,55,56,57,
                       66,67,68,69,70,
                          80           ]
        # random policy at the beginning...
        r1_op1_policy = [np.random.choice(POLICY.keys()) for l in range(len(r1_op1_init))]

        r1_op2_init = [14,15,16,17,18,
                       27,28,29,30,31,
                       40,41,42,43,44, 45,
                       53,54,55,56,57,
                       66,67,68,69,70  ]


        r1_op2_policy = [np.random.choice(POLICY.keys()) for l in range(len(r1_op2_init))]

        # room 2 option 1

        r2_op1_init = [20, 21, 22, 23, 24,
                       33, 34, 35, 36, 37,
                   45, 46, 47, 48, 49, 50,
                       59, 60, 61, 62, 63,
                       72, 73, 74, 75, 76,
                       85, 86, 87, 88, 89
                                       ]

        r2_op1_policy = [np.random.choice(POLICY.keys()) for l in range(len(r2_op1_init))]

        # room 2 option 2

        r2_op2_init = [20, 21, 22, 23, 24,
                       33, 34, 35, 36, 37,
                       46, 47, 48, 49, 50,
                       59, 60, 61, 62, 63,
                       72, 73, 74, 75, 76,
                       85, 86, 87, 88, 89,
                               100           ]

        r2_op2_policy = [np.random.choice(POLICY.keys()) for l in range(len(r2_op2_init))]

        # room 3 option 1

        r3_op1_init = [    80,
                       92, 93, 94, 95, 96,
                       105,106,107,108,109,
                       118,119,120,121,122,
                       131,132,133,134,135,
                       144,145,146,147,148  ]

        r3_op1_policy = [np.random.choice(POLICY.keys()) for l in range(len(r3_op1_init))]

        # room 3 option 2

        r3_op2_init = [
                       92, 93, 94, 95, 96,
                       105, 106, 107, 108, 109,
                       118, 119, 120, 121, 122,
                       131, 132, 133, 134, 135, 136,
                       144, 145, 146, 147, 148]

        r3_op2_policy = [np.random.choice(POLICY.keys()) for l in range(len(r3_op2_init))]

        # room 4 option 1

        r4_op1_init = [
                        111,112,113,114,115,
                        124,125,126,127,128,
                    136,137,138,139,140,141,
                        150,151,152,153,154  ]

        r4_op1_policy = [np.random.choice(POLICY.keys()) for l in range(len(r4_op1_init))]


        # room 4 option 2

        r4_op2_init = [         100,
                        111,112,113,114,115,
                        124,125,126,127,128,
                        137,138,139,140,141,
                        150,151,152,153,154  ]

        r4_op2_policy = [np.random.choice(POLICY.keys()) for l in range(len(r4_op2_init))]




        r1_op1_terminate = [45]
        r1_op1_goal_rewards = {45: 1}

        r1_op2_terminate = [80]
        r1_op2_goal_rewards = {80: 1}

        r2_op1_terminate = [100]
        r2_op1_goal_rewards = {100: 1}

        r2_op2_terminate = [45]
        r2_op2_goal_rewards = {45: 1}

        r3_op1_terminate = [136]
        r3_op1_goal_rewards = {136: 1}

        r3_op2_terminate = [80]
        r3_op2_goal_rewards = {80: 1}

        r4_op1_terminate = [100, 126]
        r4_op1_goal_rewards = {100: 1, 126: 1}

        r4_op2_terminate = [136, 126]
        r4_op2_goal_rewards = {136: 1, 126: 1}


        primitive_actions = [0, 1, 2, 3]


        r1_op1_policy = {r1_op1_init[a]: POLICY[r1_op1_policy[a]] for a in range(len(r1_op1_init))}
        r1_op2_policy = {r1_op2_init[a]: POLICY[r1_op2_policy[a]] for a in range(len(r1_op2_init))}

        r2_op1_policy = {r2_op1_init[a]: POLICY[r2_op1_policy[a]] for a in range(len(r2_op1_init))}
        r2_op2_policy = {r2_op2_init[a]: POLICY[r2_op2_policy[a]] for a in range(len(r2_op2_init))}

        r3_op1_policy = {r3_op1_init[a]: POLICY[r3_op1_policy[a]] for a in range(len(r3_op1_init))}
        r3_op2_policy = {r3_op2_init[a]: POLICY[r3_op2_policy[a]] for a in range(len(r3_op2_init))}

        r4_op1_policy = {r4_op1_init[a]: POLICY[r4_op1_policy[a]] for a in range(len(r4_op1_init))}
        r4_op2_policy = {r4_op2_init[a]: POLICY[r4_op2_policy[a]] for a in range(len(r4_op2_init))}

        room1_option1 = Option("room1_op1", 0, r1_op1_init, r1_op1_terminate, r1_op1_policy, primitive_actions=primitive_actions,
                               goal_rewards=r1_op1_goal_rewards)
        room1_option2 = Option("room1_op2", 1, r1_op2_init, r1_op2_terminate, r1_op2_policy, primitive_actions=primitive_actions,
                               goal_rewards=r1_op2_goal_rewards)

        room2_option1 = Option("room2_op1", 2, r2_op1_init, r2_op1_terminate, r2_op1_policy, primitive_actions=primitive_actions,
                               goal_rewards=r2_op1_goal_rewards)
        room2_option2 = Option("room2_op2", 3, r2_op2_init, r2_op2_terminate, r2_op2_policy, primitive_actions=primitive_actions,
                               goal_rewards=r2_op2_goal_rewards)

        room3_option1 = Option("room3_op1", 3, r3_op1_init, r3_op1_terminate, r3_op1_policy, primitive_actions=primitive_actions,
                               goal_rewards=r3_op1_goal_rewards)
        room3_option2 = Option("room3_op2", 5, r3_op2_init, r3_op2_terminate, r3_op2_policy, primitive_actions=primitive_actions,
                               goal_rewards=r3_op2_goal_rewards)


        #room4_option1 = Option("room4_op1", 6, r4_op1_init, r4_op1_terminate, r4_op1_policy, primitive_actions=primitive_actions,
        #                       goal_rewards=r4_op1_goal_rewards)
        #room4_option2 = Option("room4_op2", 7, r4_op2_init, r4_op2_terminate, r4_op2_policy, primitive_actions=primitive_actions,
        #                       goal_rewards=r4_op2_goal_rewards)



        west_room_op1_init = []

        for y in range(10):
            for x in range(10):
                west_room_op1_init.append(x+y*21)
        west_room_op1_init.remove(9+4*21)

        west_room_op1_policy = [np.random.choice(POLICY.keys()) for l in range(len(west_room_op1_init))]

        west_room_op1_terminate = [9+4*21]
        west_room_op1_goal_rewards = {9+4*21: 5}


        west_room_op1_policy = {west_room_op1_init[a]: POLICY[west_room_op1_policy[a]] for a in range(len(west_room_op1_init))}

        west_room_op1 = Option("west_room_op1", 0, west_room_op1_init, west_room_op1_terminate, west_room_op1_policy,
                               primitive_actions=primitive_actions,
                               goal_rewards=west_room_op1_goal_rewards)

        aisle_init = [93, 94, 95]
        aisle_terminate = [96]
        aisle_policy = [np.random.choice(POLICY.keys()) for i in range(3)]
        aisle_goal_rewards = {96: 1}

        aisle_policy = {aisle_init[a]: POLICY[aisle_policy[a]] for a in range(len(aisle_init))}

        aisle_option = Option("aisle_option", 5, aisle_init, aisle_terminate, aisle_policy,
                               primitive_actions=primitive_actions,
                               goal_rewards=aisle_goal_rewards)

        # on goal state every option should end...
        two_room_primitive_op1 = Option("primitive_op_left", 1, [], [209], [LEFT], is_primitive=True)
        two_room_primitive_op2 = Option("primitive_op_right", 2, [], [209], [RIGHT], is_primitive=True)
        two_room_primitive_op3 = Option("primitive_op_up", 3, [], [209], [UP], is_primitive=True)
        two_room_primitive_op4 = Option("primitive_op_down", 4, [], [209], [DOWN], is_primitive=True)





        # on goal state every option should end...
        primitive_op1 = Option("primitive_op_left", 4, [], [126], [LEFT], is_primitive=True)
        primitive_op2 = Option("primitive_op_right", 5, [], [126], [RIGHT], is_primitive=True)
        primitive_op3 = Option("primitive_op_up", 6, [], [126], [UP], is_primitive=True)
        primitive_op4 = Option("primitive_op_down", 7, [], [126], [DOWN], is_primitive=True)


        self.options = []

        # Two rooms options...
        self.options.append(west_room_op1)
        self.options.append(two_room_primitive_op1)
        self.options.append(two_room_primitive_op2)
        self.options.append(two_room_primitive_op3)
        self.options.append(two_room_primitive_op4)

        self.options.append(aisle_option)


        # option paper
        # self.options.append(room1_option1)
        # self.options.append(room1_option2)
        # self.options.append(room2_option1)
        # #self.options.append(room2_option2)
        # self.options.append(room3_option1)
        # #self.options.append(room3_option2)
        # #self.options.append(room4_option1)
        # #self.options.append(room4_option2)
        #
        # # we are adding primitive options...
        # self.options.append(primitive_op1)
        # self.options.append(primitive_op2)
        # self.options.append(primitive_op3)
        # self.options.append(primitive_op4)




        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.discount_rate = discount
        self.option_space_size = option_space_size # how many options exist
        self.state_space_dimension = [a for a in state_space_dimension]
        # state space combine with option space
        self.state_space_dimension.append(option_space_size)
        self.Q_Table = np.zeros(self.state_space_dimension, dtype=np.float32)
        # for learning internal policies...
        primitive_action_size = 4

        # define primitive options when a non-primitive exists
        primitive_options = []


        #print("total : "+str(len(primitive_options)))
        # for know we are applying option to one dimensional state space...
        for state in range(self.state_space_dimension[0]):
            #print("\n\nFirst state "+str(state)+"\n")
            #print(self.Q_Table[state])
            is_any_non_primitive = False
            for option in self.options:

                if not option.isOptionDefineOverState(state):
                    #print("infinity")

                    self.Q_Table[state][option.getOptionId()] = -float('inf')

                else:
                    self.Q_Table[state][option.getOptionId()] = 0

        if eligibility_trace == True:
            self.Eligibily_Trace = np.zeros(self.state_space_dimension, dtype=np.float32)
            self.trace_factor = trace_factor

        # if an option is not defined on a state then its corresponding table value is -infinity

    # in each step consistent options are being updated...
    def updateOptionPolicy(self, current_state, current_option, reward, next_state, current_action):

        terminal_states = current_option.getTerminationStates()
        # only when the option terminates on its terminal state than we are rewarding the option..
        if next_state in terminal_states:

            reward = current_option.getGoalRewards(next_state)
        else :
            reward = -0.001


        # when agent lives option regions, no update is performed...
        if (not next_state in current_option.getTerminationStates()) and (not next_state in current_option.initiation_set):

            return

        next_state_utility = np.max(current_option.inner_q_table[next_state])

        current_option.inner_q_table[current_state][current_action] += \
            (self.learning_rate) * (reward + (self.discount_rate) * next_state_utility -
                                    current_option.inner_q_table[current_state][current_action])

        if reward > 0:
            print("inner Q : " + str(current_option.inner_q_table[current_state]))
            print("Q Table : " + str(self.Q_Table[current_state]))
            print("\n\ncurrent state : "+str(current_state))
            print("x : "+str(current_state%21))
            print("y : "+str(current_state/21))
            print("Q_Table 9+4*21 : "+ str(self.Q_Table[9+4*21]))
            print("Q_Table 10+4*21 : " + str(self.Q_Table[10+4*21]))

            print("\n\n")

            # print("\n\nTerminate r : " + str(reward))
            # print("Next state : " + str(next_state))
            # print("Current state : " + str(current_state) + " q = " + str(current_option.inner_q_table[current_state]))


        old_policy = current_option.policy[current_state]
        new_policy = np.argmax(current_option.inner_q_table[current_state])

        current_option.setPolicy(current_state, new_policy)

        if old_policy != new_policy:
            current_option.has_any_policy_changed = True
            current_option.policy_change_count = 0

                    # print("Option "+str(current_option) + " policy has converged...")


    def updateQTable(self, current_state, current_option, reward, next_state, current_action):
        if len(self.state_space_dimension) == 2:
            # current performed action over current state
            c_act = current_action # current_option.getOptionPolicy(current_state)
            # get consistent options for the current state and action

            valid_options = self.getConsistentOptionsWithState(current_state, c_act)
            # if current option is non primitive than update also primitives...


            for c_option in valid_options:
                # if a non-primitive option exists do not update primitive options....

                # print("c option : "+str(c_option))
                current_option = c_option

                # print("\n\nCurrent state : " + str(current_state))
                # print("Next state : " + str(next_state))
                # print("Current option : " + str(c_option))
                # print("Current option term in next state : " + str(current_option.getTerminationFunctionValue(next_state)))

                next_state_terminal_probability = current_option.getTerminationFunctionValue(next_state)

                if current_option.isPrimitive() or current_option.isOptionTerminates(next_state):
                    next_state_utility = self.getMaxOptionValue(next_state)
                else:
                    next_state_utility = self.Q_Table[next_state][current_option.getOptionId()]


                # #
                # print("next state utility :  "+ str(next_state_utility))
                # print("Before Update")
                # print("q(current_state) : ", self.Q_Table[current_state])
                # print("q(next state) : " , self.Q_Table[next_state])
                self.Q_Table[current_state][current_option.getOptionId()] += \
                    (self.learning_rate) * (reward + (self.discount_rate) * next_state_utility -
                                          self.Q_Table[current_state][current_option.getOptionId()])

                # print("After Update")
                # print("q(current_state) : ", self.Q_Table[current_state])
                # print("q(next state) : ", self.Q_Table[next_state])





    # defined opptions are specified by assigning infinity values...

    def getMaxOptionValue(self, state):
        if len(self.state_space_dimension) == 2:
            return np.max(self.Q_Table[state])
        elif len(self.state_space_dimension) == 3:
            return np.max(self.Q_Table[state[0]][state[1]])

    # primitive actions are updated first later others...
    # If a non primitive option is defined over state then primitive one will also
    # be included ...
    def getConsistentOptionsWithState(self, state, action):

        #print("Requested State "+str(state))
        #print("Requested action : " + str(self.POLICY[action]))
        consistent_options = []
        #first primitive options
        for op in self.options:
            if op.isPrimitive():
                # print(op)
                if op.isConsistenWith(state, action):
                    consistent_options.append(op)

        non_primitives = []
        # first primitive options
        for op in self.options:
            if not op.isPrimitive():
                if op.isConsistenWith(state, action):
                    non_primitives.append(op)

        return consistent_options



    # defined opptions are specified by assigning infinity values...
    def getMaxOption(self, state):
        chosen_option = None
        if len(self.state_space_dimension) == 2:
            # print("Current state " + str(state)+ " " + str(self.Q_Table[state]))
            chosen_option = np.argmax(self.Q_Table[state])
        elif len(self.state_space_dimension) == 3:
            chosen_option = np.argmax(self.Q_Table[state[0]][state[1]])

        #print("chosen option : ", chosen_option)
        chosen_option = self.getOption(chosen_option)
        return chosen_option

    def getOption(self, option_id):
        #print("getOption : ", len(self.options))
        for op in self.options:
            #print("op : ", op.getOptionId())
            if option_id == op.getOptionId():
                return op

    # Only defined options should be returned over state...
    def sampleOption(self, current_state):
        if len(self.state_space_dimension) == 2:
            if random.random() < self.epsilon:
                defined_options = [op for op in self.options if op.isOptionDefineOverState(current_state)]
                #print("defined options : ", defined_options)

                # all options could be chosen...
                non_primitive = [op for op in defined_options]


                ch = np.random.choice(defined_options)
                return ch
            else:
                mx = self.getMaxOption(current_state)
                #print("Current state : "+str(current_state)+" max chosen : "+str(mx))
                return mx
        elif len(self.state_space_dimension) == 3:
            if random.random() < self.epsilon:
                return np.random.choice(range(self.option_space_size))
            else:
                return self.getMaxOption(current_state)

    def getVisualPolicy(self):
        character = np.zeros(self.state_space_dimension[0], dtype=np.str)
        way = ['<', 'V', '>', '^']
        for state in range(self.state_space_dimension[0]):
            character[state] = way[np.argmax(self.Q_Table[state])]
        return character.reshape((4, 4))

    def getQTable(self):
        return self.Q_Table

    def getLearnedOption(self, current_state):
        return self.getMaxOption(current_state)

    def getConvergenceMetric(self):
        return np.sqrt(np.square(np.ma.masked_invalid(self.Q_Table)).sum())

    # for debuggin purposes...
    def getImportantStatesLearnedOptions(self, state_list):
        for state in state_list:
            print("State "+str(state)+" Opt "+self.getLearnedOption(state).getOptionName())

    def getImportantStatesQValues(self, state_list):
        for state in state_list:
            print("q(state="+str(state)+")=", self.Q_Table[state])



# both primitive and non primitive options are threaded equally.
# on request this class creates required fields for new option on table...
# table starts with only primitive options and sequentially new options are added to current setting
# new options' policies are retrieved from primitive option policy by buffer replay...

class DynamicPolicyLearnerIntraOptionTable(object):

    def __init__(self, state_space_dimension, learning_rate, discount, epsilon,
                 eligibility_trace=False, trace_factor=0.35):

        # this policy data will be taken from environment...
        LEFT, RIGHT, UP, DOWN = 0, 2, 3,1
        self.POLICY_MAP = {'<': LEFT, 'V': DOWN, '>': RIGHT, '^': UP  }
        self.POLICY_NAME = {'<': "LEFT", "V": "DOWN", ">": "RIGHT", "^": "UP"}
        self.POLICY_SYMBOLS = ['<', 'V', '>', '^']
        self.PRIMITIVE_POLICY = [LEFT, DOWN, RIGHT, UP]

        terminal_states = [209]
        self.current_option_count = 0
        primitive_action_size = 4


        self.primitive_options = []

        self.options = []


        # on goal state every option should end...
        for action in self.POLICY_MAP.keys():
            primitive_opt = Option("primitive_option_"+str(self.POLICY_NAME[action]),
                                   self.current_option_count,
                                   [],
                                   terminal_states,
                                   [self.POLICY_MAP[action]],
                                   is_primitive=True)
            self.options.append(primitive_opt)
            self.current_option_count += 1


        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.discount_rate = discount
        self.state_space_dimension = [a for a in state_space_dimension]
        # state space combine with option space
        self.state_space_dimension.append(self.current_option_count)
        self.Q_Table = np.zeros(self.state_space_dimension, dtype=np.float32)
        # for learning internal policies...

        # non primitive options will be shown...
        self.option_information = {}
        self.option_colors = [(128, 0, 0), (255, 0, 0), (0, 128, 0), (0, 255, 0), (0, 0, 128), (0, 0, 255),
                               (128, 128, 0), (128, 0, 128), (0, 128, 128), (128, 128, 128), (255, 255, 0),
                               (0, 255, 255), (255, 0, 255), (128, 255, 255), (255, 128, 255), (255, 255, 128),
                               (128, 0, 255)]

        # for know we are applying option to one dimensional state space...
        for state in range(self.state_space_dimension[0]):
            #print("\n\nFirst state "+str(state)+"\n")
            #print(self.Q_Table[state])
            is_any_non_primitive = False
            for option in self.options:

                if not option.isOptionDefineOverState(state):
                    #print("infinity")

                    self.Q_Table[state][option.getOptionId()] = -float('inf')

                else:
                    self.Q_Table[state][option.getOptionId()] = 0

        if eligibility_trace == True:
            self.Eligibily_Trace = np.zeros(self.state_space_dimension, dtype=np.float32)
            self.trace_factor = trace_factor




        # no need for reward bacause pseudo reward will be applied..
        # state : [[next_state, action] ]
        self.experience_history = {}
    def addExperience(self, current_state, next_state, action):

        if not self.experience_history.has_key(current_state):
            self.experience_history[current_state] = []
        self.experience_history[current_state].append([next_state, action])

    def getOptionwithName(self, option_name):
        for opt in self.options:
            if opt.getOptionName() == option_name:
                return opt


    def applyExperienceReplayOnOption(self, option_name):
        option = self.getOptionwithName(option_name)
        terminate_state = option.termination_function
        initiation_set = option.initiation_set

        processed_states = [ ]
        learning_batch = []
        affected_states = set()

        state_process_times = {a: 0 for a in initiation_set}

        while True:
            # print("terminate state " +str(terminate_state))
            for target_state in terminate_state:

                # find state transition that goes into terminal state of the option...
                for state in initiation_set:
                    if self.experience_history.has_key(state):
                        for next_state in self.experience_history[state]:
                            if next_state[0] == target_state:
                                learning_batch.append([state, next_state[0], next_state[1]])

            print("Learning batch is okay...")
            # print(learning_batch)
            for curr_state, nt_state, action in learning_batch:
                self.updateOptionPolicy(curr_state, option, 0.0, nt_state , action)
                affected_states.add(curr_state)

            affected_states = list(affected_states)
            # print("affected state : "+str(affected_states))
            exclude_states = []
            terminate_state = [a for a in affected_states]
            affected_states = set()
            learning_batch = []
            for st in terminate_state:
                state_process_times[st] += 1
                if state_process_times[st] >= 4:
                    exclude_states.append(st)

            for l in exclude_states:
                terminate_state.remove(l)
            if len(terminate_state) == 0:
                break

            print("terminate len : "+str(len(terminate_state)))


    # if an option is not defined on a state then its corresponding table value is -infinity
    # Option("aisle_option", 5, aisle_init, aisle_terminate, aisle_policy,
    #        primitive_actions=primitive_actions,
    #        goal_rewards=aisle_goal_rewards)

    # we don't add primitive options...
    def addNewOption(self, option_name, option_init, option_termination, goal_rewards):
        new_option = None
        new_option_id = self.current_option_count
        new_option_policy = {}

        policy_option_values = {}

        for state in option_init:
            # get best options policy over the state...
            max_opt = self.getMaxOption(state)
            if max_opt.isPrimitive():
                new_option_policy[state] = max_opt.policy[0]
            else:
                new_option_policy[state] = max_opt.policy[state]

            policy_option_values[state] = self.getMaxOptionValue(state)

        new_option_column = np.zeros((self.state_space_dimension[0], 1), dtype=np.float32)

        for i in range(self.state_space_dimension[0]):
            if i in option_init:
                new_option_column[i][0] = policy_option_values[i]
            else:
                new_option_column[i][0] = -float('inf')

        new_option = Option(option_name, new_option_id, option_init, option_termination, new_option_policy, self.PRIMITIVE_POLICY, goal_rewards)

        # option values are added to option table...
        self.Q_Table = np.hstack((self.Q_Table, new_option_column))

        self.option_information[option_name] = {"subgoal": goal_rewards.keys()[0] , "initiation_set": option_init, "color": self.option_colors[new_option_id%len(self.option_colors)]}

        self.options.append(new_option)
        self.current_option_count += 1

    def getOptionInformation(self):
        return self.option_information

    # in each step consistent options are being updated...
    def updateOptionPolicy(self, current_state, current_option, reward, next_state, current_action):

        terminal_states = current_option.getTerminationStates()
        # only when the option terminates on its terminal state than we are rewarding the option..
        if next_state in terminal_states:

            reward = current_option.getGoalRewards(next_state)
        else :
            reward = -0.001
        # when agent lives option regions, no update is performed...
        if (not next_state in current_option.getTerminationStates()) and (not next_state in current_option.initiation_set):

            return

        next_state_utility = np.max(current_option.inner_q_table[next_state])

        current_option.inner_q_table[current_state][current_action] += \
            (self.learning_rate) * (reward + (self.discount_rate) * next_state_utility -
                                    current_option.inner_q_table[current_state][current_action])

        # if reward > 0:
        #     print("inner Q : " + str(current_option.inner_q_table[current_state]))
        #     print("Q Table : " + str(self.Q_Table[current_state]))
        #     print("\n\ncurrent state : "+str(current_state))
        #     print("x : "+str(current_state%21))
        #     print("y : "+str(current_state/21))
        #     print("Q_Table 9+4*21 : "+ str(self.Q_Table[9+4*21]))
        #     print("Q_Table 10+4*21 : " + str(self.Q_Table[10+4*21]))
        #
        #     print("\n\n")
        #
        #     # print("\n\nTerminate r : " + str(reward))
        #     # print("Next state : " + str(next_state))
        #     # print("Current state : " + str(current_state) + " q = " + str(current_option.inner_q_table[current_state]))


        old_policy = current_option.policy[current_state]
        new_policy = np.argmax(current_option.inner_q_table[current_state])

        current_option.setPolicy(current_state, new_policy)

        if old_policy != new_policy:
            current_option.has_any_policy_changed = True
            current_option.policy_change_count = 0

                    # print("Option "+str(current_option) + " policy has converged...")

    def updateQTable(self, current_state, current_option, reward, next_state, current_action):
        if len(self.state_space_dimension) == 2:
            # current performed action over current state
            c_act = current_action # current_option.getOptionPolicy(current_state)
            # get consistent options for the current state and action

            valid_options = self.getConsistentOptionsWithState(current_state, c_act)
            # if current option is non primitive than update also primitives...


            for c_option in valid_options:
                # if a non-primitive option exists do not update primitive options....

                # print("c option : "+str(c_option))
                current_option = c_option

                # print("\n\nCurrent state : " + str(current_state))
                # print("Next state : " + str(next_state))
                # print("Current option : " + str(c_option))
                # print("Current option term in next state : " + str(current_option.getTerminationFunctionValue(next_state)))

                next_state_terminal_probability = current_option.getTerminationFunctionValue(next_state)

                if current_option.isPrimitive() or current_option.isOptionTerminates(next_state):
                    next_state_utility = self.getMaxOptionValue(next_state)
                else:
                    next_state_utility = self.Q_Table[next_state][current_option.getOptionId()]


                # #
                # print("next state utility :  "+ str(next_state_utility))
                # print("Before Update")
                # print("q(current_state) : ", self.Q_Table[current_state])
                # print("q(next state) : " , self.Q_Table[next_state])
                self.Q_Table[current_state][current_option.getOptionId()] += \
                    (self.learning_rate) * (reward + (self.discount_rate) * next_state_utility -
                                          self.Q_Table[current_state][current_option.getOptionId()])

                # print("After Update")
                # print("q(current_state) : ", self.Q_Table[current_state])
                # print("q(next state) : ", self.Q_Table[next_state])





    # defined opptions are specified by assigning infinity values...

    # def getMaxOptionValue(self, state):
    #     if len(self.state_space_dimension) == 2:
    #         return np.max(self.Q_Table[state])
    #     elif len(self.state_space_dimension) == 3:
    #         return np.max(self.Q_Table[state[0]][state[1]])

    # primitive actions are updated first later others...
    # If a non primitive option is defined over state then primitive one will also
    # be included ...
    def getConsistentOptionsWithState(self, state, action):

        #print("Requested State "+str(state))
        #print("Requested action : " + str(self.POLICY[action]))
        consistent_options = []
        #first primitive options
        for op in self.options:
            if op.isPrimitive():
                # print(op)
                if op.isConsistenWith(state, action):
                    consistent_options.append(op)

        non_primitives = []
        # first primitive options
        for op in self.options:
            if not op.isPrimitive():
                if op.isConsistenWith(state, action):
                    consistent_options.append(op)

        return consistent_options



    # defined opptions are specified by assigning infinity values...
    def getMaxOption(self, state):
        chosen_option = None
        if len(self.state_space_dimension) == 2:
            # there migth be two or more options values of which are equal causes bias, so among those
            # we are choosing randomly...
            Q_values = self.Q_Table[state]
            all_indices = np.argwhere(Q_values==np.max(Q_values))
            equal_indices = all_indices.flatten().tolist()
            #if np.any(equal_indices <= 0.6):
            # non primitive optionis are superior to primitive ones..
            prior_options = []
            if len(equal_indices) > 1:
                for ind in equal_indices:
                    if ind > 3:
                        prior_options.append(ind)
                if len(prior_options) > 0: equal_indices = prior_options
                chosen_option = np.random.choice(equal_indices)
            else:
                chosen_option = equal_indices[0]

            # chosen_option = np.argmax(Q_values)

        elif len(self.state_space_dimension) == 3:
            chosen_option = np.argmax(self.Q_Table[state[0]][state[1]])

        #print("chosen option : ", chosen_option)
        chosen_option = self.getOption(chosen_option)
        return chosen_option

    # defined opptions are specified by assigning infinity values...
    def getMaxOptionValue(self, state):
            chosen_option = None
            if len(self.state_space_dimension) == 2:
                # there migth be two or more options values of which are equal causes bias, so among those
                # we are choosing randomly...
                Q_values = self.Q_Table[state]
                all_indices = np.argwhere(Q_values == np.max(Q_values))
                equal_indices = all_indices.flatten().tolist()
                return np.max(Q_values)



    def getOption(self, option_id):
        #print("getOption : ", len(self.options))
        for op in self.options:
            #print("op : ", op.getOptionId())
            if option_id == op.getOptionId():
                return op

    # Only defined options should be returned over state...
    def sampleOption(self, current_state):
        if len(self.state_space_dimension) == 2:
            if random.random() < self.epsilon:
                defined_options = [op for op in self.options if op.isOptionDefineOverState(current_state)]
                #print("defined options : ", defined_options)

                # all options could be chosen...
                non_primitive = [op for op in defined_options]


                ch = np.random.choice(defined_options)
                return ch
            else:
                mx = self.getMaxOption(current_state)
                #print("Current state : "+str(current_state)+" max chosen : "+str(mx))
                return mx
        elif len(self.state_space_dimension) == 3:
            if random.random() < self.epsilon:
                return np.random.choice(range(self.option_space_size))
            else:
                return self.getMaxOption(current_state)

    def getVisualPolicy(self):
        character = np.zeros(self.state_space_dimension[0], dtype=np.str)
        way = ['<', 'V', '>', '^']
        for state in range(self.state_space_dimension[0]):
            character[state] = way[np.argmax(self.Q_Table[state])]
        return character.reshape((4, 4))

    def getQTable(self):
        return self.Q_Table

    def getLearnedOption(self, current_state):
        return self.getMaxOption(current_state)

    def getConvergenceMetric(self):
        return np.sqrt(np.square(np.ma.masked_invalid(self.Q_Table)).sum())

    # for debuggin purposes...
    def getImportantStatesLearnedOptions(self, state_list):
        for state in state_list:
            print("State "+str(state)+" Opt "+self.getLearnedOption(state).getOptionName())

    def getImportantStatesQValues(self, state_list):
        for state in state_list:
            print("q(state="+str(state)+")=", self.Q_Table[state])

