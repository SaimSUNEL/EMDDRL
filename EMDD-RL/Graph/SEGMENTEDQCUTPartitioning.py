import networkx as nx
import numpy as np
import random


class Segment(object):
    def __init__(self, segment_name, global_graph, source, sink, nodes, state_observation_count, environment,
                 option_table, q_cut_step_threshold, cut_threshold, distance_threshold):
        self.Q_CUT_STEP_THRESHOLD = q_cut_step_threshold
        self.CUT_THRESHOLD = cut_threshold
        self.DISTANCE_THRESHOLD = distance_threshold

        self.segment_name = segment_name
        # subgraph returns only view and can not be changed... so copy it for modification....
        # print("nodes : " + str(nodes))
        # print("global graph nodes : " + str(global_graph.nodes))
        self.segment_graph = global_graph.subgraph(nodes).copy()
        self.state_observation_count = state_observation_count
        self.source_nodes = source
        self.sink_nodes = sink
        self.environment = environment
        self.DynamicPolicyLearnerIntraOption_Table = option_table

        # self.DISTANCE_THRESHOLD = 15
        self.subgoal_candidates = {}
        self.subgoals = {}

    def hasSegmentNode(self, state):
        return state in self.segment_graph.nodes;

    # [state1, state2] if there is an edge => update, else => extend segment
    # while adding trajectory make sure that next state is not in the other segment
    # this may lead repetitions in finding subgoals...
    def addTransition(self, pair):
        if self.hasSegmentNode(pair[1]):
            self.segment_graph.add_node(pair[1])

        if self.segment_graph.has_edge(pair[0], pair[1]):
            self.segment_graph[pair[0]][pair[1]]["weight"] += 1

            self.segment_graph[pair[0]][pair[1]]["capacity"] = self.segment_graph[pair[0]][pair[1]]["weight"] / float(
                self.state_observation_count[pair[0]])
        else:
            # self.local_graph.add_nodes_from(pair)
            self.segment_graph.add_edge(pair[0], pair[1])
            self.segment_graph[pair[0]][pair[1]]["weight"] = 1

            self.segment_graph[pair[0]][pair[1]]["capacity"] = 1.0 / float(self.state_observation_count[pair[0]])

    # if partition is of good quality
    def partitionSegment(self):
        # the sink nodes could be specified via passing sink state into segment object
        # or some distance metric is used among nodes when sink nodes are far enough from source
        # perform cut operation
        most_distant_node = None
        distance = 0
        start = None

        if self.sink_nodes == None:

            # find the most distant path from all of starting nodes

            for a in self.source_nodes:
                # some environment has different number of source nodes...
                if not self.hasSegmentNode(a):
                    continue
                d = nx.shortest_path_length(self.segment_graph, source=a)
                for k in d.keys():
                    if d[k] > self.DISTANCE_THRESHOLD:
                        start = a
                        distance = d[k]
                        most_distant_node = k
                        break

            if distance >= self.DISTANCE_THRESHOLD:
                min_cut_value, partitions = nx.minimum_cut(self.segment_graph, start, most_distant_node)
                Ns = list(partitions[0])
                Nt = list(partitions[1])

                # calculate ratiocut check if satisfies...
                found, Ns, Nt, Nt_start = self.checkCutQuality(Ns, Nt)

                return found, Ns, Nt, Nt_start
            else:
                # return cut condition satisfied, Ns, Nt
                return False, None, None, None


        else:
            for s in self.source_nodes:
                for t in self.sink_nodes:
                    min_cut_value, partition = nx.minimum_cut(self.segment_graph, s, t)
                    Ns = list(partition[0])
                    Nt = list(partition[1])

                    # calculate ratiocut check if satisfies...
                    found, Ns, Nt, Nt_start = self.checkCutQuality(Ns, Nt)

                    # as soon as a bottleneck is found, return

                    return found, Ns, Nt, Nt_start

            return False, None, None, None

    def checkCutQuality(self, Ns, Nt):
        size_Ns = len(Ns)
        size_Nt = len(Nt)

        if not nx.is_connected(nx.subgraph(self.segment_graph, Ns).copy().to_undirected()) or \
                not nx.is_connected(nx.subgraph(self.segment_graph, Nt).copy().to_undirected()):
            # print("Problem Zone...")

            return False, None, None, None

        sub_goal = []

        cut_edge_count = 0
        for s in Ns:
            for n in Nt:
                # add cut's other side corresponding...
                if self.segment_graph.has_edge(s, n):
                    # exclude previous found subgoal states...

                    sub_goal.append(n)
                    cut_edge_count += 1

        metric = size_Ns * size_Nt / float(cut_edge_count)
        # print("Metric : " + str(metric))
        sub_goal = list(set(sub_goal))
        for s in sub_goal:
            if not s in self.subgoal_candidates:
                self.subgoal_candidates[s] = 1
            else:
                self.subgoal_candidates[s] += 1

        # print("Subgoal state : " + str(sub_goal) + " ratio : " + str(metric))
        if metric > self.CUT_THRESHOLD:  # for two rooms environment....
            # print("*****************Option - Subgoal " + str(s) + " added...")
            # print("Subgoals : " + str(sub_goal))
            # print("initiation : " + str(sorted(Ns)))
            for s in [sub_goal[0]]:
                # # print("Initiation set "+str(self.subgoal_initiation_sets[s]))

                new_op_init = [a for a in Ns]
                self.subgoals[s] = 0
                new_op_terminate = [s]
                new_option_goal_rewards = {s: 5}
            # sub_goal contains all found sugoals and Nt's starting states...
            return True, Ns, Nt, sub_goal

        if len(self.subgoal_candidates.keys()) > 0:
            # self.environment.setEnableSubgoalDisplay(True)
            # self.environment.setDisplaySubgoal(self.subgoal_candidates)
            # # print("Subgoals so far....")
            # # print(self.subgoals)
            pass

        return False, None, None, None

    def getSegmentName(self):
        return self.segment_name


class SegmentCoordinator(object):
    def __init__(self, environment, global_graph, state_observation_table, option_table, env_start_state,
                 env_goal_state, q_cut_step_threshold, cut_threshold, distance_threshold):
        self.Q_CUT_STEP_THRESHOLD = q_cut_step_threshold
        self.CUT_THRESHOLD = cut_threshold
        self.DISTANCE_THRESHOLD = distance_threshold

        self.environment = environment
        self.DynamicPolicyLearnerIntraOption_Table = option_table

        self.env_goal_state = env_goal_state
        self.segment_batch = {}
        self.global_graph = global_graph
        self.state_observation_count = state_observation_table

        self.segment_number = 0
        segment_0 = Segment("segment_0", self.global_graph, env_start_state, None, env_start_state,
                            self.state_observation_count, self.environment, self.DynamicPolicyLearnerIntraOption_Table, self.Q_CUT_STEP_THRESHOLD, self.CUT_THRESHOLD, self.DISTANCE_THRESHOLD)

        self.segment_batch["segment_0"] = segment_0
        self.segment_number += 1

        self.segment_colors = [(128, 0, 0), (255, 0, 0), (0, 128, 0), (0, 255, 0), (0, 0, 128), (0, 0, 255),
                               (128, 128, 0), (128, 0, 128), (0, 128, 128), (128, 128, 128), (255, 255, 0),
                               (0, 255, 255), (255, 0, 255), (128, 255, 255), (255, 128, 255), (255, 255, 128),
                               (128, 0, 255)]
        import random
        for i in range(150):
            self.segment_colors.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

        self.segment_information = {}
        self.segment_information["segment_0"] = {"color": self.segment_colors[0], "graph": segment_0.segment_graph}

    def addTrajectory(self, pair):
        pair_0_segment = None
        pair_1_segment = None
        for segment_name in self.segment_batch:
            segment = self.segment_batch[segment_name]
            if segment.hasSegmentNode(pair[0]):
                pair_0_segment = segment.getSegmentName()
            if segment.hasSegmentNode(pair[1]):
                pair_1_segment = segment.getSegmentName()

        # if pair_0_segment == None:
        #     # print(f"Pair {pair}")
        #     # print(f"segment len {len(self.segment_batch)}")
        #     # print(f"Segment batch : {self.segment_batch}")
        #     # print(f"list {self.segment_batch.values()}")
        #     # print(f"type {type(self.segment_batch.values())}")
        #     # print(f"Segment 0 {list(self.segment_batch.values())[0].segment_graph.nodes}")
        #     exit()

        # next state may not be in any segment, than add it to current_state's segment...
        # pair_0_segment can not be None...

        if pair_0_segment != None and pair_1_segment == None:
            self.segment_batch[pair_0_segment].addTransition(pair)
        # if pair in different segments than do not add it..
        # do not repeate previous segmentation
        elif pair_0_segment != pair_1_segment:
            pass
        # update segment trajectory...
        elif (not pair_0_segment is None)  and (pair_0_segment == pair_1_segment):
            self.segment_batch[pair_0_segment].addTransition(pair)

    # after adding trajectories to segments... We checks for new bottlenecks
    # option creation is handled in Segment class...
    def checkForNewSegment(self):
        for segment in self.segment_batch.values():
            # do not create option in goal segment, may cause distortions due to option and agent may not
            # be able to reach goal...
            if segment.hasSegmentNode(self.env_goal_state[0]):
                continue

            success, Ns, Nt, Nt_sources = segment.partitionSegment()
            # if target segment could be divided...
            if success:

                erased = segment.getSegmentName()
                new_segment_1 = Segment("segment_" + str(self.segment_number), self.global_graph,
                                        [a for a in segment.source_nodes], None, Ns, self.state_observation_count,
                                        self.environment, self.DynamicPolicyLearnerIntraOption_Table, self.Q_CUT_STEP_THRESHOLD, self.CUT_THRESHOLD, self.DISTANCE_THRESHOLD)

                if not nx.is_connected(new_segment_1.segment_graph.to_undirected()):
                    continue

                self.segment_number += 1

                new_segment_2 = Segment("segment_" + str(self.segment_number), self.global_graph, Nt_sources, None, Nt,
                                        self.state_observation_count, self.environment,
                                        self.DynamicPolicyLearnerIntraOption_Table, self.Q_CUT_STEP_THRESHOLD, self.CUT_THRESHOLD, self.DISTANCE_THRESHOLD)

                if not nx.is_connected(new_segment_1.segment_graph.to_undirected()):
                    continue

                self.segment_information["segment_" + str(self.segment_number - 1)] = {
                    "color": self.segment_colors[self.segment_number - 1],
                    "graph": new_segment_1.segment_graph}

                self.segment_information["segment_" + str(self.segment_number)] = {
                    "color": self.segment_colors[self.segment_number],
                    "graph": new_segment_2.segment_graph}

                self.segment_number += 1

                self.segment_batch[new_segment_1.getSegmentName()] = new_segment_1
                self.segment_batch[new_segment_2.getSegmentName()] = new_segment_2

                # after current segment has been partitioned, we are creating new two segments from this segment
                # erasing the divided segment....

                # print("Segment 1 : " + str(nx.is_connected(new_segment_1.segment_graph.to_undirected())))
                # print("Segment 2 : " + str(nx.is_connected(new_segment_2.segment_graph.to_undirected())))

                if not nx.is_connected(new_segment_1.segment_graph.to_undirected()) or \
                        not nx.is_connected(new_segment_2.segment_graph.to_undirected()):

                    all_nodes = [a for a in segment.segment_graph.nodes]
                    for j in new_segment_1.segment_graph.nodes:
                        all_nodes.remove(j)

                    for j in new_segment_2.segment_graph.nodes:
                        all_nodes.remove(j)

                self.segment_information.pop(erased)
                self.segment_batch.pop(erased)


                return Nt_sources

class SEGMENTEDQCUT(object):
    def __init__(self, Q_CUT_STEP_THRESHOLD = 20, CUT_THRESHOLD=100, DISTANCE_THRESHOLD=15):
        self.current_option = None
        self.current_action = None
        self.current_state = None

        self.Q_CUT_STEP_THRESHOLD = Q_CUT_STEP_THRESHOLD
        self.CUT_THRESHOLD = CUT_THRESHOLD
        self.DISTANCE_THRESHOLD = DISTANCE_THRESHOLD

        self.option_step_count = 0
        self.option_accumulated_reward = 0
        self.option_started_state = None
        self.is_all_options_converged = False

        # for iterating q cut, we don't have to wait till the episode terminates
        # this variable keeps the episode step count
        self.q_cut_step_count = 0

        # for storing episode history... it will hold episode steops and this transitions are
        # added to global graph...
        # iteration...
        self.q_cut_batch = []
        # flow graph is a directed graph...
        self.global_graph = nx.DiGraph()

        self.starting_states = []
        self.goal_states = []

        # tp parameter : how many times a stated is identified as hit...
        self.subgoal_candidates = {}

        # total local graph built count for measuring tc parameter
        self.total_qcut_construction = 0
        self.subgoals = {}

        # state : set([states...])
        self.subgoal_initiation_sets = {}
        self.state_observation_count = {}

        self.segment_coordinator_created = False

    def addStartingState(self, state):
        self.starting_states.append(state)
        if state in self.state_observation_count:
            self.state_observation_count[state] += 1
        else:
            self.state_observation_count[state] = 1

    def addGoalState(self, state):
        if state in self.state_observation_count:
            self.state_observation_count[state] += 1
        else:
            self.state_observation_count[state] = 1
        self.goal_states.append(state)

    # when episode finishes, option also terminates...
    # so after each termination, a start option must be chosen among the available one in the starting state
    def preEpisode(self, current_state):
        self.option_started_state = current_state
        self.option_step_count = 0
        self.option_accumulated_reward = 0

        # update state observation counts...
        if self.option_started_state in self.state_observation_count:
            self.state_observation_count[self.option_started_state] += 1
        else:
            self.state_observation_count[self.option_started_state] = 1

    def preAction(self, state):
        # if option terminates than choose the one consistent with the current state
        # accordingto e greedy approach...
        self.current_state = state
        if state in self.state_observation_count:
            self.state_observation_count[state] += 1
        else:
            self.state_observation_count[state] = 1

        return None

    def afterAction(self, next_state):
        # update state observation counts...
        if next_state in self.state_observation_count:
            self.state_observation_count[next_state] += 1
        else:
            self.state_observation_count[next_state] = 1

        # Current state and its precedor is added...
        self.q_cut_batch.append([self.current_state, next_state])
        self.q_cut_step_count += 1

        if (self.Q_CUT_STEP_THRESHOLD is None) or self.q_cut_step_count >= self.Q_CUT_STEP_THRESHOLD:

            # when qcut step exceeds threshold re constract local graph

            subgoal_identified = self.applySegmentedQCut(self.q_cut_batch)

            self.q_cut_step_count = 0
            self.q_cut_batch = []
            return subgoal_identified

    def applySegmentedQCut(self, history):

        if self.Q_CUT_STEP_THRESHOLD is not None and len(history) < 2:
            return

        self.total_qcut_construction += 1

        # this graph is directed graph
        for pair in history:
            if self.global_graph.has_node(pair[0]):
                pass
            else:
                self.global_graph.add_node(pair[0])

            if self.global_graph.has_node(pair[1]):
                pass
            else:
                self.global_graph.add_node(pair[1])

            if self.global_graph.has_edge(pair[0], pair[1]):
                self.global_graph[pair[0]][pair[1]]["weight"] += 1

                self.global_graph[pair[0]][pair[1]]["capacity"] += 1
                self.global_graph[pair[0]][pair[1]]["capacity"] = self.global_graph[pair[0]][pair[1]]["weight"] / float(
                    self.state_observation_count[pair[0]])

            else:
                # self.local_graph.add_nodes_from(pair)
                self.global_graph.add_edge(pair[0], pair[1])
                self.global_graph[pair[0]][pair[1]]["weight"] = 1

                self.global_graph[pair[0]][pair[1]]["capacity"] = 1.0 / float(self.state_observation_count[pair[0]])

        s_state = np.random.choice(self.starting_states)
        g_state = None
        nodes = self.global_graph.nodes

        if self.segment_coordinator_created == False:
            self.segment_coordinator = SegmentCoordinator(None, self.global_graph,
                                                          self.state_observation_count,
                                                          None,
                                                          self.starting_states, self.goal_states, self.Q_CUT_STEP_THRESHOLD, self.CUT_THRESHOLD, self.DISTANCE_THRESHOLD)
            self.segment_coordinator_created = True

        for pair in history:
            self.segment_coordinator.addTrajectory(pair)

        return self.segment_coordinator.checkForNewSegment() # return identified subgoal state
