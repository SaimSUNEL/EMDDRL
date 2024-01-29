import  Environments.RLEnvironment as RLEnvironment
import gym
import Environments.KeyRoomEnvironment as KeyRoomEnvironment

# different papers might setup the same environment but with different reward and goal schemes...
class RLKeyRoomEnvironment(RLEnvironment.RLEnvironment):
    def __init__(self,version_number, free_travelling_reward = 0, goal_reward = {103: 1.0}, terminal_states= [103], is_step_restricted = False, step_limit=0):
        super(RLKeyRoomEnvironment, self).__init__("KeyRoomEnvironment", self.RLENVIRONMENT_DISCRETE, is_step_restricted, step_limit)

        from gym import envs
        # print(envs.registry.all())
        self.environment = gym.make('KeyRoomEnvironment-'+version_number)

        # for restricting step in episodes, when agent reaches the limit the episode finishes...
        # no extra reward is returned...

        self.ACTION_SPACE_SIZE = 4
        self.STATE_SPACE_DIMENSIONS = [self.environment.row_tile_count*
                                       self.environment.column_tile_count]
        self.reset()

    def getStartingStates(self):
        return self.environment.getStartingStates()

    def getGoalState(self):
        return self.environment.getGoalState()

    def applyAction(self, action):
        self.next_state, self.current_reward, self.has_finished, info = self.environment.step(action)
        self.has_finished_successfully = info["issuccesful"]
        return self.next_state, self.current_reward

    def setEnableOptionDisplay(self, val):
        self.environment.setEnableOptionDisplay(val)

    def setDisplayOption(self, options):
        self.environment.setDisplayOption(options)


    def setEnableSegmentDisplay(self, val):
        self.environment.setEnableSegmentDisplay(val)

    def setDisplaySegment(self, val):
        self.environment.setDisplaySegment(val)

    def setEnablePolicyDisplay(self, val):
        self.environment.setEnablePolicyDisplay(val)
    def setDisplayPolicy(self, pol):
        self.environment.setDisplayPolicy(pol)

    def setEnableValueDisplay(self, val):
        self.environment.setEnableValueDisplay(val)
    def setDisplayValue(self, value):
        self.environment.setDisplayValue(value)

    def setEnableSubgoalDisplay(self, val):
        self.environment.setEnableSubgoalDisplay(val)

    def setDisplaySubgoal(self, subgoal):
        self.environment.setDisplaySubgoal(subgoal)

    def getEnvironmentGraph(self):
        return self.environment.getEnvironmentGraph()


    def saveEnvironmentImage(self, file_name):
        self.environment.saveEnvironmentImage(file_name)
        pass

    def setEnvironmentImageTitle(self, name):
        self.environment.setEnvironmentImageTitle(name)
        pass

    def setEnablePathDisplay(self, val):
        self.environment.setEnablePathDisplay(val)

    def setPathData(self, instance_bag, color=(0, 0, 150)):
        self.environment.setPathData(instance_bag, color)

    def setEnableRelationDisplay(self, val):
        self.environment.setEnableRelationDisplay(val)
        # color  = {local peak: color1, local_peak2: color2 ....}

    def setRelationData(self, data, color={}):
        self.environment.setRelationData(data, color)

    def getSurfaceValueData(self, data):
        return self.environment.getSurfaceValueData(data)

    def setEnableColorState(self, val):
        return self.environment.setEnableColorState(val)

    def setColorData(self, dictionary):
        return self.environment.setColorData(dictionary)