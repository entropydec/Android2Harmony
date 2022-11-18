from uiautomator2 import Device
from executor.appium_driver.UIObjectWrapper import UIObjectWrapper
import time
import uiautomator2 as u2
from Model.App import App
from Model.Task import Task
from monitor.AndroidEventMonitor import AndroidEventMonitor
from util.ARPPersistence import ARPPersistence
from executor.Executor import ExecutionStrategy
from comparison.StateComparison import StateComparisonStrategy
from functools import wraps

keycodes = {5: 'call',
            6: 'endcall',
            3: 'home',
            82: 'menu',
            4: 'back',
            84: 'search',
            27: 'camera',
            80: 'focus',
            111: 'escape',
            66: 'enter'}


# def dialog_box_handler(func):
#     @wraps(func)
#     def wrap(self, *args, **kwargs):
#         while self.device.info['currentPackageName'] != self.capabilities['appPackage']:
#             if len(self.watchers) == 0:
#                 break
#             for watcher in self.watchers:
#                 if watcher.triggering:
#                     self.current_state = watcher.execute(self.current_state)
#                     break
#         return func(self, *args, **kwargs)
#
#     return wrap


# appium脚本执行驱动,用来替代appium自身的driver
class AppiumScriptDriver:
    def __init__(self, monitor, device: Device, desired_caps=None):
        self.monitor = monitor
        self.device = device
        self.current_state = None
        self.capabilities = {} if not desired_caps else desired_caps

    def implicitly_wait(self, time_to_wait):
        time.sleep(time_to_wait)

    def find_element(self, by, elem):
        if elem.exists:
            return UIObjectWrapper(elem, self, by)
        else:
            raise Exception('No such element!')

    # @dialog_box_handler
    def find_element_by_id(self, id_):
        # time.sleep(2)
        elem = self.device(resourceId=id_)
        return self.find_element({'resourceId': id_}, elem)

    # @dialog_box_handler
    def find_element_by_xpath(self, xpath):
        # time.sleep(2)
        elem = self.device.xpath(xpath)
        return self.find_element({'xpath': xpath}, elem)

    # @dialog_box_handler
    def find_elements_by_class_name(self, name):
        elems = self.device(className=name)
        ui_objects = []
        for instance, elem in enumerate(elems):
            ui_object = self.find_element({'className': name, 'instance': instance}, elem)
            ui_objects.append(ui_object)
        return ui_objects

    # @dialog_box_handler
    def find_element_by_accessibility_id(self, accessibility_id):
        elem = self.device(description=accessibility_id)
        return self.find_element({'description': accessibility_id}, elem)

    # @dialog_box_handler
    def find_element_by_android_uiautomator(self, uia_string):
        uia_string = uia_string.strip()
        if uia_string.startswith('new UiSelector'):
            args = uia_string.split('.')[1:]
            identify = {}
            for arg in args:
                k, v = arg.rtrip(')').split('(')
                v = v.strip('"')
                identify[k] = v
            elem = self.device(**identify)
            return self.find_element(identify, elem)

    def save_screenshot(self, filename):
        self.device.screenshot(filename)

    # @dialog_box_handler
    def press_keycode(self, keycode):
        # 由于bug 将code映射为具体的键
        if keycode in keycodes:
            keycode = keycodes[keycode]
        self.device.press(keycode)

    # @dialog_box_handler
    def scroll(self, origin_el: UIObjectWrapper, destination_el: UIObjectWrapper, duration=600):
        origin_bounds = origin_el.get_attribute('bounds')
        destination_bounds = destination_el.get_attribute('bounds')
        origin_x, origin_y = (origin_bounds[0] + origin_bounds[2]) / 2, \
                             (origin_bounds[1] + origin_bounds[3]) / 2
        destination_x, destination_y = (destination_bounds[0] + destination_bounds[2]) / 2, \
                                       (destination_bounds[1] + destination_bounds[3]) / 2
        self.swipe(origin_x, origin_y, destination_x, destination_y, duration)

    @property
    def page_source(self):
        return self.device.dump_hierarchy()

    # @dialog_box_handler
    def back(self):
        self.current_state = self.monitor.before_back(self.current_state)
        self.device.press('back')
        time.sleep(4)
        self.current_state, _ = self.monitor.after_back(self.current_state)[0]

    # @dialog_box_handler
    def swipe(self, begin_x, begin_y, end_x, end_y, duration=0):
        self.current_state = self.monitor.before_swipe(self.current_state)
        self.device.swipe(begin_x, begin_y, end_x, end_y, duration / 1000)
        identify = {'begin_x': begin_x, 'begin_y': begin_y, 'end_x': end_x, 'end_y': end_y, 'duration': duration}
        time.sleep(4)
        self.current_state, _ = self.monitor.after_swipe(self.current_state, None, identify)[0]

    def launch_app(self):
        self.current_state = self.monitor.before_launch(self.current_state)
        self.device.app_start(self.capabilities['appPackage'], self.capabilities['appActivity'])
        time.sleep(2)
        self.current_state, _ = self.monitor.after_launch(self.current_state)

    def close_app(self):
        self.current_state = self.monitor.before_home(self.current_state)
        self.device.press('home')
        time.sleep(2)
        self.current_state, _ = self.monitor.after_home(self.current_state)
        self.current_state = self.monitor.before_stop(self.current_state)
        self.device.app_stop(self.capabilities['appPackage'])
        time.sleep(2)
        self.current_state, _ = self.monitor.after_stop(self.current_state)

    def update_capabilities(self, **desired_caps):
        for cap in desired_caps:
            self.capabilities[cap] = desired_caps[cap]

    # 判断device和capabilities是否匹配
    @staticmethod
    def check_capabilities(capabilities, device: Device):
        if capabilities is not None:
            if 'appPackage' not in capabilities:
                raise Exception('the attribute appPackage does not in capabilities!')
            d_info = device.device_info
            d_version = d_info['version'].split('.')
            cap_version = capabilities['platformVersion'].split('.')
            if len(d_version) < len(cap_version):
                d_version += ['0'] * (len(cap_version) - len(d_version))
            elif len(cap_version) < len(d_version):
                cap_version += ['0'] * (len(d_version) - len(cap_version))
            if d_version != cap_version:
                raise Exception(
                    f"the version of the device is {d_info['version']} but the platformVersion of the capabilities is {capabilities['platformVersion']}!")
        else:
            raise Exception("missing capabilities!")

    @staticmethod
    def build(desired_caps):
        device = u2.connect_usb()
        # 判断device和capabilities是否匹配
        AppiumScriptDriver.check_capabilities(desired_caps, device)
        app = App(None, None, desired_caps['appActivity'], desired_caps['appPackage'], None)
        task = Task(app, ExecutionStrategy.APPIUM, StateComparisonStrategy.XML, None, app, False)
        monitor = AndroidEventMonitor(task.get_arp(), device)
        driver = AppiumScriptDriver(monitor, device, desired_caps)
        driver.launch_app()
        return driver

    def save_result(self, saved_path):
        arpp = ARPPersistence(self.monitor.app, saved_path)
        arpp.save2disk()
