from Model.Task import Task
from Model.State import State
from uiautomator2 import Device
from enum import Enum
from Model.AppRunningPathModel import AppRunningPathModel


class StateComparisonStrategy(Enum):
    XML = 'xml_comparison'
    ACTION = 'action_based_comparison'
    STRING = "string_comparison"


class StateComparison:

    def __init__(self, arp: AppRunningPathModel, device: Device):
        self.arp = arp
        self.device = device

    def compare_states(self, current_state: State) -> State:
        pass
