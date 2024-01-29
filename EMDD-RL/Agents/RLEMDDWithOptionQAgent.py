import networkx as nx
import numpy as np
import Agents.RLAgent
import networkx as nx
import Tables.QTable
import Tables.OptionQTable
import MIL.Methods.EMDD as EMDD
import MIL.Methods.DD as DiverseDensity
# starting state is not included in trajectory....
class RLEMDDWithOptionQAgent(Agents.RLAgent.RLAgent):

    def __init__(self, environment, learning_rate, epsilon, discount_factor):
        super(RLEMDDWithOptionQAgent, self).__init__(environment, learning_rate, epsilon, discount_factor)
        self.state_space_dimensions = environment.getStateSpaceDimensions()
        primitive_action_space_size = environment.getActionSpaceSize()

        self.DynamicPolicyLearnerIntraOption_Table = Tables.OptionQTable.DynamicPolicyLearnerIntraOptionTable(
            self.state_space_dimensions, learning_rate,
            discount_factor, epsilon)  # trace factor 0.35
        self.environment = environment
        self.current_option = None

        self.current_action = None
        self.current_state = None

        self.option_step_count = 0
        self.option_accumulated_reward = 0
        self.option_started_state = None
        self.is_all_options_converged = False

        # how many previous states will be considered for initiation set when the current state is identified as target....

        self.OPTION_LAG = 5

        # tp parameter : how many times a stated is identified as hit...
        self.subgoal_candidates = {}

        # positive bag and negative bags of the diverse density...
        # the trajectories reached goal will be saved in positive bag...

        # we might count episode steps, after some threshold, we might deem current trajectory as negative...

        self.positive_bag = []
        self.negative_bag = []

        # max step number at which current trajectory is deemed to be negative...
        # in paper there is no limitation on steps... due to environment every episode is successfull...
        self.MAX_STEP_COUNT = 1000

        self.subgoals = []

        # when a state becomes a hit, we save its inititaion set candidates according to paper...
        # state : set([states...])
        self.subgoal_initiation_sets = {}

        self.state_observation_count = {}
        # for selecting initiation set for subgoal, previous states will be inspected...
        self.episode_history = []
        # after how many episodes later EMDD algorithm will be running..
        self.EMDD_EPISODE_THRESHOLD_COUNT = 20
        self.episode_count = 0
        self.positive_bag_state_counts = []
        self.negative_bag_state_counts = []
        self.positive_bag_count = 0
        self.negative_bag_count = 0

        self.episodic_state_counts = {}
        self.traversed_states = set()
        # to accept a state as a goal, threshold of the running average of concept..

        # static filter, states that are near to goal appear in trajectories frequently, choosing these states
        # as subgoal will have no benefit
        self.excluded_states = set([0, 1, 2, 3,
                                    21,22,23,24,
                                    42, 43, 44, 45,
                                    63, 64, 65, 66,

                                    143, 144, 145, 146,
                                    164, 165, 166, 167,
                                    185, 186, 187, 188,
                                    206, 207, 208, 209

                                    ])
        # how many previous steps before goal and starting state will be eliminated for subgoal
        self.state_exclusion_radius = 4
        self.lambda_parameter = 0.6
        self.DD_AVERAGE_THRESOLD = self.lambda_parameter / float(1.0-self.lambda_parameter)-0.04

        # state : value
        # c = lambda*(c+1)
        self.state_averages = {}

        # states that were visited during last episode..
        self.last_traversed_states = set()
        self.last_episode_sequence = []
        self.OPTION_COUNT_LIMIT = 1
        self.G = nx.Graph()
        self.first_graph_construnction = True
        #distance source
        self.DS = None



        self.graph_update_frequency = 3
        self.graph_update_count = 0
        # instances
        self.option_creation_history = []

        self.episode_counter = 0


    # when episode finishes, option also terminates...
    # so after each termination, a start option must be chosen among the available one in the starting state
    def preEpisode(self):
        super(RLEMDDWithOptionQAgent, self).preEpisode()
        self.current_option = self.DynamicPolicyLearnerIntraOption_Table.sampleOption(
            self.environment.getCurrentState())
        self.option_started_state = self.environment.getCurrentState()
        self.option_step_count = 0
        self.option_accumulated_reward = 0
        # adding starting state...
        self.episode_history.append(self.option_started_state)
        # in each episode we count each state occurence in trajectory,
        # for adequte counting... rather than counting in all batches,
        self.episodic_state_counts[self.option_started_state] = 1
        self.traversed_states.add(self.option_started_state)

        self.episode_counter += 1

    def preAction(self, state):
        # if option terminates than choose the one consistent with the current state
        # accordingto e greedy approach...
        self.current_action = self.current_option.getOptionPolicy(state)
        self.current_state = state
        return self.current_action

    def afterAction(self, next_state, reward):
        super(RLEMDDWithOptionQAgent, self).afterAction(next_state, reward)
        self.DynamicPolicyLearnerIntraOption_Table.addExperience(self.current_state, next_state,
                                                                 self.current_action)
        # increase current state's observation count..
        # if next_state != self.current_state:
        self.traversed_states.add(next_state)
        self.episode_history.append(next_state)
        if not self.episodic_state_counts.has_key(next_state):
            self.episodic_state_counts[next_state] = 1
        else:
            self.episodic_state_counts[next_state] += 1
        if next_state in self.state_observation_count.keys():
            self.state_observation_count[next_state] += 1
        else:
            self.state_observation_count[next_state] = 1

        # If chosen option is not primitive, adjust its policy...
        pol_ = {}
        for st in range(self.state_space_dimensions[0]):
            if st in self.environment.environment.unused_states:
                continue
            max_opt = self.DynamicPolicyLearnerIntraOption_Table.getMaxOption(st)
            if max_opt.isPrimitive():
                pol_[st] = max_opt.policy[0]
        self.environment.setEnablePolicyDisplay(True)
        self.environment.setDisplayPolicy(pol_)
        if not self.current_option.isPrimitive():
            # we do not wait option to converge...
            # if self.current_option.is_learning == True:
            # print("Non primitive Option")
            # print("Reward : "+str(reward))
            self.DynamicPolicyLearnerIntraOption_Table.updateOptionPolicy(self.current_state, self.current_option,
                                                                          reward, next_state, self.current_action)
            for o in self.current_option.policy.keys():
                pol_[o] = self.current_option.policy[o]

        self.DynamicPolicyLearnerIntraOption_Table.updateQTable(self.current_state, self.current_option, reward,
                                                                next_state, self.current_action)

        # primitive actions last only one step...
        if self.current_option.isOptionTerminates(next_state) or self.current_option.isPrimitive():
            self.current_option = self.DynamicPolicyLearnerIntraOption_Table.sampleOption(next_state)



    def createTransitionGraph(self):
        if self.first_graph_construnction:
            for pos in self.positive_bag:
                for i in range(1, len(pos)):
                    c = pos[i-1]
                    n = pos[i]
                    if not self.G.has_edge(c,n):
                        self.G.add_edge(c, n, weight=1)

            for neg in self.negative_bag:
                for i in range(1, len(neg)):
                    c = neg[i-1]
                    n = neg[i]
                    if not self.G.has_edge(c,n):
                        self.G.add_edge(c, n, weight=1)

            self.first_graph_construnction = False
        else:
            for i in range(1, len(self.episode_history)):
                c = self.episode_history[i - 1]
                n = self.episode_history[i]
                if not self.G.has_edge(c, n):
                    self.G.add_edge(c, n, weight=1)

    def findInitiationSet(self, goal):
        init_set = set()
        # both in negative and positive bags the goal is search to extract initiation set...
        for bag in self.positive_bag+self.negative_bag:
            bag = list(bag)
            goal_index = 0
            if goal in bag:
                while(bag[goal_index] != goal):
                    goal_index += 1
                if goal_index-1-self.OPTION_LAG-1 < 0:
                    state = bag[: goal_index]
                else:
                    state = bag[goal_index-self.OPTION_LAG:goal_index]
                for j in state:
                    init_set.add(j)
        return init_set

    def calculateEMDD(self):
        # discard states close to goal and start state...
        # max value is the output of DD search
        max_value = -float('inf')
        max_dd_state = None
        # print("Excluded states : "+str(self.excluded_states))
        # last episode history is used to find
        #if option limit is reached tham do not waste time and resources for further calculation
        if len(self.DynamicPolicyLearnerIntraOption_Table.options) - 4 >= self.OPTION_COUNT_LIMIT:
            return
        positive_bags = [list(set([i for i in  bag if not i in self.excluded_states])) for bag in self.positive_bag]
        negative_bags = [list(set([i for i in bag if not i in self.excluded_states])) for bag in self.negative_bag]

        STATES_TO_TEST = []
        # populate transition graph
        self.createTransitionGraph()

        if self.graph_update_count % self.graph_update_frequency == 0:
            self.DS = DistanceSource(self.G)

        self.graph_update_count += 1
        emdd = EMDD.EMDD(positive_bags, negative_bags, self.DS, STATES_TO_TEST, EMDD.EMDD.EXPONENTIAL,
                    distance_metric=DiverseDensity.DiverseDensity.DISTANCE_METRIC_GRAPH,
                    H_CHECK=EMDD.EMDD.H_SET, SKIPPING_FACTOR=2, DISTANCE_SOURCE=EMDD.EMDD.INDIRECT_DISTANCE)

        max_dd, max_dd_value = emdd()
        print("Max dd state : %d DD value %.3f" %(max_dd, max_dd_value))
        max_states = [max_dd]

        for max_dd_state in max_states:
            if not self.state_averages.has_key(max_dd_state):
                self.state_averages[max_dd_state] = self.lambda_parameter*(0.0+1.0)
            else:
                self.state_averages[max_dd_state] = self.lambda_parameter*(self.state_averages[max_dd_state] + 1.0)

            print("DD(%i)=%f" %(max_dd_state, max_dd_value))
            print("C^(%d) = %f" % (max_dd_state, self.state_averages[max_dd_state]))

            # if concept is early and persistent then create a new option for this state....
            if self.state_averages[max_dd_state] > self.DD_AVERAGE_THRESOLD:
                # find initiation set.....
                if not self.subgoal_candidates.has_key(max_dd_state):
                    self.subgoal_candidates[max_dd_state] = 0

                self.subgoal_candidates[max_dd_state] += 1
                self.environment.setDisplaySubgoal(self.subgoal_candidates)
                self.environment.setEnableSubgoalDisplay(True)

                # paper limits option number created... 4 primitive already
                if len(self.DynamicPolicyLearnerIntraOption_Table.options)-4 < self.OPTION_COUNT_LIMIT:

                    # for testing purposes we are not adding any option...
                    new_op_init = self.findInitiationSet(max_dd_state)

                    self.subgoals.append(max_dd_state)
                    s = max_dd_state
                    new_op_init = list(new_op_init)
                    if max_dd_state in new_op_init:
                        new_op_init.remove(max_dd_state)

                    new_op_terminate = [s]
                    new_option_goal_rewards = {s: 5}

                    print("*****************Subgoal " + str(s) + " added...")
                    print("Initiation set " + str(new_op_init))

                    self.DynamicPolicyLearnerIntraOption_Table.addNewOption("non_primitive" + str(s), new_op_init,
                                                                            new_op_terminate,
                                                                           new_option_goal_rewards)

                    self.DynamicPolicyLearnerIntraOption_Table.applyExperienceReplayOnOption("non_primitive" + str(s))
                    self.environment.setEnableOptionDisplay(True)
                    self.environment.setDisplayOption(self.DynamicPolicyLearnerIntraOption_Table.getOptionInformation())
                    self.option_creation_history.append(self.episode_counter)

    def afterEpisode(self):
            super(RLEMDDWithOptionQAgent, self).afterEpisode()
            # those are the
            for a in self.episode_history[-self.state_exclusion_radius: ]:
                pass
                #self.excluded_states.add(a)

            # if there is only one starting state the same state exclusion strategy is valid...
            if len(self.environment.getStartingStates()) == 1:
                for a in self.episode_history[0: self.state_exclusion_radius]:
                    pass
                    #self.excluded_states.add(a)

            self.last_traversed_states = set(self.episode_history)
            if self.environment.isSuccessfullFinish():
                print("Succesful finish")
                self.positive_bag.append(self.episode_history)
                self.positive_bag_state_counts.append(self.episodic_state_counts)

            else:
                print("unsuccesfull finish")
                self.negative_bag.append(self.episode_history)
                self.negative_bag_state_counts.append(self.episodic_state_counts)

            self.episode_count += 1
            # wait till at least one positive bag is retrieved...
            if self.episode_count >= self.EMDD_EPISODE_THRESHOLD_COUNT and (len(self.positive_bag) > 1):
                self.calculateEMDD()

            # clear current episode history for next episode..
            self.episode_history = []

    def getVisualPolicy(self):
        pol_ = {}
        for st in range(self.state_space_dimensions[0]):
            if st in self.environment.environment.unused_states:
                continue
            max_opt = self.DynamicPolicyLearnerIntraOption_Table.getMaxAction(st)

            # if max_opt.isPrimitive():
            #    pol_[st] = max_opt.policy[0]
            # else:
            #    pol_[st] = max_opt.policy[st]
            pol_[st] = max_opt
        self.environment.setEnablePolicyDisplay(True)
        self.environment.setDisplayPolicy(pol_)
        self.environment.renderEnvironment()
        raw_input("")
        return ""

    def getLearnedAction(self, state):
        return self.DynamicPolicyLearnerIntraOption_Table.getLearnedAction(state)

    def getConvergenceMetric(self):
        return self.DynamicPolicyLearnerIntraOption_Table.getConvergenceMetric()


class DistanceSource:
    def __init__(self, graph):
        self.distance_dict = {}
        self.graph = graph

    def getDistance(self, Bij, i):
        if self.distance_dict.has_key(Bij):
            if self.distance_dict[Bij].has_key(i):
                return self.distance_dict[Bij][i]

        ds = nx.shortest_path_length(self.graph, Bij, i)
        if not Bij in self.distance_dict:
            self.distance_dict[Bij] = {}
        if not i in self.distance_dict:
            self.distance_dict[i] = {}
        self.distance_dict[Bij][i] = ds
        self.distance_dict[i][Bij] = ds
        #print("Distance %d-%d = %d" % (Bij, i, ds))

        return ds