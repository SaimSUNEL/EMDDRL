import time

class Mediator(object):
    def __init__(self, agent, environment, episode_count, render_learning=False):
        self.agent = agent
        self.environment = environment
        self.logging = None
        self.EPISODE_COUNT = episode_count
        self.renderLearning = render_learning

    def run(self):
        episode_count = self.EPISODE_COUNT
        time_step = 0
        self.environment.preEpisode()
        self.agent.preEpisode()
        print("Episode count : ", episode_count)
        positive_bag_count = 0
        negative_bag_count = 0
        while episode_count > 0:
            self.environment.preAction()
            selected_action = self.agent.preAction(self.environment.getCurrentState())
            next_state, reward = self.environment.applyAction(selected_action)
            time_step += 1
            self.environment.afterAction()
            self.agent.afterAction(next_state, reward)

            if self.renderLearning == True:
                self.environment.renderEnvironment()
            # time.sleep(0.005)
            if self.environment.hasFinished():
                finish_ = False
                # to be  erased...
                # for faster data gathering
                if self.environment.isSuccessfullFinish():
                    print("***************************Success")
                    print("Success:" +str(positive_bag_count)+"-"+str(negative_bag_count))
                    positive_bag_count += 1

                else:
                    negative_bag_count += 1

                if positive_bag_count >= 20 and negative_bag_count >= 20:
                    pass
                    print("Both positive and negative 50")
                    finish_ = True


                self.environment.afterEpisode()
                self.agent.afterEpisode()

                self.environment.reset()

                time_step = 0
                episode_count -= 1
                print("Episode count : ", episode_count)

                self.environment.preEpisode()
                self.agent.preEpisode()

                if finish_:
                    break

    def experiment(self):
        self.environment.preExperiment()
        self.agent.preExperiment()
        self.run()
        self.environment.afterExperiment()
        self.agent.afterExperiment()