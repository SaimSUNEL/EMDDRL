import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
import matplotlib.pyplot as plt

from timeit import default_timer as timer

class TransitionGraph(object):

    def __init__(self, saved_file=None):
        self.saved_file = saved_file
        if saved_file == None:
            self.graph = nx.Graph()
            self.distance_dictionary = {}
            self.state_frequency = {}

    def add2Vertices(self, vertex1, vertex2):
        if self.saved_file == None:

            if not vertex1 in self.state_frequency:
                self.state_frequency[vertex1] = 0
            if not vertex2 in self.state_frequency:
                self.state_frequency[vertex2] = 0

            self.state_frequency[vertex1] += 1
            self.state_frequency[vertex2] += 1


            # each distance between adjacent nodes is 1
            self.graph.add_edge(vertex1, vertex2, weight=1)

    def __getitem__(self, item):
        if self.saved_file is not None:
            # print(item)
            return self.saved_file[item[0]][item[1]]
        # distance to itself is 0
        # print(item)
        if item[0] == item[1]:
            return 0

        # return abs(self.state_frequency[item[0]] - self.state_frequency[item[1]])

        if item in self.distance_dictionary:
            return self.distance_dictionary[item]
        try:
            distance = len(nx.bidirectional_shortest_path(self.graph, item[0], item[1]))-1
        except:
            distance = 100000000
            pass


        # distance = nx.shortest_path_length(self.graph, item[0], item[1])
        # print(f"shortest_path_length took {diff2} - bidirectional_dijkstra took {diff1} fold : {diff2/diff1}")
        # print(distance)
        # print(distance, distance2)
        # exit()

        self.distance_dictionary[(item[0], item[1])] = distance
        self.distance_dictionary[(item[1], item[0])] = distance
        return distance

    def drawGraph(self, filename="transition_graph.png"):
        plt.clf()
        options = {
            'node_color': 'blue',
            'node_size': 750,
            'width': 100,
            "font_size": 15,
            "font_color": "green"}
        pos = nx.nx_agraph.graphviz_layout(self.graph)
        nx.draw(self.graph, pos=pos, with_labels=True, **options)
        plt.savefig(filename)


    def saveGraph(self, filename):
        import pickle
        pickle.dump(self.graph, open(filename, "wb"))

    def loadGraph(self, filename):
        # TODO: implement graph loading
        pass
