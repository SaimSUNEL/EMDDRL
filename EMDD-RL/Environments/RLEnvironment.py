class RLEnvironment(object):
    """Custom and openai gym environments sometimes needs to be preprocessed such as discritization, custom model loading
    All this operations are handled in this class"""
    # Take min and max values from env. spaces with high and low...

    RLENVIRONMENT_DISCRETE = 1
    RLENVIRONMENT_CONTINUOUS = 2

    def __init__(self, environment_name, environment_type, is_step_restricted=False, step_limit=0):
        self.environment_name = environment_name
        # the number of states
        self.state_space = None
        # action number...
        self.ACTION_SPACE_SIZE = None

        # state might be more than 1 dimension, like in Mountain car state space might in two dimension...
        self.STATE_SPACE_DIMENSIONS = None

        self.current_state = None
        self.has_finished = None
        self.next_state = None
        self.current_reward = None
        self.ENVIRONMENT_TYPE = environment_type
        self.has_finished_successfully = None
        self.environment = None

        self.is_step_restricted = is_step_restricted
        self.step_limit = step_limit
        self.step_count = 0

    # specifies whether the state space is discrete of continous..
    def getEnvironmentType(self):
        return self.ENVIRONMENT_TYPE;

    def getStateSpaceDimensions(self):
        return self.STATE_SPACE_DIMENSIONS

    def getActionSpaceSize(self):
        return self.ACTION_SPACE_SIZE

    def preAction(self):
        self.current_state = self.next_state

    def hasFinished(self):
        return self.has_finished

    def getCurrentState(self):
        return self.current_state

        # reset the environment, the environment can be in one of
    def reset(self):
        self.current_state = self.next_state = self.current_state = self.environment.reset()
        self.has_finished = False

    def applyAction(self, action):
        self.next_state, self.current_reward, self.has_finished, info = self.environment.step(action)
        self.has_finished_successfully = info["issuccesful"]
        return self.next_state, self.current_reward

    def preEpisode(self):
        self.environment.has_finished_successfully = False
        self.step_count = 0
        pass

    def isSuccessfullFinish(self):
        return self.has_finished_successfully

    def afterEpisode(self):
        pass

    def afterAction(self):
        self.step_count += 1
        if self.is_step_restricted:
            if self.step_count == self.step_limit:
                self.has_finished_successfully = False
                # terminate current episode...
                self.has_finished = True
                print("Step limit reached...")

    def preExperiment(self):
        pass

    def afterExperiment(self):
        pass

    def renderEnvironment(self):
        self.environment.render()
