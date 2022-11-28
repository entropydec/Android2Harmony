from comparison.StateComparison import StateComparison
from executor.event_extractor.EventExtractor import EventExtractor


class ActionsBasedStateComparison(StateComparison):

    def __init__(self, arp, device):
        super().__init__(arp, device)
        self.states = self.arp.get_states()
        self.package_name = self.arp.get_app().get_package_name()
        self.main_activity = self.arp.get_app().get_main_activity()
        # key:state_id value:list of actions
        self.actions = {}

    # 比较actions 相同返回True 否则返回False
    def compare_actions(self, actions1, actions2):
        if len(actions1) != len(actions2):
            return False
        for action_id in range(len(actions1)):
            action1 = actions1[action_id]
            action2 = actions2[action_id]
            if action1.action_type != action2.action_type or action1.trigger_identify != action2.trigger_identify:
                return False
        return True

    def compare_states(self, current_state):
        extractor = EventExtractor(current_state, self.package_name, self.main_activity)
        current_actions = extractor.executable_actions
        for state_id in self.actions:
            if self.compare_actions(current_actions, self.actions[state_id]):
                return self.states[state_id]
            else:
                self.actions[len(self.states)] = current_actions
                return None
