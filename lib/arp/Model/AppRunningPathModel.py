import time


class AppRunningPathModel:
    def __init__(self, arp_id=None, app=None, create_time=time.asctime(), update_time=time.asctime()):
        self.arp_id = arp_id
        self.app = app
        self.create_time = create_time
        self.update_time = update_time
        self.states = {}
        self.transitions = {}

    def get_states(self):
        return self.states

    def get_transitions(self):
        return self.transitions

    def set_arp_id(self, arp_id):
        self.arp_id = arp_id

    def get_arp_id(self):
        return self.arp_id

    def get_app(self):
        return self.app

    def set_app(self, app):
        self.app = app

    def set_states(self, states):
        self.states = states

    def set_transitions(self, transitions):
        self.transitions = transitions

    def set_create_time(self, create_time):
        self.create_time = create_time

    def get_create_time(self):
        return self.create_time

    def set_update_time(self, update_time):
        self.update_time = update_time

    def get_update_time(self):
        return self.update_time
