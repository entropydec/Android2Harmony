from monitor.Monitor import Monitor


class AndroidEventMonitor(Monitor):
    def __init__(self, arp, device, state_comparison=None):
        super().__init__(arp, device, state_comparison)

    def before_action(self, current_state=None):
        if not current_state:
            return self.state_generator.catch_state()
        else:
            return current_state

    def after_action(self, source_state, trigger_action, trigger_identify):
        target_state = self.state_generator.catch_state()
        transition = self.transition_generator.build_transition(source_state, target_state, trigger_action,
                                                                trigger_identify)
        return target_state, transition

    def before_click(self, current_state=None):
        return self.before_action(current_state)

    def after_click(self, source_state, trigger_identify):
        return self.after_action(source_state, 'click', trigger_identify)

    def before_long_click(self, current_state):
        return self.before_action(current_state)

    def after_long_click(self, source_state, trigger_identify):
        return self.after_action(source_state, 'long_click', trigger_identify)

    def before_edit(self, current_state=None):
        return self.before_action(current_state)

    def after_edit(self, source_state, trigger_identify, value):
        trigger_identify['input'] = value
        return self.after_action(source_state, 'edit', trigger_identify)

    def before_back(self, current_state=None):
        return self.before_action(current_state)

    def after_back(self, source_state):
        return self.after_action(source_state, 'back', None)

    def before_swipe(self, current_state=None):
        return self.before_action(current_state)

    def after_swipe(self, source_state, direction=None, trigger_identify=None):
        if direction is not None:
            action = f'swipe({direction.lower()})'
        else:
            action = 'swipe'
        return self.after_action(source_state, action, trigger_identify)

    def before_menu(self, current_state=None):
        return self.before_action(current_state)

    def after_menu(self, source_state):
        return self.after_action(source_state, 'menu', None)

    def before_rotation(self, current_state=None):
        return self.before_action(current_state)

    def after_rotation(self, direction, source_state):
        return self.after_action(source_state, f'rotation({direction.lower()})', None)

    def before_home(self, current_state=None):
        return self.before_action(current_state)

    def after_home(self, source_state):
        return self.after_action(source_state, 'home', None)

    def before_launch(self, current_state=None):
        return self.before_action(current_state)

    def after_launch(self, source_state):
        return self.after_action(source_state, 'launch', None)

    def before_stop(self, current_state=None):
        return self.before_action(current_state)

    def after_stop(self, source_state=None):
        return self.after_action(source_state, 'stop', None)
