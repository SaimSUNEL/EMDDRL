import networkx as nx
import numpy as np
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
import matplotlib.pyplot as plt
import networkx as nx
import math

class BETWEENNESSOnline():

    def __init__(self, STEP_THRESHOLD = 200, FIND_LOCAL_PEAKS=True):
        super(BETWEENNESSOnline, self).__init__()
        self.FIND_LOCAL_PEAKS = FIND_LOCAL_PEAKS
        self.partial_graph = nx.Graph()
        self.STEP_THRESHOLD = STEP_THRESHOLD
        self.state_observation_count = {}

        self.step_count = 0
        self.betweenness_history = {}

        self.Q = 0.0056
        self.P = 0.0712
        self.FA_and_MISS = 100.0
        self.PN_PT = 100.0




    def preEpisode(self, first_state):
        # add first state at the beginnign of the
        self.partial_graph.add_node(first_state)
        self.current_state = first_state

        if first_state in self.state_observation_count.keys():
            self.state_observation_count[first_state] += 1
        else:
            self.state_observation_count[first_state] = 1

        self.step_count = 1

    def addHistory(self, pair):
        next_state = pair[1]
        self.current_state = pair[0]
        self.partial_graph.add_edge(next_state, self.current_state)
        self.step_count += 1
        # self transitions are not counted for observation independence...
        if next_state != self.current_state:
            if next_state in self.state_observation_count.keys():
                self.state_observation_count[next_state] += 1
            else:
                self.state_observation_count[next_state] = 1

            if self.step_count >= self.STEP_THRESHOLD:

                subgoals = self.applyOnlineBetweennes()

                self.afterEpisode()

                return subgoals

            return None

    def afterEpisode(self):
        self.partial_graph = nx.Graph()
        for key in self.state_observation_count.keys():
            self.state_observation_count[key] = 0
        self.step_count = 0

    def applyOnlineBetweennes(self):
        betweennes = nx.betweenness_centrality(self.partial_graph, weight="weight")
        # we may want to get all local peaks or the global peak depending on the problem...
        if self.FIND_LOCAL_PEAKS:
            candidates = self.findLocalPeak(self.partial_graph, betweennes)
            # subgoals that passing the test...
            subgoals = []
            for candidate in candidates:

                if candidate in self.betweenness_history:
                    self.betweenness_history[candidate].append(1)
                else:
                    self.betweenness_history[candidate] = [1]

                n1 = np.sum(self.betweenness_history[candidate])

                n = len(self.betweenness_history[candidate])

                test_ratio = n1 / float(n)

                test_value = math.log((1.0 - self.Q) / (1.0 - self.P)) / math.log(
                    (self.P * (1.0 - self.Q)) / (self.Q * (1.0 - self.P))) + \
                             (1.0 / n) * (math.log(self.FA_and_MISS * self.PN_PT) / math.log(
                    (self.P * (1.0 - self.Q)) / (self.Q * (1.0 - self.P))))

                if test_ratio >= test_value:
                    print(f"**************** Found Subgoal : {candidate}")
                    subgoal = candidate
                    subgoals.append(subgoal)
            return subgoals if len(subgoals) > 0 else None


        else:
            tuple_form = [(key, betweennes[key]) for key in betweennes]
            sorted_form = sorted(tuple_form, key=lambda v: v[1])
            return [sorted_form[-1][0]]

    def findLocalPeak(self, graph, dictionary):
        nodes = graph.nodes
        local_peaks = []
        for node in nodes:
            neighbors = graph.neighbors(node)
            is_heightest = True
            for n in neighbors:
                if dictionary[node] >= dictionary[n]:
                    pass
                else:
                    is_heightest = False
                    break
            if is_heightest:
                local_peaks.append(node)
        return local_peaks