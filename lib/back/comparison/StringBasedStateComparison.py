from comparison.StateComparison import StateComparison
from Model.State import State


class StringBasedStateComparison(StateComparison):
    def __init__(self, arp, device):
        super().__init__(arp, device)
        self.states = self.arp.get_states()

    def compress_xml(self, xml):
        return "".join([line.strip() for line in xml.splitlines()])

    def compare_states(self, current_state: State) -> None:
        current_layout = self.compress_xml(current_state.get_layout())
        for state in self.states.values():
            if current_layout == self.compress_xml(state.get_layout()):
                return state
        return None
