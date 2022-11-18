from uiautomator2 import Device
from executor.event_extractor.Action import Action
import time
from executor.DeviceWrapper import DeviceWrapper
from Model.App import App


class Watcher(DeviceWrapper):
    def __init__(self, device: Device, monitor, app: App):
        super().__init__(device, monitor, app)
        self.device = device
        self.monitor = monitor
        self.triggers = []
        self.actions = []

    def when(self, **trigger):
        self.triggers.append(trigger)
        return self

    @property
    def triggering(self):
        for trigger in self.triggers:
            if not self.device(**trigger).exists:
                return False
        return True

    def __append_action(self, action_type, trigger_identifier=None):
        self.actions.append(Action(len(self.actions), action_type, trigger_identifier))
        return self

    def click(self, **trigger_identifier):
        return self.__append_action(Action.click, trigger_identifier)

    def edit(self, **trigger_identifier):
        return self.__append_action(Action.editText, trigger_identifier)

    def long_click(self, **trigger_identifier):
        return self.__append_action(Action.longClick, trigger_identifier)

    def swipe_down(self):
        return self.__append_action(Action.swipeDown)

    def swipe_up(self):
        return self.__append_action(Action.swipeUp)

    def swipe_left(self):
        return self.__append_action(Action.swipeLeft)

    def swipe_right(self):
        return self.__append_action(Action.swipeRight)

    def rotation_upside_down(self):
        return self.__append_action(Action.rotationUpSideDown)

    def rotation_natural(self):
        return self.__append_action(Action.rotationNatural)

    def rotation_left(self):
        return self.__append_action(Action.rotationLeft)

    def rotation_right(self):
        return self.__append_action(Action.rotationRight)

    def menu(self):
        return self.__append_action(Action.menu)

    def back(self):
        return self.__append_action(Action.back)

    def home(self):
        return self.__append_action(Action.home)

    def stop(self):
        return self.__append_action(Action.stop)

    def launch(self):
        return self.__append_action(Action.launch)

    def execute(self, current_state):
        for action in self.actions:
            current_state = self.monitor.before_action(current_state)
            self.execute_action(action)
            time.sleep(2)
            current_state, _ = self.monitor.after_action(current_state,
                                                         action.action_type,
                                                         action.trigger_identify)

        return current_state
