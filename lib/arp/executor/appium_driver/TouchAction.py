import time

from executor.appium_driver.AppiumScriptDriver import AppiumScriptDriver
from executor.appium_driver.UIObjectWrapper import UIObjectWrapper
from functools import wraps


# def dialog_box_handler(func):
#     @wraps(func)
#     def wrap(self, *args, **kwargs):
#         trigger_identifier = {'textMatches': 'Y|y|ALLOW|allow|OK|ok|是|确认|确定|同意|Continue|continue|CONTINUE|继续'}
#         allow_button = self.device(**trigger_identifier)
#         while self.device.info['currentPackageName'] != self.driver.capabilities['appPackage'] and allow_button.exists:
#             self.driver.current_state = self.monitor.before_click(self.driver.current_state)
#             allow_button.click()
#             time.sleep(2)
#             self.driver.current_state = self.monitor.after_click(self.driver.current_state, trigger_identifier)[0]
#             allow_button = self.device(**trigger_identifier)
#         return func(self, *args, **kwargs)
#
#     return wrap


class TouchAction:
    def __init__(self, driver: AppiumScriptDriver):
        self.driver = driver
        self.monitor = driver.monitor
        self.actions = []
        self.device = driver.device

    def press(self, el: UIObjectWrapper = None, x=None, y=None):
        self.actions.append({'action': 'press', 'options': {'el': el, 'x': x, 'y': y}})
        return self

    def tap(self, el: UIObjectWrapper = None, x=None, y=None):
        return self.press(el, x, y)

    # duration单位是ms
    def long_press(self, el: UIObjectWrapper = None, x=None, y=None, duration=None):
        self.actions.append({'action': 'longPress', 'options': {'el': el, 'x': x, 'y': y, 'duration': duration}})
        return self

    def move_to(self, el: UIObjectWrapper = None, x=None, y=None):
        self.actions.append({'action': 'moveTo', 'options': {'el': el, 'x': x, 'y': y}})
        return self

    def release(self):
        self.actions.append({'action': 'release', 'options': {}})
        return self

    # 等待时间单位是ms
    def wait(self, ms=0):
        self.actions.append({'action': 'wait', 'options': {'ms': ms}})
        return self

    def perform(self):
        exec_queue = []
        for action in self.actions:
            if len(exec_queue) > 0 and not self.can_group(exec_queue[-1], action):
                self.handle_exec_queue(exec_queue)
            exec_queue.append(action)
        self.handle_exec_queue(exec_queue)
        self.actions.clear()

    # @dialog_box_handler
    def handle_exec_queue(self, exec_queue):
        if len(exec_queue) == 1:
            if exec_queue[0]['action'] in ['tap', 'press']:
                self.execute_click(exec_queue)
            elif exec_queue[0]['action'] == 'longPress':
                self.execute_long_press(exec_queue)
            elif exec_queue[0]['action'] == 'wait':
                time.sleep(exec_queue[0]['options']['ms'] / 1000)
        elif len(exec_queue) == 2:
            if exec_queue[0]['action'] == 'press' and exec_queue[1]['action'] == 'moveTo':
                self.execute_swipe(exec_queue)
        elif len(exec_queue) == 3:
            if exec_queue[0]['action'] == 'press' and exec_queue[1]['action'] == 'moveTo' \
                    and exec_queue[2]['action'] == 'release':
                self.execute_swipe(exec_queue)
        exec_queue.clear()

    # 判断两个action可以组合在一起
    def can_group(self, action1, action2):
        if action2['action'] == 'moveTo' and action1['action'] in ['press', 'longPress', 'tap']:
            return True
        if action2['action'] == 'release' and action1['action'] == 'moveTo':
            return True
        return False

    def execute_long_press(self, exec_queue):
        long_press = exec_queue[0]
        if long_press['options']['el'] is not None:
            if long_press['options']['duration'] is not None:
                long_press['options']['el'].tap_hold(long_press['options']['duration'])
            else:
                long_press['options']['el'].tap_hold()
        elif long_press['options']['x'] is not None and long_press['options']['y'] is not None \
                and long_press['options']['duration'] is not None:
            self.driver.current_state = self.monitor.before_long_click(self.driver.current_state)
            self.device.long_click(long_press['options']['x'], long_press['options']['y'],
                                   long_press['options']['duration'] / 1000)
            identifier = {'x': long_press['options']['x'], 'y': long_press['options']['y'],
                          'duration': long_press['options']['duration']}
            time.sleep(4)
            self.driver.current_state = self.monitor.after_long_click(self.driver.current_state, identifier)[0]

    def execute_swipe(self, exec_path):
        press = exec_path[0]
        move_to = exec_path[1]
        origin_el = press['options']['el']
        destination_el = move_to['options']['el']
        if origin_el is not None and destination_el is not None:
            self.driver.scroll(origin_el, destination_el)
        elif press['options']['x'] is not None and press['options']['y'] is not None and \
                move_to['options']['x'] is not None and move_to['options']['y'] is not None:
            self.driver.swipe(press['options']['x'], press['options']['y'],
                              move_to['options']['x'], move_to['options']['y'])

    def execute_click(self, exec_queue):
        click = exec_queue[0]
        if click['options']['el'] is not None:
            click['options']['el'].click()
        elif click['options']['x'] is not None and click['options']['y'] is not None:
            self.driver.current_state = self.monitor.before_click(self.driver.current_state)
            self.device.click(click['options']['x'], click['options']['y'])
            identifier = {'x': click['options']['x'], 'y': click['options']['y']}
            time.sleep(4)
            self.driver.current_state = self.monitor.after_click(self.driver.current_state, identifier)[0]
