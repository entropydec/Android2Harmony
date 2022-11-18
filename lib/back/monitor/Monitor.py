from uiautomator2 import Device
from Model.App import App
from Model.AppRunningPathModel import AppRunningPathModel
from comparison.StateComparison import StateComparison
from monitor.StateGenerator import StateGenerator
from monitor.TransitionGenerator import TransitionGenerator
from Model.Task import Task


class Monitor:

    def __init__(self, arp: AppRunningPathModel, device: Device, state_comparison: StateComparison = None):
        self.device = device
        self.arp = arp
        self.app = arp.get_app()
        self.state_comparison = state_comparison
        transitions = arp.get_transitions()
        states = arp.get_states()
        self.state_generator = StateGenerator(arp.arp_id, states, device, state_comparison)
        self.transition_generator = TransitionGenerator(arp.arp_id, transitions, states, device)

    def before_action(self, current_state):
        pass

    def after_action(self, source_state, trigger_action, trigger_identify):
        pass

    def before_click(self, current_state):
        pass

    def after_click(self, source_state, trigger_identify):
        pass

    def before_long_click(self, current_state):
        pass

    def after_long_click(self, source_state, trigger_identify):
        pass

    def before_edit(self, current_state=None):
        pass

    def after_edit(self, source_state, trigger_identify, value):
        pass

    def before_back(self, current_state=None):
        pass

    def after_back(self, source_state):
        pass

    def before_swipe(self, current_state=None):
        pass

    def after_swipe(self, source_state, direction=None, trigger_identify=None):
        pass

    def before_menu(self, current_state=None):
        pass

    def after_menu(self, source_state):
        pass

    def before_rotation(self, current_state=None):
        pass

    def after_rotation(self, direction, source_state):
        pass

    def before_home(self, current_state=None):
        pass

    def after_home(self, source_state):
        pass

    def before_launch(self, current_state=None):
        pass

    def after_launch(self, source_state):
        pass

    def before_stop(self, current_state=None):
        pass

    def after_stop(self, source_state=None):
        pass
