from uiautomator2 import Device
from heapq import heappush, heappop, heapify
import random
from executor.Strategy import Strategy

INITIAL_Q_VALUE = 1000
SYSTEM_THRESHOLD = 0.97
EPSILON = 0.9
ALPHA = 0.1
GAMMA = 0.99


class QTable:
    def __init__(self, device: Device, package_name):
        self.device = device
        self.package_name = package_name
        # key:state_id value:the priority queue of actions
        # action可以看成一条边 他的的权重在这里表示q-value
        self.q_table = {}

    def new_state(self, state):
        return state.state_id not in self.q_table

    def out_of_package(self):
        return self.device.info['currentPackageName'] != self.package_name

    # 若新的state 返回True 否则返回False
    def append_actions(self, state, actions):
        state_id = state.state_id
        if state_id not in self.q_table:
            self.q_table[state_id] = []
            for action in actions:
                action.weight = INITIAL_Q_VALUE
                self.push_action(state, action)

    def push_action(self, state, action):
        q_actions = self.q_table[state.state_id]
        heappush(q_actions, action)

    def pop_action(self, state, index=0):
        q_actions = self.q_table[state.state_id]
        if index == 0:
            action = heappop(q_actions)
        else:
            action = q_actions[index]
            del q_actions[index]
            heapify(q_actions)
        return action

    # q-value值最大的action
    def peek_action(self, state):
        return self.q_table[state.state_id][0]

    def get_random_action(self, state):
        state_id = state.state_id
        q_actions = self.q_table[state_id]
        random_num = random.randint(0, len(q_actions) - 1)
        return self.pop_action(state, random_num)

    def get_q_learning_action(self, state):
        random_num = random.uniform(0, 1)
        # 0.03概率选择系统action
        if random_num > SYSTEM_THRESHOLD:
            return Strategy.get_system_action()
        # 0.07概率随机选择action
        if random_num > EPSILON:
            return self.get_random_action(state)
        return self.pop_action(state)

    def update(self, source_state, target_state, action, reward):
        q_value = action.weight
        # 测试跳出了待测应用
        if self.out_of_package():
            if q_value > -950:
                q_value = q_value + ALPHA * 5 * ((-500) + GAMMA * (-500) - q_value)
            else:
                q_value -= 100
        # 探索到新的state
        elif target_state.get_state_id() not in self.q_table:
            q_value = q_value + ALPHA * (reward + GAMMA * 1000 - q_value)
        else:  # 没探索到新的state
            action_with_max_value = self.peek_action(target_state)
            target_max_value = action_with_max_value.weight
            # when the q-value is going to reduce, make it faster
            if reward + GAMMA * target_max_value - q_value < 0:
                q_value = q_value + ALPHA * 5 * (reward + GAMMA * target_max_value - q_value)
            else:
                q_value = q_value + ALPHA * (reward + GAMMA * target_max_value - target_max_value)
        action.weight = q_value
        self.push_action(source_state, action)
