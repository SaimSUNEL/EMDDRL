import numpy as np
import networkx as nx

class DiverseDensity:
    DISTANCE_METRIC_STANDARDIZATION = 1
    DISTANCE_METRIC_GRAPH = 2
    DISTANCE_METRIC_NONE = 3

    DIRECT_DISTANCE = 100
    INDIRECT_DISTANCE = 102

    def __init__(self, positive_bags, negative_bags, graph, distance_metric = DISTANCE_METRIC_NONE, DISTANCE_SOURCE=DIRECT_DISTANCE):
        self.positive_bags = positive_bags
        self.negative_bags = negative_bags
        self.distance_metric = distance_metric
        self.graph = graph
        self.probability_network = nx.Graph()

        self.DISTANCE_SOURCE = DISTANCE_SOURCE

    def getSummary(self):
        return "DD Positive bag size %d - Negative bag size %d" % (len(self.positive_bags),
                                                                     len(self.negative_bags))

    def __call__(self, t):
        return self.DD(t)

    def Pr(self, x, Bij):
        if self.probability_network.has_edge(Bij, x):
            return self.probability_network[Bij][x]["weight"]
        else:
            # todo : change to
            distance = self.graph[Bij,x]# self.graph[Bij,x]# self.graph[Bij][x]
            distance = np.exp(-((distance) ** 2))
            self.probability_network.add_edge(Bij, x, weight=distance)
            return distance

    def PrPositive(self, t, Bi):
        multiplication = 1.0
        for element in set(Bi):

            v =  self.Pr(t, element)
            multiplication *= (1.0 - v)
        return 1.0 - multiplication

    def PrNegative(self, t, Bi):
        multiplication = 1.0
        for element in set(Bi):
            multiplication *= (1.0 - self.Pr(t, element))
        return multiplication

        # sd = 0.1 we will take, it has not been mentioned

    def DD(self, t):
        positive_multiplication = 0.0
        negative_multiplication = 0.0
        for positive_bag in self.positive_bags:

            pos = self.PrPositive(t, positive_bag)
            if -1e-10 < pos < 1e-10:
                pos = 1e-10

            positive_multiplication += np.log(pos)

        for negative_bag in self.negative_bags:
            neg = self.PrNegative(t, negative_bag)
            if 0-1e-10 < neg < 0+1e-10:
                neg = 1-1e-10
            positive_multiplication += np.log(neg)
        return (positive_multiplication )
