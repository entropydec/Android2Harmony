from executor.Executor import Executor
from executor.event_extractor.Action import Action
import time
import random
from executor.event_extractor.EventExtractor import EventExtractor


class Strategy(Executor):
    system_actions = [Action(0, Action.rotationNatural, None),
                      Action(1, Action.rotationLeft, None),
                      Action(2, Action.rotationRight, None),
                      Action(3, Action.rotationUpSideDown, None),
                      Action(4, Action.home, None)]

    @classmethod
    def is_system_action(cls, action):
        return action in cls.system_actions

    @classmethod
    def get_system_action(cls):
        random_num = random.randint(0, len(cls.system_actions) - 1)
        return cls.system_actions[random_num]

    def __init__(self, arp, device, monitor, parameters):
        super().__init__(arp, device, monitor, parameters)
        self.app = self.arp.get_app()

    def handle_out_of_package_exception(self, current_state, time_out=60):
        if not self.app_exists():
            self.install_app()
        start_time = time.time()
        while self.out_of_package():
            if time.time() - start_time >= time_out:
                raise RuntimeError('Out Of Package Exception Handling timed out')
            if not self.app_exists():
                self.install_app()
            if len(self.watchers) == 0:
                time.sleep(time_out)
            for watcher in self.watchers:
                if watcher.triggering:
                    current_state = watcher.execute(current_state)
                    break
        return current_state

    # 抽取state的actions
    def infer_events(self, state):
        extractor = EventExtractor(state, self.app.package_name, self.app.main_activity)
        # 这里不区分event和action
        actions = extractor.extract_actions()
        return actions

    def pre_execution(self):
        pass

    def get_action(self, state, actions) -> Action:
        pass

    def get_termination(self) -> dict:
        pass

    """
    termination:终止执行的条件 
    :return True表示终止执行 False表示继续执行
    """

    def terminate(self, **termination) -> bool:
        pass

    def handle_failed_execution(self, state, action, actions):
        pass

    def post_execution(self, source_state, target_state, action):
        pass

    def timeout(self, start_time, limit_time):
        current_time = time.time()
        return current_time - start_time > limit_time

    def execute(self):
        # 刚开始app会进入启动后的页面 不需要再启动app
        current_state = self.monitor.before_action(None)
        termination = self.get_termination()
        while not self.terminate(**termination):
            if self.out_of_package():
                current_state = self.handle_out_of_package_exception(current_state)
            actions = self.infer_events(current_state)
            action = self.get_action(current_state, actions)
            # 若执行失败 处理action
            while not self.execute_action(action):
                self.handle_failed_execution(current_state, action, actions)
                action = self.get_action(current_state, actions)
            time.sleep(2)
            next_state, _ = self.monitor.after_action(current_state, action.action_type,
                                                      action.trigger_identify)
            self.post_execution(current_state, next_state, action)
            current_state = next_state
