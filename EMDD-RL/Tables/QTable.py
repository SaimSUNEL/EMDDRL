import numpy as np
import random
class QTable(object):
    def __init__(self, state_space_dimension, action_space_size, learning_rate, discount, epsilon, eligibility_trace=False, trace_factor =0.35):
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.discount_rate = discount
        self.action_space_size = action_space_size
        self.state_space_dimension = [a for a in state_space_dimension]
        # state space combine with action space
        self.state_space_dimension.append(action_space_size)
        self.Q_Table = np.zeros(self.state_space_dimension, dtype=np.float32)
        if eligibility_trace == True:
            self.Eligibily_Trace = np.zeros(self.state_space_dimension, dtype=np.float32)
            self.trace_factor = trace_factor

    def updateQTable(self, current_state, current_action, next_state, reward):
        # print("current state : ", current_state)
        # print("current action : ", current_action)
        # print("next state : ", next_state)
        # print("reward : ", reward)
        # print("\n\n")
        if len(self.state_space_dimension) == 2:
            self.Q_Table[current_state][current_action] += \
                self.learning_rate*(reward + self.discount_rate*self.getMaxActionValue(next_state)-self.Q_Table[current_state][current_action])

        elif len(self.state_space_dimension) == 3:
            self.Q_Table[current_state[0]][current_state[1]][current_action] += \
                self.learning_rate * (reward + self.discount_rate * self.getMaxActionValue(next_state) -
                                      self.Q_Table[current_state[0]][current_state[1]][current_action])


    def updateSarsaTable(self, current_state, current_action, next_state, next_action, reward):
        # print("current state : ", current_state)
        # print("current action : ", current_action)
        # print("next state : ", next_state)
        # print("reward : ", reward)
        # print("\n\n")
        if len(self.state_space_dimension) == 2:
            self.Q_Table[current_state][current_action] += \
                self.learning_rate*(reward + self.discount_rate*self.Q_Table[next_state][next_action]-self.Q_Table[current_state][current_action])

        elif len(self.state_space_dimension) == 3:
            self.Q_Table[current_state[0]][current_state[1]][current_action] += \
                self.learning_rate * (reward + self.discount_rate * self.Q_Table[next_state[0]][next_state[1]][next_action] -
                                      self.Q_Table[current_state[0]][current_state[1]][current_action])

    def updateSarsaLambdaTable(self, current_state, current_action, next_state, next_action, reward):
        if len(self.state_space_dimension) == 2:
            TD_Error = reward + self.discount_rate * self.Q_Table[next_state][next_action] - self.Q_Table[current_state][current_action]

            self.Eligibily_Trace[current_state][current_action] += 1.0

            self.Q_Table += self.learning_rate * TD_Error * self.Eligibily_Trace

            self.Eligibily_Trace *= self.trace_factor*self.discount_rate

        elif len(self.state_space_dimension) == 3:
            TD_Error = reward + self.discount_rate * \
                       self.Q_Table[next_state[0]][next_state[1]][next_action] \
                       - self.Q_Table[current_state[0]][current_state[1]][current_action]

            self.Eligibily_Trace[current_state[0]][current_state[1]][current_action] += 1.0

            self.Q_Table += self.learning_rate * TD_Error * self.Eligibily_Trace

            self.Eligibily_Trace *= self.trace_factor*self.discount_rate

    # Watkins Q. if selected action is the max action (not exploratory) then normal decay
    # else eligibility is zeroed
    def updateWatkinsQLambdaTable(self, current_state, current_action, next_state, next_action, reward):
        if len(self.state_space_dimension) == 2:
            # max action in next state ...
            a_max = self.getMaxAction(next_state)

            # increase eligibility trace with 1
            self.Eligibily_Trace[current_state][current_action] += 1.0

            TD_Error = reward + self.discount_rate * self.Q_Table[next_state][a_max] - \
                       self.Q_Table[current_state][current_action]

            self.Q_Table += self.learning_rate * TD_Error * self.Eligibily_Trace


            # if non-greedy chosen stop learning...
            if next_action == a_max:
                self.Eligibily_Trace *= self.trace_factor*self.discount_rate
            else:
                self.Eligibily_Trace = np.zeros(self.state_space_dimension, dtype=np.float32)

        elif len(self.state_space_dimension) == 3:
            TD_Error = reward + self.discount_rate * \
                       self.getMaxActionValue(next_state) \
                       - self.Q_Table[current_state[0]][current_state[1]][current_action]

            self.Eligibily_Trace[current_state[0]][current_state[1]][current_action] += 1.0
            max_action = self.getMaxAction(current_state)

            self.Q_Table += self.learning_rate * TD_Error * self.Eligibily_Trace

            # if non-greedy chosen stop learning...
            if current_action == max_action:
                self.Eligibily_Trace *= self.trace_factor
            else:
                self.Eligibily_Trace = np.zeros(self.state_space_dimension, dtype=np.float32)

    def updatePengQLambdaTable(self, current_state, current_action, next_state, reward):
        if len(self.state_space_dimension) == 2:
            # max action in next state ...
            # e_prime = reward + gamma * V(x(t+1)) - Q(x(t), a)
            e_prime = reward + self.discount_rate * self.getMaxActionValue(next_state)- \
                      self.Q_Table[current_state][current_action]
            # e = reward + gamma * V(x(t+1))-V(x(t))
            e = reward + self.discount_rate*self.getMaxActionValue(next_state) - \
                self.getMaxAction(current_state)
            # first apply trace decay...
            self.Eligibily_Trace *= self.trace_factor*self.discount_rate
            # update Q table
            self.Q_Table += self.learning_rate * e * self.Eligibily_Trace

            # update Q(current, a) = Q(current, a)+learning_rate*e_prime again (?)
            self.Q_Table[current_state][current_action] += self.learning_rate*e_prime

            # increase current state, action trace value...
            self.Eligibily_Trace[current_state][current_action] += 1.0

        elif len(self.state_space_dimension) == 3:
            pass
    def getMaxActionValue(self, state):
        if len(self.state_space_dimension) == 2:
            return np.max(self.Q_Table[state])
        elif len(self.state_space_dimension) == 3:
            return np.max(self.Q_Table[state[0]][state[1]])
    # If at least two actions have the same Q value then randomly one of them is chosen...
    def getMaxAction(self, state):
        chosen_action = None
        if len(self.state_space_dimension) == 2:
            chosen_action = np.random.choice(np.flatnonzero(self.Q_Table[state] == self.Q_Table[state].max()))
        elif len(self.state_space_dimension) == 3:
            chosen_action = np.argmax(self.Q_Table[state[0]][state[1]])

        return chosen_action


    def sampleAction(self, current_state):
        if len(self.state_space_dimension) == 2:
            if random.random() < self.epsilon:
                return np.random.choice(range(self.action_space_size))
            else:
                return self.getMaxAction(current_state)
        elif len(self.state_space_dimension) == 3:
            if random.random() < self.epsilon:
                return np.random.choice(range(self.action_space_size))
            else:
                return self.getMaxAction(current_state)

    def getVisualPolicy(self):
        character = np.zeros(self.state_space_dimension[0], dtype=np.str)
        way = ['<', 'V', '>', '^']
        for state in range(self.state_space_dimension[0]):
            character[state] = way[np.argmax(self.Q_Table[state])]
        return character.reshape((self.state_space_dimension[0]))

    def getQTable(self):
        return self.Q_Table

    def getLearnedAction(self, current_state):
        return self.getMaxAction(current_state)

    def getConvergenceMetric(self):
        return np.linalg.norm(self.Q_Table)
