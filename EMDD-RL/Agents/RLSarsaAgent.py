from Agents import RLAgent
import Tables.QTable
import os

class RLSarsaAgent(RLAgent.RLAgent):

    def __init__(self, environment, learning_rate, epsilon, discount_factor, saveTrajectory=False, trajectoryFileName="", fileNumber=-1):
        super(RLSarsaAgent, self).__init__(environment, learning_rate, epsilon, discount_factor)
        self.Q_Table = Tables.QTable.QTable(environment.getStateSpaceDimensions(), environment.getActionSpaceSize(), learning_rate, discount_factor, epsilon)
        self.environment = environment
        self.current_action = None
        self.next_action = None
        self.current_state = None

        self.trajectory_file_name = trajectoryFileName

        # to be erased
        self.positive_count = 0
        self.negative_count = 0

        self.save_trajectory = saveTrajectory
        if self.save_trajectory:
            if fileNumber == -1:
                experiment_number = 1
                temp_file_name =  trajectoryFileName+"BagExperiment["+str(experiment_number)+"].txt"
                files = os.listdir(".")
                while temp_file_name in files:
                    experiment_number += 1
                    temp_file_name = trajectoryFileName+"BagExperiment[" + str(experiment_number) + "].txt"

            else:
              temp_file_name = trajectoryFileName+"BagExperiment[" + str(fileNumber) + "].txt"


            self.bag_file = open(temp_file_name, "w")
        self.episode_history = []



    def __del__(self):
        if self.save_trajectory:
            self.bag_file.close()

    def preAction(self, state):
        if self.save_trajectory:
            self.episode_history.append(state)
        if self.next_action is None:
            self.next_action = self.sampleAction(state)
        self.current_action = self.next_action
        self.current_state = state
        return self.current_action

    def afterAction(self, next_state, reward):
        super(RLSarsaAgent, self).afterAction(next_state, reward)
        self.next_action = self.sampleAction(next_state)
        self.Q_Table.updateSarsaTable(self.current_state, self.current_action, next_state, self.next_action, reward)

        # pol_ = {}
        # for st in range(self.Q_Table.state_space_dimension[0]):
        #     if st in self.environment.environment.unused_states:
        #         continue
        #     max_opt = self.Q_Table.getLearnedAction(st)
        #     pol_[st] = max_opt
        # self.environment.setEnablePolicyDisplay(True)
        # self.environment.setDisplayPolicy(pol_)


    def afterEpisode(self):
        super(RLSarsaAgent, self).afterEpisode()
        if self.save_trajectory:
            # condition to be erased...
                write_ = False
                if self.environment.isSuccessfullFinish():
                    if self.positive_count < 50:
                        self.bag_file.write("1")
                        self.positive_count += 1
                        write_ = True

                else:
                    if self.negative_count < 50:

                        self.bag_file.write("0")
                        self.negative_count += 1
                        write_ = True
                if write_:
                    for i in range(len(self.episode_history)):
                            self.bag_file.write(","+str(self.episode_history[i]))

                    self.bag_file.write("\n")

    def preEpisode(self):
        super(RLSarsaAgent, self).preEpisode()
        del self.episode_history
        self.episode_history = []
        self.current_action = None
        self.next_action = None

    def sampleAction(self, state):
        return self.Q_Table.sampleAction(state)

    def getVisualPolicy(self):
        return self.Q_Table.getVisualPolicy()

    def getQTable(self):
        return self.Q_Table.getQTable()

    def getLearnedAction(self, state):
        return self.Q_Table.getLearnedAction(state)

    def getConvergenceMetric(self):
        return self.Q_Table.getConvergenceMetric()
