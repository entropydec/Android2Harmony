import os
from orm.SqlHelper import SqlHelper
from orm.DatabaseModels import TableState, TableTransition, TableApp
import json
from util.FileHelper import FileHelper
from Model.Task import PersistenceType


class ARPPersistence:
    def __init__(self, app, task):
        self.app = app
        self.states = app.get_states()
        self.transitions = app.get_transitions()
        self.task = task

    #   保存到磁盘
    def save2disk(self):
        user_id = self.task.get_user_id()
        task_id = self.task.get_task_id()
        result_path = FileHelper.result_dir(user_id, task_id)
        # 保存state的路径
        screens_path = FileHelper.screens_dir(user_id, task_id)
        # 如果路径不存在就创建
        if not os.path.exists(screens_path):
            os.makedirs(screens_path)
        # 保存transition的路径
        jump_pairs_path = os.path.join(result_path, 'jump_pairs.txt')
        # 保存activity的路径
        activity_path = os.path.join(result_path, 'activity_info.txt')
        # 保存app信息的路径
        app_path = os.path.join(result_path, 'app_info.txt')
        # 保存state和activity
        with open(activity_path, 'w', encoding='utf-8') as af:
            for state in self.states.values():
                state.get_picture().save(os.path.join(screens_path, f"{state.get_state_id()}.png"))
                with open(os.path.join(screens_path, f"{state.get_state_id()}.xml"), 'w', encoding='utf-8') as sf:
                    layout = state.get_layout()
                    # if sys.platform.startswith('win'):
                    #     layout = layout.replace(u'\xe4', u'')
                    sf.write(layout)
                af.write(f"{state.get_state_id()} {state.get_activity_name()}\n")
        # 保存transition
        with open(jump_pairs_path, 'w', encoding='utf-8') as f:
            for transition in self.transitions.values():
                identify = transition.get_event().get_trigger_identifier()
                f.write(
                    f"{transition.get_source_id()} {transition.get_target_id()} "
                    f"{transition.get_event().get_trigger_action()}"
                    f"{'(' + ','.join([str(k) + '=' + str(identify[k]) for k in identify]) + ')' if identify else ''}\n")
        # 保存app信息
        with open(app_path, 'w', encoding='utf-8') as f:
            f.write(f"packageName {self.app.get_package_name()}\n"
                    f"version {self.app.get_version()}\n"
                    f"apkPath {self.app.get_apk_path()}\n"
                    f"mainActivity {self.app.get_main_activity()}\n"
                    f"sourceCodePath {self.app.get_source_code_path()}\n"
                    f"permissions {','.join(self.app.get_permissions())}")

    # 保存到数据库
    def save2database(self):
        if self.task.persistence == PersistenceType.DATABASE_DISK:
            # 保存state
            states_info = [
                {'id': state.get_state_id(), 'task_id': state.get_task_id(),
                 'activity': state.get_activity_name(),
                 'picture': FileHelper.screen_file(self.task.get_user_id(), self.task.get_task_id(),
                                                   state.get_state_id()),
                 'layout': FileHelper.layout_file(self.task.get_user_id(), self.task.get_task_id(),
                                                  state.get_state_id())
                 } for state in self.states.values()]
            SqlHelper.add_all(TableState, *states_info)

            # 保存transition
            transitions_info = [{'id': transition.get_transition_id(),
                                 'task_id': transition.get_task_id(),
                                 'source_id': transition.get_source_id(),
                                 'target_id': transition.get_target_id(),
                                 'trigger_action': transition.get_event().get_trigger_action(),
                                 'trigger_identifier': json.dumps(transition.get_event().get_trigger_identifier()),
                                 'conditions': json.dumps(transition.get_event().get_conditions())}
                                for transition in self.transitions.values()]
            SqlHelper.add_all(TableTransition, *transitions_info)
