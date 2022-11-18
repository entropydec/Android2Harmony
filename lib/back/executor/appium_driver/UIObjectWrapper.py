import time

from uiautomator2 import UiObject


# UI组件的包装类 在执行action前后可以用monitor收集信息
class UIObjectWrapper:
    def __init__(self, element, driver, trigger_identifier):
        # 通过xpath获得的element是XMLElement对象，其他是UiObject对象
        self.element = element
        self.driver = driver
        self.monitor = driver.monitor
        self.trigger_identifier = trigger_identifier

    def get_attribute(self, name):
        if name == 'bounds':
            return self.element.bounds()
        return self.element.info[name]

    def click(self):
        self.driver.current_state = self.monitor.before_click(self.driver.current_state)
        self.element.click()
        time.sleep(4)
        self.driver.current_state = self.monitor.after_click(self.driver.current_state, self.trigger_identifier)[0]

    def send_keys(self, value):
        self.driver.current_state = self.monitor.before_edit(self.driver.current_state)
        self.element.set_text(value)
        time.sleep(4)
        self.driver.current_state = self.monitor.after_edit(self.driver.current_state, self.trigger_identifier, value)[0]

    # 长按
    def tap_hold(self, duration=1.0):
        self.driver.current_state = self.monitor.before_long_click(self.driver.current_state)
        if isinstance(self.element, UiObject):
            self.element.long_click(duration)
        else:
            # XMLElement的longclick方法不能指定duration
            self.element.long_click()
        time.sleep(4)
        self.driver.current_state = self.monitor.after_long_click(self.driver.current_state, self.trigger_identifier)[0]

    def clear(self):
        self.element.set_text('')
        time.sleep(1)
