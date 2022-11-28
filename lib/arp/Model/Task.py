import uuid

from enum import Enum
import time
from Model.AppRunningPathModel import AppRunningPathModel
from util.ARPHelper import ARPHelper


class TaskStatus(Enum):
    WAITING = 'waiting'
    RUNNING = 'running'
    FINISHED = 'finished'
    SAVING = 'saving'
    END = 'end'
    ERROR = 'error'


class PersistenceType(Enum):
    DISK = 'disk'
    DATABASE_DISK = 'db_disk'


class Task:

    def __init__(self, execution_strategy, state_comparison_strategy, parameters, user_id, arp,
                 instrumentation=False):
        self.task_id = None
        self.execution_strategy = execution_strategy
        self.user_id = user_id
        self.state_comparison_strategy = state_comparison_strategy
        self.arp = arp
        self.parameters = parameters
        self.instrumentation = instrumentation
        self.status = TaskStatus.WAITING
        self.commit_time = time.asctime()
        self.start_time = None
        self.finished_time = None
        self.end_time = None
        self.persistence = PersistenceType.DATABASE_DISK
        self.installed = False
        self.scenarios = []

    def get_execution_strategy(self):
        if self.execution_strategy is None:
            return None
        return self.execution_strategy.value

    def get_state_comparison_strategy(self):
        return self.state_comparison_strategy.value

    def set_installed(self, installed):
        self.installed = installed

    def is_installed(self):
        return self.installed

    def set_task_id(self, task_id):
        self.task_id = task_id

    def get_task_id(self):
        return self.task_id

    def set_commit_time(self, commit_time):
        self.commit_time = commit_time

    def get_commit_time(self):
        return self.commit_time

    def set_start_time(self, start_time):
        self.start_time = start_time

    def get_start_time(self):
        return self.start_time

    def set_finished_time(self, finished_time):
        self.finished_time = finished_time

    def get_finished_time(self):
        return self.finished_time

    def set_end_time(self, end_time):
        self.end_time = end_time

    def get_end_time(self):
        return self.end_time

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status.value

    def get_app(self):
        return self.arp.get_app()

    def set_app(self, app):
        self.arp.set_app(app)

    def get_parameter(self, key):
        if key in self.parameters:
            return self.parameters[key]
        else:
            return None

    def get_parameters(self):
        return self.parameters

    def set_parameter(self, key, value):
        self.parameters[key] = value

    def get_arp(self):
        return self.arp

    def get_user_id(self):
        return self.user_id

    def set_persistence(self, type):
        self.persistence = type

    def set_scenarios(self, scenarios):
        self.scenarios = scenarios

    def get_scenarios(self):
        return self.scenarios
