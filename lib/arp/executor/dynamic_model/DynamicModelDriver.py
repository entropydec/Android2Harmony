from executor.Executor import Executor
from util.AppHelper import AppHelper
from Model.ExectionGraph import ExecutionGraph
from executor.event_extractor.Action import Action
import time


class DynamicModelDriver(Executor):
    def __init__(self, arp, device, monitor, parameters):
        super().__init__(arp, device, monitor, parameters)
        self.model = AppHelper.disk2memory(parameters['arp_model_path'])
        # self.coverage_threshold = task.get_parameter('coverage_threshold')
        # self.graph = ExecutionGraph(app)

    def execute(self):
        current_state = None
        for transition in self.model.get_transitions().values():
            action = Action(transition.get_transition_id(), transition.get_event().get_trigger_action(),
                            transition.get_event().get_trigger_identifier())
            current_state = self.monitor.before_action(current_state)
            self.execute_action(action)
            time.sleep(4)
            current_state, _ = self.monitor.after_action(current_state, action.action_type, action.trigger_identify)
