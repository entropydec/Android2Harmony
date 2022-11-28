from uiautomator2 import Device
from executor.event_extractor.Action import Action
import uiautomator2 as u2
from monitor.Monitor import Monitor
from Model.App import App
import time


class DeviceWrapper:
    def __init__(self, device: Device, monitor: Monitor, app: App):
        self.device = device
        self.monitor = monitor
        self.app = app

    # 当前页面跳出了待测的app
    def out_of_package(self):
        return self.device.info['currentPackageName'] != self.app.get_package_name()

    def stop_app(self, current_state):
        current_state = self.monitor.before_home(current_state)
        self.device.press('home')
        self.device.app_stop(self.app.package_name)
        time.sleep(2)
        current_state = self.monitor.after_home(current_state)[0]
        return current_state

    def launch_app(self, current_state):
        current_state = self.monitor.before_launch(current_state)
        self.device.app_start(self.app.package_name, self.app.main_activity, use_monkey=True)
        time.sleep(2)
        current_state = self.monitor.after_launch(current_state)[0]
        return current_state

    def restart_app(self, current_state):
        current_state = self.stop_app(current_state)
        current_state = self.launch_app(current_state)
        return current_state

    def install_app(self):
        self.device.app_install(self.app.get_apk_path())

    def app_exists(self):
        return self.app.get_package_name() in self.device.app_list()

    # 没有定位到组件就返回False 表示执行失败 成功则返回True
    def execute_action(self, action: Action) -> bool:
        try:
            action_type = action.action_type
            identify = action.trigger_identify
            if action_type == Action.click:
                if 'x' in identify and 'y' in identify:
                    self.device.click(identify['x'], identify['y'])
                else:
                    element = self.device(**identify)
                    if element.exists:
                        element.click()
                    else:
                        return False
            elif action_type == Action.longClick:
                element = self.device(**identify)
                if element.exists:
                    element.long_click()
                else:
                    return False
            elif action_type == Action.editText:
                value = '1'
                if 'input' in action.trigger_identify:
                    value = action.trigger_identify.pop('input')
                element = self.device(**identify)
                action.trigger_identify['input'] = value
                if element.exists:
                    element.set_text(action.trigger_identify['input'])
                else:
                    return False
            elif action_type == Action.swipeLeft:
                self.device.swipe_ext('left')
            elif action_type == Action.swipeRight:
                self.device.swipe_ext("right")
            elif action_type == Action.swipeUp:
                self.device.swipe_ext("up")
            elif action_type == Action.swipeDown:
                self.device.swipe_ext("down")
            elif action_type == Action.rotationLeft:
                self.device.set_orientation('left')
            elif action_type == Action.rotationRight:
                self.device.set_orientation('right')
            elif action_type == Action.rotationNatural:
                self.device.set_orientation('natural')
            elif action_type == Action.rotationUpSideDown:
                self.device.set_orientation('upsidedown')
            elif action_type == Action.back:
                self.device.press('back')
            elif action_type == Action.menu:
                self.device.press('menu')
            elif action_type == Action.home:
                self.device.press('home')
            elif action_type == Action.launch:
                self.device.app_start(self.app.get_package_name(), self.app.get_main_activity(), use_monkey=True)
            elif action_type == Action.stop:
                self.device.app_stop(self.app.get_package_name())
        except u2.exceptions.UiObjectNotFoundError:
            return False
        else:
            return True
