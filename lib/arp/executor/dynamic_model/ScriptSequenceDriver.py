from executor.Executor import Executor
from util.ScriptConverter import ScriptConverter
import time


class ScriptSequenceDriver(Executor):
    def __init__(self, arp, device, monitor, parameters):
        super().__init__(arp, device, monitor, parameters)
        self.actions = []
        self.actions = self.parameters['actions']

    def execute(self):
        current_state = None
        for action in self.actions:
            current_state = self.monitor.before_action(current_state)
            self.execute_action(action)
            time.sleep(4)
            current_state, _ = self.monitor.after_action(current_state, action.action_type, action.trigger_identify)
