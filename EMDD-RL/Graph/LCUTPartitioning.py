import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
import matplotlib.pyplot as plt
import numpy as np

class LCUT(object):

    def __init__(self, TC_PARAM = 0.05, TO_PARAM = 10, TP_PARAM = 0.25, L_CUT_STEP_THRESHOLD = 500):
        self.local_l_cut_graph = None
        self.distance_dictionary = {}
        self.state_frequency = {}
        # total local graph built count for measuring tc parameter
        self.total_lcut_construction = 0

        # n_cut threshold value...
        self.TC_PARAM = TC_PARAM
        self.TO_PARAM = TO_PARAM
        self.TP_PARAM = TP_PARAM
        self.L_CUT_STEP_THRESHOLD = L_CUT_STEP_THRESHOLD  # corresponds h param in paper...

        self.state_observation_count = {}
        self.subgoals = {}

        self.history = []
        self.subgoal_candidates = {}



    def addHistory(self, episode):
        self.history.append(episode)
        res = None

        if len(self.history) > self.L_CUT_STEP_THRESHOLD:
            # print("****************APPLY LCUT**************")
            res = self.applyLCut()
            self.subgoals = {} # zero returned subgoals of the current search for next search...

        return res

    def afterEpisode(self):
        self.history = [] # zero the episode history for the next graph contrunction, graph is constructed first when the episode threshold exceeds a certain value and secondly when the episode finishes...
        self.subgoals = {}


    def drawGraph(self, filename="transition_graph.png"):
        plt.clf()
        options = {
            'node_color': 'blue',
            'node_size': 750,
            'width': 100,
            "font_size": 15,
            "font_color": "green"}
        pos = nx.nx_agraph.graphviz_layout(self.local_l_cut_graph)
        nx.draw(self.local_l_cut_graph, pos=pos, with_labels=True, **options)
        plt.savefig(filename)

    def applyLCut(self):
        history = self.history
        if len(history) < 2:
            return

        self.total_lcut_construction += 1

        # this graph is directed graph
        self.local_graph = nx.DiGraph()
        for pair in history:
            self.local_graph.add_nodes_from(pair)
            self.local_graph.add_edge(pair[0], pair[1])

            weight = self.local_graph[pair[0]][pair[1]]
            # if edge is not added previously, than add the weight information
            if len(weight.keys()) == 0:
                self.local_graph[pair[0]][pair[1]]["weight"] = 1

            # If edge exists already, than increase the weight...
            else:
                self.local_graph[pair[0]][pair[1]]["weight"] += 1

        # undirected graph...
        self.local_l_cut_graph = nx.Graph()
        self.local_l_cut_graph.add_nodes_from(self.local_graph.nodes)
        for edge in self.local_graph.edges:
            if self.local_l_cut_graph.has_edge(edge[0], edge[1]):
                self.local_l_cut_graph[edge[0]][edge[1]]["weight"] += self.local_graph[edge[0]][edge[1]]["weight"]
            else:
                self.local_l_cut_graph.add_edge(edge[0], edge[1])
                self.local_l_cut_graph[edge[0]][edge[1]]["weight"] = self.local_graph[edge[0]][edge[1]]["weight"]

        nodes = list(self.local_l_cut_graph.nodes)

        for n in nodes:
            # add observation numbers...
            if n in self.state_observation_count:
                self.state_observation_count[n] += 1
            else:
                self.state_observation_count[n] = 1

        # print("nodes : ", nodes)
        state_indices = {nodes[k]:k for k in range(len(nodes))}
        D = np.eye(len(nodes), len(nodes), dtype=np.float32)
        W = np.zeros((len(nodes), len(nodes)), dtype=np.float32)

        for ind in range(len(nodes)):
            node = nodes[ind]
            sum = 0
            for neigh in self.local_l_cut_graph.adj[node]:
                weight = self.local_l_cut_graph[node][neigh]["weight"]
                W[state_indices[node]][state_indices[neigh]] = weight
                sum += weight
            D[state_indices[node]][state_indices[node]] = sum

        # A = np.matmul(np.linalg.inv(D), D-W)
        A = np.matmul(np.linalg.inv(D), D-W)

        # print("A : ")
        # print(A)
        # doc says the eigen values are not necessarily ordered...
        eigen_values, eigen_vector = np.linalg.eig(A)
        # print("eigen values : \n")
        # print(eigen_values)
        # print("eigen vectors : \n")
        # print(eigen_vector)
        sort_ind  = np.argsort(eigen_values)

        second_smallest_index = sort_ind[1]
        second_smallest_eigen = eigen_values[second_smallest_index]
        second_eigen_vector = eigen_vector[:, second_smallest_index]

        # print("required eigen : ", str(second_smallest_eigen))
        # print("required vector : ", str(second_eigen_vector))

        min_val = np.min(second_eigen_vector)
        max_val = np.max(second_eigen_vector)

        interval = (max_val - min_val)/len(nodes)
        # print("max val "+str(max_val))
        # print("min val "+str(min_val))
        # print("Interval : "+str(interval))

        block_index = 1
        set_best_a = None
        set_best_b = None

        set_best_subgoal_a = []
        set_best_subgoal_b = []
        set_best_a = []
        set_best_b = []
        min_cut_value = float('inf')

        while min_val + interval*block_index < max_val:

            set_a = []
            set_b = []
            set_a_subgoal_candidate = []
            set_b_subgoal_candidate = []

            threshold_value = min_val + interval*block_index
            for node_index in range(len(nodes)):
                if second_eigen_vector[node_index] <= threshold_value:
                    set_a.append(node_index)
                else:
                    set_b.append(node_index)


            # current partitions..
            set_a = [nodes[i] for i in set_a]
            set_b = [nodes[i] for i in set_b]

            # print("Set A : "+str(set_a))
            # print("Set B : "+str(set_b))


            # for visualization purposes...
            part1 = nx.Graph()
            part2 = nx.Graph()

            set_a_volume = 0
            cut_a_b = 0

            set_b_volume = 0
            cut_b_a = 0

            for node in set_a:
                neightbours = list(self.local_graph.adj[node])

                # print("node : "+str(node))
                # print("neighbours : "+str(neightbours))

                for neigh in neightbours:
                    # print("neight : "+str(neigh))
                    if neigh in set_a:
                        # print(str(neigh)+" in set_a")
                        # print("weight ", self.local_graph[node][neigh]["weight"])
                        set_a_volume += self.local_graph[node][neigh]["weight"]
                        # part1.add_nodes_from([node, neigh])
                        # if self.local_graph.has_edge(node, neigh):
                        #    part1.add_weighted_edges_from([[node, neigh, self.local_graph[node][neigh]["weight"]]])

                    else:
                        set_a_subgoal_candidate.append(node)
                        # print(str(neigh)+" in set_b")
                        # print("weight : ", self.local_graph[node][neigh]["weight"])

                        set_a_volume += self.local_graph[node][neigh]["weight"]
                        cut_a_b += self.local_graph[node][neigh]["weight"]


            for node in set_b:
                neightbours = list(self.local_graph.adj[node])
                for neigh in neightbours:
                    if neigh in set_b:
                        set_b_volume += self.local_graph[node][neigh]["weight"]
                        # part2.add_nodes_from([node, neigh])
                        #if self.local_graph.has_edge(node, neigh):
                        #    part2.add_weighted_edges_from([[node, neigh, self.local_graph[node][neigh]["weight"]]])
                    else:
                        set_b_subgoal_candidate.append(node)
                        set_b_volume += self.local_graph[node][neigh]["weight"]
                        cut_b_a += self.local_graph[node][neigh]["weight"]


            appr_n_cut = (cut_a_b+cut_b_a)/float((set_a_volume+cut_b_a)) + (cut_b_a+cut_a_b)/float((set_b_volume+cut_a_b))

            if min_cut_value > appr_n_cut:
                min_cut_value = appr_n_cut
                set_best_a = set_a
                set_best_b = set_b

                set_best_subgoal_a = set_a_subgoal_candidate
                set_best_subgoal_b = set_b_subgoal_candidate


            # self.drawLocalGraph(self.local_l_cut_graph, part1, part2)
            #self.drawLocalGraph(part1)
            #self.drawLocalGraph(part2)
            block_index += 1


        # print("Best min cut : "+str(min_cut_value))
        #print("set a : "+ str(set_best_a))
        #print("set b : "+ str(set_best_b))
        #print("a candidtate : "+str(set_best_subgoal_b))
        #print("b candidate : "+str(set_best_subgoal_a))

        if min_cut_value <= self.TC_PARAM:
            pass
        else:
            set_best_subgoal_a = []
            set_best_subgoal_b = []


        # one state might exist in array more than once


        for s in set_best_subgoal_a:
            if s in self.subgoal_candidates:
                self.subgoal_candidates[s] += 1

                # add sets of opposite block whose distantce to this hit is fewer than lo parameter...

                # TO control min hit count for state to become subgoal...
                # print(str(s)+"to : "+ str(self.state_observation_count[s]) +" - tp : "+str(self.subgoal_candidates[s] / float(self.state_observation_count[s])))
                if self.state_observation_count[s] >= self.TO_PARAM:
                    # and hit must occur in local graph as a hit proportional to total graph construction..

                    # add sets of opposite block whose distantce to this hit is fewer than lo parameter...

                    if self.subgoal_candidates[s] / float(self.state_observation_count[s]) >= self.TP_PARAM:
                        self.subgoals[s] = 0
                        # print("*****************Subgoal "+str(s)+" added...")

            else:
                self.subgoal_candidates[s] = 1

        for s in set_best_subgoal_b:
            if s in self.subgoal_candidates:
                self.subgoal_candidates[s] += 1
                # add sets of opposite block whose distantce to this hit is fewer than lo parameter...
                if self.state_observation_count[s] > self.TO_PARAM:
                    if self.subgoal_candidates[s] / float(self.state_observation_count[s]) >= self.TP_PARAM:
                        self.subgoals[s] = 0
                        print("*****************Subgoal " + str(s) + " added...")
            else:
                self.subgoal_candidates[s] = 1

        self.history = [] # zero the episode history for the next graph contrunction, graph is constructed first when the episode threshold exceeds a certain value and secondly when the episode finishes...
        return self.subgoals