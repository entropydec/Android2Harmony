from Model.Transition import Transition
from Model.State import State
from Model.Event import Event
from Model.State import State
from uiautomator2 import Device


class TransitionGenerator:
    def __init__(self, arp_id, transitions, states, device: Device):
        self.arp_id = arp_id
        self.transitions = transitions
        self.states = states
        self.device = device

    def build_transition(self, source_state, target_state, trigger_action, trigger_identify: dict):
        transition = Transition(self.arp_id)
        transition.set_source_id(source_state.get_state_id())
        transition.set_target_id(target_state.get_state_id())
        event = Event(trigger_action, trigger_identify, None)
        transition.set_event(event)
        same_transition = self.search_same_transition(transition)
        if same_transition is None:
            transition.set_transition_id(len(self.transitions))
            self.transitions[transition.get_transition_id()] = transition
            return transition
        return same_transition

    # 寻找探索过的相同的transition
    def search_same_transition(self, transition):
        return None
