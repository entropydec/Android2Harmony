from executor.Executor import Executor
import time


class SimpleScriptExecutor(Executor):
    def __init__(self, arp, device, monitor, parameters):
        super().__init__(arp, device, monitor, parameters)
        self.package_name = arp.get_app().get_package_name()
        self.script_path = self.parameters['script_path']
        self.current_state = None

    def execute(self):
        with open(self.script_path, 'r') as f:
            # self.device.app_start(self.package_name)
            for line in f.readlines():
                self.device.app_start(self.package_name)
                time.sleep(1)
                line = line.rstrip('\n')
                for opt in line.split("@"):
                    if opt.startswith('click'):
                        self.execute_click(opt)
                    elif opt == 'back':
                        self.execute_back()
                    elif opt.startswith('swipe'):
                        self.execute_swipe(opt)
                    elif opt.startswith('edit'):
                        self.execute_edit(opt)
                    elif opt.startswith('rotation'):
                        self.execute_rotation(opt)
                    elif opt.startswith('home'):
                        self.execute_home()
                    elif opt.startswith('menu'):
                        self.execute_menu()
                    elif opt.startswith('longclick'):
                        self.execute_longclick(opt)

    def execute_click(self, opt):
        self.current_state = self.monitor.before_click(self.current_state)
        params = opt[6: -1].split(',')
        identify = {}
        for param in params:
            k, v = param.split('=')
            identify[k] = v
        ui_component = self.device(**identify)
        # print(ui_component.info)
        ui_component.click()
        time.sleep(1)
        self.current_state = self.monitor.after_click(self.current_state, identify)[0]

    def execute_back(self):
        self.current_state = self.monitor.before_click(self.current_state)
        self.device.press('back')
        time.sleep(1)
        self.current_state = self.monitor.after_back(self.current_state)[0]

    def execute_swipe(self, opt):
        self.current_state = self.monitor.before_swipe(self.current_state)
        direction = opt[6: -1]
        self.device.swipe_ext(direction, scale=0.9)
        time.sleep(1)
        self.current_state = self.monitor.after_swipe(self.current_state, direction)[0]

    def execute_edit(self, opt):
        self.current_state = self.monitor.before_edit(self.current_state)
        identify = {}
        value = ''
        for param in opt[5:-1].split(','):
            k, v = param.split('=')
            if k != 'value':
                identify[k] = v
            else:
                value = v
        self.device(**identify).set_text(value)
        time.sleep(1)
        self.current_state = self.monitor.after_edit(self.current_state, identify, value)[0]

    def execute_rotation(self, opt):
        self.current_state = self.monitor.before_rotation(self.current_state)
        direction = opt[9:-1]
        # self.device.freeze_rotation(False)
        self.device.set_orientation(direction)
        time.sleep(1)
        self.current_state = self.monitor.after_rotation(direction, self.current_state)[0]

    def execute_home(self):
        self.current_state = self.monitor.before_click(self.current_state)
        self.device.press('home')
        time.sleep(1)
        self.current_state = self.monitor.after_back(self.current_state)[0]

    def execute_menu(self):
        self.current_state = self.monitor.before_click(self.current_state)
        self.device.press('menu')
        time.sleep(1)
        self.current_state = self.monitor.after_back(self.current_state)[0]

    def execute_longclick(self, opt):
        self.current_state = self.monitor.before_long_click(self.current_state)
        params = opt[10: -1].split(',')
        identify = {}
        for param in params:
            k, v = param.split('=')
            identify[k] = v
        self.device(**identify).long_click(duration=2)
        time.sleep(1)
        self.current_state = self.monitor.after_long_click(self.current_state, identify)[0]
