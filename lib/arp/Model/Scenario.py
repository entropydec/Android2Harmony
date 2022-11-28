'''

场景类，与数据库scenarios表项对应关系：
appId->app_id
scenarioName->scenario_name
description->description
path->path

author zhouxinyu

'''


# id = Column(Integer, primary_key=True, autoincrement=True)
# task_id = Column(Integer)
# name = Column(String(100))
# description = Column(String(200))
# path = Column(String(100))
class Scenario:

    def __init__(self, s_id=None, task_id=None, s_name=None, des=None, path=None):
        self.id = s_id
        self.task_id = task_id
        self.scenario_name = s_name
        self.description = des
        self.path = path

    def get_id(self):
        return self.id

    def get_task_id(self):
        return self.task_id

    def set_name(self, n):
        self.scenario_name = n

    def set_des(self, d):
        self.description = d

    def set_path(self, p):
        self.path = p

    def get_name(self):
        return self.scenario_name

    def get_des(self):
        return self.description

    def get_path(self):
        return self.path

    def __str__(self):
        return "[id:" + str(self.id) + " scenario_name:" + str(self.scenario_name) + " description:" + str(
            self.description) + " path:" + str(self.path) + "]"
