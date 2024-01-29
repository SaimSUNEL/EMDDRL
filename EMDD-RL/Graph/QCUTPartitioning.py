import networkx as nx
import numpy as np
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
import matplotlib.pyplot as plt

class QCUT(object):
    def __init__(self, Q_CUT_STEP_THRESHOLD = 200, single_run=False, CUT_THRESHOLD=4000):
        # for iterating q cut, we don't have to wait till the episode terminates
        # this variable keeps the episode step count
        self.q_cut_step_count = 0
        # for storing episode history... it will hold episode steops and this transitions are
        # added to global graph...
        # iteration...
        self.q_cut_batch = []
        # flow graph is a directed graph...
        self.global_graph = nx.DiGraph()

        self.single_run = single_run

        self.CUT_THRESHOLD = CUT_THRESHOLD

        # tp parameter : how many times a stated is identified as hit...
        self.subgoal_candidates = {}
        # total local graph built count for measuring tc parameter
        self.total_qcut_construction = 0
        self.Q_CUT_STEP_THRESHOLD = Q_CUT_STEP_THRESHOLD  # in every 1000 steps we run the algorithm...
        self.subgoals = {}
        # state : set([states...])
        self.state_observation_count = {}

        self.starting_states = []
        self.goal_states = []

    # when episode finishes, option also terminates...
    # so after each termination, a start option must be chosen among the available one in the starting state

    # we'll feed the episodes, so the first state is one of the states residing in the left room
    def addStartingState(self, state):
        if state in self.state_observation_count:
            self.state_observation_count[state] += 1
        else:
            self.state_observation_count[state] = 1
        if state in self.starting_states:
            return
        self.starting_states.append(state)

    # we'll feed the episodes, so the last state is one of the states residing in the left room
    def addGoalState(self, state):
        if state in self.goal_states:
            return
        self.goal_states.append(state)

    def addHistory(self, pair):
        next_state = pair[0]
        # update state observation counts...
        if next_state in self.state_observation_count:
            self.state_observation_count[next_state] += 1
        else:
            self.state_observation_count[next_state] = 1

        # Current state and its precedor is added...
        self.q_cut_batch.append(pair)
        self.q_cut_step_count += 1
        res = None
        if not self.single_run:
            if self.q_cut_step_count >= self.Q_CUT_STEP_THRESHOLD:
                # when qcut step exceeds threshold re constract local graph
                res = self.applyQCut(self.q_cut_batch)
                self.q_cut_step_count = 0
                self.q_cut_batch = []
        return res
    def afterEpisode(self):
        self.q_cut_step_count = 0
        self.q_cut_batch = []

    def applyQCut(self, history=None):
        # print("\n\n**************Apply QCUT**************\n\n")
        history = self.q_cut_batch if history == None else history
        if len(history) < 2:
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

        while not s_state in nodes:
            s_state = np.random.choice(self.starting_states)

        if len(self.goal_states) == 1:
            g_state = self.goal_states[0]

        if not g_state in nodes:
            # print("Goal state does not exist", g_state)
            # print(self.global_graph.nodes)
            # self.drawGraph("qcuttworooms")
            # exit()
            return
        min_cut_value, partitions = nx.minimum_cut(self.global_graph, s_state, g_state)
        Ns = list(partitions[0])
        Nt = list(partitions[1])

        size_Ns = len(Ns)
        size_Nt = len(Nt)

        sub_goal = []
        reachable, non_reachable = partitions

        cut_edge_count = 0
        cutset = set()

        for u, nbrs in ((n, self.global_graph[n]) for n in reachable):
            cutset.update((u, v) for v in nbrs if v in non_reachable)

        # print("CUT set : ", sorted(cutset))

        # cut_value == sum(G.edges[u, v]["capacity"] for (u, v) in cutset)
        for pair in cutset:
            sub_goal.append(pair[0])
            break
        cut_edge_count = len(cutset)
        # for s in Ns:
        #     for n in Nt:
        #         # add cut's other side corresponding...
        #         if self.global_graph.has_edge(s, n):
        #             if n in self.subgoals.keys():
        #                 continue
        #             sub_goal.append(n)
        #             cut_edge_count += 1

        if cut_edge_count == 0:
            return
        metric = size_Ns * size_Nt / float(cut_edge_count)

        sub_goal = list(set(sub_goal))
        for s in sub_goal:
            if not s in self.subgoal_candidates:
                self.subgoal_candidates[s] = 1
            else:
                self.subgoal_candidates[s] += 1
        s = pair[0]
        # print("min cut value : " + str(min_cut_value))
        # print("partitions : "+ str(partitions))

        # print("Subgoal state : " + str(sub_goal) + " ratio : " + str(metric))
        if metric > self.CUT_THRESHOLD:  # for two rooms environment....
            # print("*****************Option - Subgoal " + str(s) + " added...")
            return s

    def drawGraph(self, filename="transition_graph.png"):
        plt.clf()
        options = {
            'node_color': 'blue',
            'node_size': 750,
            'width': 100,
            "font_size": 15,
            "font_color": "green"}
        pos = nx.nx_agraph.graphviz_layout(self.global_graph)
        nx.draw(self.global_graph, pos=pos, with_labels=True, **options)
        plt.savefig(filename)
