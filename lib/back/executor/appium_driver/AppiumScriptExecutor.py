from executor.Executor import Executor
from uiautomator2 import Device
from executor.appium_driver.AppiumScriptDriver import AppiumScriptDriver
import importlib, os
from util.FileHelper import FileHelper
import sys
from executor.appium_driver.UIObjectWrapper import UIObjectWrapper

class TouchAction:
    def __init__(self,device:Device):
        self.device=device
        self.element=None
    def long_press(self,object:UIObjectWrapper):
        return LongPressAction(self,object)
        
class LongPressAction:
    def __init__(self,action:TouchAction,object:UIObjectWrapper):
        self.element=object
    def perform(self):
        self.element.tap_hold()

class AppiumScriptExecutor(Executor):
    def __init__(self, arp, device: Device, monitor, parameters):
        super().__init__(arp, device, monitor, parameters)
        self.script_path = self.parameters['script_path']
        self.driver = AppiumScriptDriver(monitor, device)

    def execute(self):
        prefix, suffix = os.path.splitext(self.script_path)
        if sys.platform.startswith('win'):
            module_name = prefix.replace(FileHelper.project_dir, '').replace('\\', '.')
        else:
            module_name = prefix.replace(FileHelper.project_dir, '').replace('/', '.')
        if module_name.startswith('.'):
            module_name = module_name[1:]
        if suffix == '.py':
            module = importlib.import_module(module_name)
            self.driver.update_capabilities(**module.desired_caps)
            module.run(self.driver)
