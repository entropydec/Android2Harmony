import time
from executor.event_extractor.Action import Action
from executor.Strategy import Strategy
from executor.qlearning.QTable import QTable
from comparison.LSTMBasedScenarioDivision import LSTMBasedScenarioDivision

SMALL_REWARD = -500
LARGE_REWARD = 500


class QLearningStrategy(Strategy):

    def __init__(self, arp, device, monitor, parameters):
        super().__init__(arp, device, monitor, parameters)
        self.time_limit = self.parameters['time_limit']
        self.q_table = QTable(self.device, self.arp.get_app().package_name)
        self.scenario_division = LSTMBasedScenarioDivision(self.device, 0.5)

    def get_action(self, state, actions) -> Action:
        # 某个状态第一次被探索到 随机选择一个action
        if self.q_table.new_state(state):
            self.q_table.append_actions(state, actions)
            return self.q_table.get_random_action(state)
        else:
            return self.q_table.get_q_learning_action(state)

    def get_termination(self) -> dict:
        termination = {'start_time': time.time()}
        return termination

    def terminate(self, **termination) -> bool:
        start_time = termination['start_time']
        current_t = time.time()
        return current_t - start_time >= self.time_limit

    def handle_failed_execution(self, state, action, actions):
        action.weight -= 100

    def post_execution(self, source_state, target_state, action):
        reward = self.get_reward(target_state)
        self.q_table.update(source_state, target_state, action, reward)
        print(action.action_type, action.trigger_identify, reward)

    def get_reward(self, target_state):
        # 产生了新的state 返回large reward 否则返回small reward
        if self.scenario_division.new_state(target_state):
            # if self.q_table.new_state(target_state):
            return LARGE_REWARD
        else:
            return SMALL_REWARD
