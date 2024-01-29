import networkx as nx
import numpy as np
from networkx.drawing.nx_agraph import graphviz_layout
from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
import matplotlib.pyplot as plt
import Graph.TransitionGraph as TransitionGraph

class BETWEENNESS(TransitionGraph.TransitionGraph):

    def __init__(self, FIND_LOCAL_PEAKS=True):
        super(BETWEENNESS, self).__init__()
        raise Exception("Implement as Directed grahp")
        self.FIND_LOCAL_PEAKS = FIND_LOCAL_PEAKS

    def applyBetweennes(self):
        betweennes = nx.betweenness_centrality(self.graph, weight="weight")
        # we may want to get all local peaks or the global peak depending on the problem...
        if self.FIND_LOCAL_PEAKS:
            return self.findLocalPeak(self.graph, betweennes)
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