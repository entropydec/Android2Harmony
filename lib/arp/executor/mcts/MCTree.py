import math
import random
from enum import Enum
from executor.Strategy import Strategy


class Status(Enum):
    unvisited = 1
    out_of_package = -1
    non_terminal = 0


class State:

    def __init__(self, status=Status.non_terminal):
        self.actions = []
        # 已经执行过的边 key: action id ,value: 下一个状态
        self.explored_states = {}
        # 未执行过的边 key: 边id ,value: 下一个状态
        self.unexplored_states = {}
        # 是否被初始化过
        self.initialized = False
        # 节点的状态
        self.status = status

    @property
    def is_terminal(self):
        return self.status != Status.non_terminal

    @property
    def is_full_extended(self):
        return len(self.unexplored_states) == 0

    def init(self, actions):
        if not self.initialized:
            self.actions = actions
            for action in actions:
                self.unexplored_states[action.action_id] = State(Status.unvisited)
            self.initialized = True

    def get_possible_actions(self):
        return self.actions

    def get_next_state(self, action):
        action_id = action.action_id
        if action_id in self.explored_states:
            return self.explored_states[action_id]
        else:
            return self.unexplored_states[action_id]

    def predict(self):
        action_id = random.choice(list(self.unexplored_states.keys()))
        return self.actions[action_id]

    def get_next_state_with_random_choice(self):
        action = random.choice(self.actions)
        return self.get_next_state(action)

    def compute_reward(self):
        if self.status == Status.unvisited:
            return 1
        elif self.status == Status.out_of_package:
            return -1
        else:
            return 0


class Node:

    def __init__(self, state, action=None, parent=None):
        self.state = state
        self.action = action
        self.parent = parent
        # 是否是终止节点
        self.terminal = state.status != Status.non_terminal
        # 子节点 key: action id value : node
        self.children = {}
        # 收益值
        self.quality_value = 0
        # 模拟次数
        self.visit_time = 0

    @property
    def is_terminal(self):
        return self.terminal

    # 是否完全扩展
    @property
    def is_full_expanded(self):
        return len(self.children) == len(self.state.actions)


class MCTree:
    def __init__(self):
        # 状态集合 key:页面state id value:state
        self.states = {}

    # 初始化节点 添加可执行的action边
    def init(self, state, actions):
        state_id = state.get_state_id()
        if state_id not in self.states:
            self.states[state_id] = State()
        self.states[state_id].init(actions)

    # 扩展 将下一步跳转后的节点添加到对应边的位置
    def extend(self, source_state, target_state, action, status):
        source_id = source_state.get_state_id()
        target_id = target_state.get_state_id()
        if target_id not in self.states:
            self.states[target_id] = State(status)
        parent = self.states[source_id]
        child = self.states[target_id]
        if action.action_id in parent.unexplored_states:
            parent.unexplored_states.pop(action.action_id)
            parent.explored_states[action.action_id] = child
        else:
            parent.explored_states[action.action_id] = child

    # 获取action
    def get_action(self, current_state):
        random_num = random.uniform(0, 1)
        # 0.03概率会选择系统事件
        if random_num <= 0.03:
            return Strategy.get_system_action()
        state = self.states[current_state.get_state_id()]
        # 当前state为终止状态会选择系统事件
        if state.is_terminal:
            return Strategy.get_system_action()
        elif not state.is_full_extended:
            return state.predict()
        else:
            node = Node(state)
            best_child = self.monte_carlo_tree_search(node)
            return best_child.action

    def uct(self, node, parent, C):
        return node.quality_value / node.visit_time + C * math.sqrt(math.log(parent.visit_time) / node.visit_time)

    # 扩展
    def expand(self, node):
        state = node.state
        actions = state.get_possible_actions()
        for action in actions:
            if action.action_id not in node.children:
                next_state = state.get_next_state(action)
                new_node = Node(next_state, action, node)
                node.children[action.action_id] = new_node
                return new_node
        raise Exception("Should never reach here")

    # 反向传播
    def backpropagate(self, node, reward):
        while node is not None:
            node.visit_time += 1
            node.quality_value += reward
            node = node.parent

    # 选择最佳节点
    def get_best_child(self, node, is_exploration=True):
        """
          使用UCB算法，权衡exploration和exploitation后选择得分最高的子节点，注意如果是预测阶段直接选择当前Q值得分最高的。
        """
        best_value = None
        best_child = []
        if is_exploration:
            C = 1 / math.sqrt(2.0)
        else:
            C = 0.0
        for child in node.children.values():
            value = self.uct(child, node, C)
            if best_value is None or value > best_value:
                best_child.clear()
                best_child.append(child)
                best_value = value
            elif best_value == value:
                best_child.append(child)
        # 如果多个节点uct值相等，随机选择其中一个
        return random.choice(best_child)

    def default_policy(self, node):
        """
        蒙特卡洛树的simulation阶段，输入一个需要expand的节点，创建新的节点，返回新增节点的reward，
        基本策略是基于随机/模型选择action
        """
        current_state = node.state
        while not current_state.is_terminal:
            current_state = current_state.get_next_state_with_random_choice()
        final_reward = current_state.compute_reward()
        return final_reward

    def tree_policy(self, node):
        """
        蒙特卡罗树搜索的Selection和Expansion阶段，传入当前需要开始搜索的节点（例如根节点），根据exploration/exploitation算法返回最好的需要expend的节点，注意如果节点是叶子结点直接返回。
        基本策略是先找当前未选择过的子节点，如果有多个则随机选。如果都选择过就找权衡过exploration/exploitation的UCB值最大的，如果UCB值相等则随机选。
        """
        while not node.is_terminal:
            if node.is_full_expanded:
                node = self.get_best_child(node)
            else:
                return self.expand(node)
        # 返回终止状态节点
        return node

    def monte_carlo_tree_search(self, node):
        """
         实现蒙特卡洛树搜索算法，传入一个根节点，在有限的时间内根据之前已经探索过的树结构expand新节点和更新数据，然后返回只要exploitation最高的子节点。
         蒙特卡洛树搜索包含四个步骤，Selection、Expansion、Simulation、Backpropagation。
         前两步使用tree policy找到值得探索的节点。
         第三步使用default policy也就是在选中的节点上随机算法选一个子节点并计算reward。
         最后一步使用backup也就是把reward更新到所有经过的选中节点的节点上。
         进行预测时，只需要根据Q值选择exploitation最大的节点即可，找到下一个最优的节点。
         """
        # 迭代次数
        computation_budget = 1000
        for i in range(computation_budget):
            # 搜索最佳节点 如果存在未选择的子节点 优先选择未访问的子节点
            best_node = self.tree_policy(node)
            # 随机游走 获取节点的价值
            reward = self.default_policy(best_node)
            # 反向传播 更新父节点的值
            self.backpropagate(best_node, reward)
        best_next_child = self.get_best_child(node, False)
        return best_next_child
