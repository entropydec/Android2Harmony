'''

存储数据库中每个app信息的存储单元；
与数据库表项的对应：
appId->app_id
apkName->apk_name
packageName->package_name
version->version
states->相应app中所有的state数据，以<state_id,state_info>键值对存入hashMap中。
appJumpMap->相应app中的Transition信息组合成的跳转关系图
scenarios->相应app中的场景集合

author zhouxinyu

'''


class App:

    def __init__(self, app_id=None, apk_path=None, main_activity=None,
                 package_name=None, version=None, source_code_path=None, permissions=None):
        self.app_id = app_id
        self.apk_path = apk_path
        self.source_code_path = source_code_path
        self.package_name = None if package_name == '' else package_name
        self.version = None if version == '' else version
        # self.states = {}
        self.main_activity = None if main_activity == '' else main_activity
        # self.transitions = {}
        self.permissions = [] if permissions is None else permissions

    def set_id(self, id):
        self.app_id = id

    def set_apk_path(self, apk_path):
        self.apk_path = apk_path

    def set_package_name(self, pck):
        self.package_name = pck

    def set_version(self, v):
        self.version = v

    def set_source_code_path(self, source_code_path):
        self.source_code_path = source_code_path

    # def set_states(self, s):
    #     if self.states is None:
    #         self.states = {}
    #     self.states.update(s)

    # def set_scenarios(self, sc):
    #     if self.scenarios is None:
    #         self.scenarios = []
    #     self.scenarios.extend(sc)

    def get_id(self):
        return self.app_id

    def get_apk_path(self):
        return self.apk_path

    def get_package_name(self):
        return self.package_name

    def get_version(self):
        return self.version

    # def get_states(self):
    #     return self.states
    #
    # def get_transitions(self):
    #     return self.transitions

    # def get_scenarios(self):
    #     return self.scenarios

    def get_main_activity(self):
        return self.main_activity

    def set_main_activity(self, main_activity):
        self.main_activity = main_activity

    def get_source_code_path(self):
        return self.source_code_path

    def get_permissions(self):
        return self.permissions

    def __str__(self):
        return "[app_id:" + str(self.app_id) + " apk_path:" + str(self.apk_path) + " package_name:" + str(
            self.package_name) + " version:" + str(self.version) + "]"
