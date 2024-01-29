import time
import matplotlib.pyplot as plt

class RLAgent(object):
    """Base class for all RL learning agents...
    It implements common functions for all learning agents...
    All environment interactions will be performed on this class
    Derived agents simply provides the decision on the environment
    Model savings are handled on this class
    Learning graphs are drawn here"""

    # later lambda parameter might be needed for eligibility traces...
    def __init__(self, environment, learning_rate, epsilon, discount_factor):
        """environment: openai gym environment to solve (RLEnvironment)
           learning rate: coefficient of change of learning (float)
           discount factor: attenuation factor for future rewards(float)"""
        self.environment = environment
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.total_reward = 0
        # reward accumulated per episode...
        self.episode_reward = []
        self.convergence_batch = []
        self.step_count = 0
        self.episode_step = []

    def preEpisode(self):
        self.total_reward = 0

    def afterEpisode(self):
        self.episode_reward.append(self.total_reward)
        self.convergence_batch.append(self.getConvergenceMetric())
        self.episode_step.append(self.step_count)


    def preEpisode(self):
        # zero reward and step counters...
        self.total_reward = 0
        self.step_count = 0
        pass

    def preAction(self):
        pass

    def afterAction(self, next_state, reward):
        self.total_reward += reward
        self.step_count += 1

    def getVisualPolicy(self):
        pass

    def sampleAction(self):
        pass

    def preExperiment(self):
        pass

    def afterExperiment(self):
        pass

    def getConvergenceMetric(self):
        pass

    def saveModel(self):
        pass

    def loadModel(self):
        pass

    def renderAgent(self):
        self.environment.reset()
        self.environment.renderEnvironment()
        rend_count = 0

        current_action = self.getLearnedAction(self.environment.getCurrentState())

        while not self.environment.hasFinished():
            next_state , _ = self.environment.applyAction(current_action)
            print("Next state : ", next_state)
            self.environment.renderEnvironment()
            time.sleep(0.05)
            current_action = self.getLearnedAction(next_state)
            rend_count += 1

        print(self.environment.hasFinished())
        print(self.current_state)
        print("Rend Count : ", rend_count)
        # print(self.environment.environment.state)

    def plotAccumulatedReward(self):
        x = range(len(self.episode_reward))
        plt.title("Accumulated Reward")
        plt.plot(x, self.episode_reward)
        plt.show()

    def plotConvergence(self):
        x = range(len(self.convergence_batch))
        plt.title("Convergence")
        plt.plot(x, self.convergence_batch)
        plt.show()

    def getRewardPerEpisode(self):
        return self.episode_reward

    def getStepPerEpisode(self):
        return self.episode_step

    def plotStepPerEpisode(self):
        x = range(len(self.episode_step))
        plt.title("Step Per Step")
        plt.plot(x, self.episode_step)
        plt.show()

