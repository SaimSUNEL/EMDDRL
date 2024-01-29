import numpy as np
from MIL.Methods.DD import DiverseDensity
import networkx as nx

class EMDD:
    DISTANCE_METRIC_STANDARDIZATION = 1
    DISTANCE_METRIC_GRAPH = 2
    DISTANCE_METRIC_NONE = 3
    LINEAR = "LINEAR"
    DD_MODEL = "DDMODEL"
    EXPONENTIAL = "EXPONENTIAL"
    M_MODEL = LINEAR

    SEED_SET_SHORTEST_PATH_WITH_K = "SEED_SET_SHORTEST_PATH_WITH_K"
    SEED_SET_CONCEPT_FILTER = "SEED_SET_CONCEPT_FILTER"
    SEED_SET_MANUEL = "SEED_SET_MANUEL"
    SEED_SET_LAST_PATH_WITH_K = "SEED_SET_LAST_PATH_WITH_K"
    SEED_SET_ALL_POSITIVE = "SEED_SET_ALL_POSITIVE"

    DIRECT_DISTANCE = 100
    INDIRECT_DISTANCE = 102

    # on maximization step which states will be checked for maximum h
    # all positive instances
    H_ALL = "H_ALL"
    # or only h's neightbor hood.
    H_NEIGHBOR = "H_NEIGHBOR"
    H_SET = "H_SET"



    def __init__(self, positive_bags, negative_bags, graph, h_state_set, M_MODEL,distance_metric=DISTANCE_METRIC_NONE, H_CHECK=H_ALL, SKIPPING_FACTOR=1, DISTANCE_SOURCE=DIRECT_DISTANCE, SEED_SET=SEED_SET_SHORTEST_PATH_WITH_K, TRANSITION_GRAPH=None):
        self.DD = DiverseDensity(positive_bags, negative_bags, graph, distance_metric=distance_metric, DISTANCE_SOURCE=DISTANCE_SOURCE)
        self.positive_bags = positive_bags
        self.negative_bags = negative_bags
        self.distance_metric = distance_metric
        self.graph = graph
        self.STATES_TO_TEST = h_state_set
        self.M_MODEL = M_MODEL
        self.SKIPPING_FACTOR = SKIPPING_FACTOR

        self.SEED_SET = SEED_SET

        self.TRANSITION_GRAPH = TRANSITION_GRAPH
        self.test_indices = None
        self.test_instances = None
        self.shortest_positive_bag = None

        self.average_loop_count = 0

        self.H_METHOD = H_CHECK
        self.dd_value_table = {}
        self.probability_network = nx.Graph()

        self.neighbourhood = {}
        # for bag in self.positive_bags:
        #     for ins in bag:
        #         if not ins in self.neighbourhood:
        #             neighbors = self.graph[ins]
        #             neighbors_to_test = [a for a in neighbors if neighbors[a] == 1]
        #             self.neighbourhood[ins] = neighbors_to_test


        print("\n\n********EMDD**********\n\n")
        print("Search space : ", self.H_METHOD)
        print("Method : ", self.M_MODEL)
        self.DISTANCE_SOURCE = DISTANCE_SOURCE

    def getSummary(self):
        return "EMDD Positive bag size %d - Negative bag size %d" % (len(self.positive_bags),
                                                                len(self.negative_bags))

    def Pr(self, Bij, h):
        if self.probability_network.has_edge(Bij, h):
            return self.probability_network[Bij][h]["weight"]
        else:
            # todo : change to self.graph[Bij,h]
            distance = self.graph[Bij,h]# self.graph[Bij][h]
            distance = np.exp(-(((distance)) ** 2))
            self.probability_network.add_edge(Bij, h, weight=distance)
            return  distance
    
    def __call__(self):
        if self.SEED_SET == self.SEED_SET_SHORTEST_PATH_WITH_K:

            # print(range(len(self.positive_bags)))
            indices = np.random.choice(range(len(self.positive_bags)), 1)
            indices = [len(self.positive_bags)-1]
            max_value = -float("inf")
            shortest_episode_index = None
            max_length = float("inf")
            for i in range(len(self.positive_bags)):
                if len(self.positive_bags[i]) < max_length:
                    max_length = len(self.positive_bags[i])
                    shortest_episode_index = i

            max_h = None
            #randindices = np.random.choice(range(len(self.positive_bags[indices[0]])),20)
            #all_required_instances = []
            #for i in randindices:
            #    all_required_instances.append(self.positive_bags[-1][i])

            for index in [shortest_episode_index]:
                bag = np.array(self.positive_bags[index], dtype=np.int32)
                indices = self.test_indices = range(0, len(bag), self.SKIPPING_FACTOR)
                self.shortest_positive_bag = self.positive_bags[index]
                self.test_instances = bag[indices]
                for Bij in bag[indices]:
            #for Bij in all_required_instances:
                    h_, value = self.EMDD_(Bij)
                    # print("Initial : ", Bij, " found h : ", h_, " value : ", value)

                    if value > max_value:
                        max_value = value
                        max_h = h_
            # print("MAx h : ", max_h, " value : ", max_value)
            return max_h, max_value

        elif self.SEED_SET == self.SEED_SET_LAST_PATH_WITH_K:
            max_value = -float("inf")

            max_h = None

            for index in [-1]:
                bag = np.array(self.positive_bags[index], dtype=np.int32)
                indices = self.test_indices = range(0, len(bag), self.SKIPPING_FACTOR)
                self.shortest_positive_bag = self.positive_bags[index]
                self.test_instances = bag[indices]
                for Bij in bag[indices]:
                    h_, value = self.EMDD_(Bij)
                    # print("Initial : ", Bij, " found h : ", h_, " value : ", value)
                    if value > max_value:
                        max_value = value
                        max_h = h_
            # print("MAx h : ", max_h, " value : ", max_value)
            return max_h, max_value
        elif self.SEED_SET == self.SEED_SET_MANUEL:
            max_value = -float("inf")
            max_h = None
            self.test_instances = [93,94,95,114,115,116]
            self.test_instances = [94,214,325]
            for Bij in self.test_instances:
                # for Bij in all_required_instances:
                h_, value = self.EMDD_(Bij)
                # print("Initial : ", Bij, " found h : ", h_, " value : ", value)

                if value > max_value:
                    max_value = value
                    max_h = h_
            return max_h, max_value
        elif self.SEED_SET == self.SEED_SET_ALL_POSITIVE:
            max_value = -float("inf")
            max_h = None
            all_instances = set()
            for bag in self.positive_bags:
                for i in bag:
                    all_instances.add(i)

            self.test_instances = list(all_instances)
            for Bij in self.test_instances:
                # for Bij in all_required_instances:
                h_, value = self.EMDD_(Bij)
                # print("Initial : ", Bij, " found h : ", h_, " value : ", value)

                if value > max_value:
                    max_value = value
                    max_h = h_
            return max_h, max_value





    def EMDD_(self, h):

        nldd0 = float('inf')
        sd = 1.0
        if h in self.dd_value_table:
            nldd1 = self.dd_value_table[h]
        else:
            nldd1 = self.DD(h)* -1 # NLDD
            self.dd_value_table[h] = nldd1
        # print("nldd1 first : ", nldd1)
        # for k in range(5):
        loop_count = 0
        best_h = h
        best_DD_value = nldd1*-1
        while(nldd1 < nldd0):
            loop_count += 1
            # print("****")
            Bag_pi_star = []
            # E Step....
            for Bi in self.positive_bags:
                max_Bij = 0
                max_Bij_value = -float('inf')
                for Bij in Bi:
                    Bij_value = self.Pr(Bij, h)
                    if Bij_value > max_Bij_value:
                        max_Bij_value = Bij_value
                        max_Bij = Bij
                # 1 for positive bag...
                Bag_pi_star.append([max_Bij, max_Bij_value, 1])

            # traverse in negative bag...
            for Bi in self.negative_bags:
                max_Bij = 0
                max_Bij_value = -float('inf')
                for Bij in Bi:
                    Bij_value = self.Pr(Bij, h)
                    if Bij_value > max_Bij_value:
                        max_Bij_value = Bij_value
                        max_Bij = Bij
                # 1 for positive bag...
                Bag_pi_star.append([max_Bij, max_Bij_value, 0])

            # M-Step
            # since we are using only positive bags li s are 1.0
            # print("Bag pi start ", Bag_pi_star)
            inner_pi_positive_bag = [[a[0]] for a in Bag_pi_star if a[2] == 1]
            inner_pi_negative_bag = [[a[0]] for a in Bag_pi_star if a[2] == 0]
            #print("Inner pi positive bag : ", inner_pi_positive_bag)
            #print("Inner pi negative bag : ", inner_pi_negative_bag)

            inner_pi_positive_bag_set = set()
            for a in inner_pi_positive_bag:
                inner_pi_positive_bag_set.add(a[0])

            inner_pi_negative_bag_set = set()
            for a in inner_pi_negative_bag:
                inner_pi_negative_bag_set.add(a[0])

            inner_pi_positive_bag = [[a] for a in inner_pi_positive_bag_set]
            inner_pi_negative_bag = [[a] for a in inner_pi_negative_bag_set]

            #print("Final inner_pi_positive_bag : ", inner_pi_positive_bag)
            #print("Final inner_pi_negative_bag : ", inner_pi_negative_bag)
            if self.M_MODEL == self.DD_MODEL:
                # print("")
                max_h = None
                max_h_value = -float("inf")
                # here we use linear model
                temp_dd = DiverseDensity(inner_pi_positive_bag,inner_pi_negative_bag,self.graph,self.distance_metric)

                if self.H_METHOD == self.H_ALL:
                    test_instances = self.STATES_TO_TEST
                elif self.H_METHOD == self.H_NEIGHBOR:
                    neighbors = self.graph[h]
                    neighbors_to_test = [a for a in neighbors if neighbors[a] == 1]
                    test_instances = neighbors_to_test

                elif self.H_METHOD == self.H_SET:
                    test_instances = [a for a in inner_pi_positive_bag_set]
                for h_test in test_instances:

                    # # papers imposed solution...
                    # # h_test = None
                    # pi_ = set()
                    # multiplication = 0.0 # 1.0
                    # for pair in Bag_pi_star:
                    #     pi_star = pair[0]
                    #     bag_label = pair[2]
                    #     if pi_star in pi_:
                    #         continue
                    #     pi_.add(pi_star)
                    #
                    #     pi_star_value = pair[1]
                    #     # can be calculated two different ways, we have chosen exponential one...
                    #     # li = 1.0
                    #
                    #     value = 0 # np.exp(-(float(bag_label) - self.Pr(pi_star, h_test)) ** 2)
                    #     value = -((float(bag_label)-self.Pr(pi_star, h_test))**2)
                    #     multiplication += value
                    # # print("pr(%d, %d)=%f"%(pi_star, h_test, self.Pr(pi_star, h_test)))
                    # # print("Htest %d - DD %f" %(h_test, multiplication))

                    # multiplication = 0.0
                    # for pi in inner_pi_positive_bag:
                    #     multiplication += np.log(np.exp())

                    multiplication = temp_dd(h_test)
                    if multiplication > max_h_value:
                        # print("max h value : %f - multiplication %f : max_h : %d" %
                        #      (max_h_value, multiplication, h_test))

                        max_h_value = multiplication
                        max_h = h_test

            elif self.M_MODEL == self.LINEAR:
                max_h = None
                max_h_value = -float("inf")
                if self.H_METHOD == self.H_ALL:
                    test_instances = self.STATES_TO_TEST
                elif self.H_METHOD == self.H_NEIGHBOR:
                    neighbors = self.graph[h]
                    neighbors_to_test = [a for a in neighbors if neighbors[a] == 1]
                    test_instances = neighbors_to_test

                elif self.H_METHOD == self.H_SET:
                    test_instances = [a for a in inner_pi_positive_bag_set]
                    # to be removed...
                    # for c in inner_pi_negative_bag_set:
                    #     test_instances.append(c)
                for h_test in test_instances:
                    multiplication = 0.0

                    for pos_pi in inner_pi_positive_bag_set:
                        # because bag is positive 1.0 is added..
                        multiplication += np.log(1 - np.abs(1.0 - self.Pr(pos_pi, h_test))+1e-10)

                    for neg_pi in inner_pi_negative_bag_set:
                        # because bag is positive 1.0 is added..
                        multiplication += np.log(1- np.abs(-self.Pr(neg_pi, h_test))+1e-10)

                    if multiplication > max_h_value:
                        max_h_value = multiplication
                        max_h = h_test

            elif self.M_MODEL == self.EXPONENTIAL:
                max_h = None
                max_h_value = -float("inf")
                if self.H_METHOD == self.H_ALL:
                    test_instances = self.STATES_TO_TEST
                elif self.H_METHOD == self.H_NEIGHBOR:
                    neighbors = self.graph[h]
                    neighbors_to_test = [a for a in neighbors if neighbors[a] == 1]
                    test_instances = neighbors_to_test

                elif self.H_METHOD == self.H_SET:
                    test_instances = [a for a in inner_pi_positive_bag_set]
                    # To be removed...
                    # for c in inner_pi_negative_bag_set:
                    #     test_instances.append(c)

                for h_test in test_instances:# self.STATES_TO_TEST:
                    multiplication = 0.0

                    for pos_pi in inner_pi_positive_bag_set:
                        # because bag is positive 1.0 is added..
                        # multiplication += np.log(np.exp(-(1.0-self.Pr(pos_pi, h_test))))
                        multiplication += -(1.0-self.Pr(pos_pi, h_test))

                    for neg_pi in inner_pi_negative_bag_set:
                        # because bag is positive 1.0 is added..
                        # multiplication += np.log(np.exp(-(-self.Pr(neg_pi, h_test))))

                        multiplication += -(-self.Pr(neg_pi, h_test))

                    if multiplication > max_h_value:
                        max_h_value = multiplication
                        max_h = h_test


            h_prime = max_h
            # print("h prime : ", h_prime)

            nldd0 = nldd1
            # print("nldd0 : ", nldd0)
            if h_prime in self.dd_value_table:
                nldd1 = self.dd_value_table[h_prime]
            else:
                nldd1 = self.DD(h_prime) * -1  # NLDD
                self.dd_value_table[h_prime] = nldd1
            # print("nldd1 : ", nldd1)
            if nldd1 < nldd0:
                best_h = h_prime
                best_DD_value = nldd1*-1
            h = h_prime


        self.average_loop_count += loop_count
        # print("Loop Count : ", loop_count)
        # print("nldd1/-1 : ", nldd1/-1.0)
        # print("******")
        return best_h, best_DD_value


    def getTestInfo(self):
         # method : checked state, model : linear or exponential
        return self.H_METHOD, self.M_MODEL, self.test_indices, self.test_instances, self.shortest_positive_bag