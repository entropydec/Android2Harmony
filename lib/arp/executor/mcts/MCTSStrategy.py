from executor.Strategy import Strategy
from executor.event_extractor.Action import Action
import time
from executor.mcts.MCTree import MCTree
from executor.mcts.MCTree import Status


class MCTSStrategy(Strategy):
    def __init__(self, arp, device, monitor, parameters):
        super().__init__(arp, device, monitor, parameters)
        self.time_limit = self.parameters['time_limit']
        self.mct = MCTree()

    def get_termination(self) -> dict:
        termination = {'start_time': time.time()}
        return termination

    def terminate(self, **termination) -> bool:
        start_time = termination['start_time']
        current_t = time.time()
        return current_t - start_time >= self.time_limit

    def infer_events(self, state):
        actions = super().infer_events(state)
        return actions

    def is_out_of_package(self, state):
        return state.get_package_name() != self.app.get_package_name()

    def post_execution(self, source_state, target_state, action):
        if self.is_out_of_package(target_state):
            status = Status.out_of_package
        else:
            status = Status.non_terminal
        if not Strategy.is_system_action(action):
            self.mct.extend(source_state, target_state, action, status)

    def execute(self):
        # 刚开始app会进入启动后的页面 不需要再启动app
        current_state = self.monitor.before_action(None)
        termination = self.get_termination()
        while not self.terminate(**termination):
            if self.out_of_package():
                current_state = self.handle_out_of_package_exception(current_state)
            actions = self.infer_events(current_state)
            self.mct.init(current_state, actions)
            action = self.mct.get_action(current_state)
            # 若执行失败 处理action
            while not self.execute_action(action):
                action = self.mct.get_action(current_state)
            time.sleep(2)
            next_state, _ = self.monitor.after_action(current_state, action.action_type,
                                                      action.trigger_identify)
            self.post_execution(current_state, next_state, action)
            current_state = next_state
