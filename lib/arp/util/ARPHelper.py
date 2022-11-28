from Model.AppRunningPathModel import AppRunningPathModel
from orm.SqlHelper import SqlHelper
from orm.DatabaseModels import TableARP, TableState, TableTransition
from util.FileHelper import FileHelper
import os
import json
from Model.App import App
from Model.Transition import Transition
from Model.State import State
from PIL import Image
import re
from Model.Event import Event


class ARPHelper:

    @classmethod
    def create_arp(cls, app, persistence=False):
        arp = AppRunningPathModel(None, app)
        if persistence:
            arp_id = SqlHelper.add_return_key(TableARP, 'arp_id',
                                              app_id=app.get_id(),
                                              create_time=arp.get_create_time(),
                                              update_time=arp.get_update_time())
            arp.set_arp_id(arp_id)
        return arp

    # 保存到磁盘
    @classmethod
    def save2disk(cls, arp: AppRunningPathModel):
        arp_id = arp.get_arp_id()
        states = arp.get_states()
        transitions = arp.get_transitions()
        # 保存state的路径
        screens_path = FileHelper.screens_dir(arp_id)
        # 如果路径不存在就创建
        FileHelper.create_dir(screens_path)
        # 保存transition的路径
        jump_pairs_path = FileHelper.jump_pairs_file(arp_id)
        # 保存activity的路径
        activity_path = FileHelper.activity_info_file(arp_id)
        # 保存state和activity
        with open(activity_path, 'w', encoding='utf-8') as af:
            for state in states.values():
                state.get_picture().save(os.path.join(screens_path, f"{state.get_state_id()}.png"))
                with open(os.path.join(screens_path, f"{state.get_state_id()}.xml"), 'w', encoding='utf-8') as sf:
                    layout = state.get_layout()
                    # if sys.platform.startswith('win'):
                    #     layout = layout.replace(u'\xe4', u'')
                    sf.write(layout)
                af.write(f"{state.get_state_id()} {state.get_activity_name()}\n")

        # 保存transition
        with open(jump_pairs_path, 'w', encoding='utf-8') as f:
            for transition in transitions.values():
                identify = transition.get_event().get_trigger_identifier()
                f.write(
                    f"{transition.get_source_id()} {transition.get_target_id()} "
                    f"{transition.get_event().get_trigger_action()}"
                    f"{'(' + ','.join([str(k) + '=' + str(identify[k]) for k in identify]) + ')' if identify else ''}\n")
        # 创建arp模型压缩包
        FileHelper.zip(FileHelper.arp_model_dir(arp_id), FileHelper.arp_model_zip(arp_id))

    @classmethod
    def save2database(cls, arp: AppRunningPathModel):
        arp_id = arp.get_arp_id()
        states = arp.get_states()
        transitions = arp.get_transitions()
        # 保存state
        states_info = [
            {'id': state.get_state_id(), 'arp_id': arp_id,
             'activity': state.get_activity_name(),
             'picture': FileHelper.screen_file(arp_id, state.get_state_id()),
             'layout': FileHelper.layout_file(arp_id, state.get_state_id())
             } for state in states.values()]
        SqlHelper.add_all(TableState, *states_info)

        # 保存transition
        transitions_info = [{'id': transition.get_transition_id(),
                             'arp_id': arp_id,
                             'source_id': transition.get_source_id(),
                             'target_id': transition.get_target_id(),
                             'trigger_action': transition.get_event().get_trigger_action(),
                             'trigger_identifier': json.dumps(transition.get_event().get_trigger_identifier()),
                             'conditions': json.dumps(transition.get_event().get_conditions())}
                            for transition in transitions.values()]
        SqlHelper.add_all(TableTransition, *transitions_info)

    @classmethod
    def none_str(cls, s):
        if s == 'None' or s == '':
            s = None
        return s

    @classmethod
    def disk2memory(cls, arp_id):
        arp_id = int(arp_id)
        arp = AppRunningPathModel(arp_id)
        screens_dir = FileHelper.screens_dir(arp_id)
        activity_info_file = FileHelper.activity_info_file(arp_id)
        jump_pairs_file = FileHelper.jump_pairs_file(arp_id)

        # 加载app基本信息
        # with open(app_info_file, 'r', encoding='utf-8') as f:
        #     lines = f.readlines()
        #     package_name = cls.none_str(lines[0].strip().split(' ')[1])
        #     version = cls.none_str(lines[1].strip().split(' ')[1])
        #     apk_path = cls.none_str(lines[2].strip().split(' ')[1])
        #     main_activity = cls.none_str(lines[3].strip().split(' ')[1])
        #     source_code = cls.none_str(lines[4].strip().split(' ')[1])
        #     permissions_line = lines[5].strip().split(' ')
        #     if len(permissions_line) < 2:
        #         permissions = []
        #     else:
        #         permissions = permissions_line[1].split(',')
        #     app = App(None, apk_path, main_activity, package_name, version, source_code, permissions)
        #
        states = arp.get_states()
        # 加载state的截图和xml
        for f in os.listdir(screens_dir):
            f_path = os.path.join(screens_dir, f)
            if os.path.isfile(f_path):
                state_id, suffix = os.path.splitext(f)
                if suffix == '.xml' or suffix == '.png':
                    state_id = int(state_id)
                    if state_id in states:
                        state = states[state_id]
                    else:
                        state = State(None, state_id)
                        states[state_id] = state
                        state.set_arp_id(arp_id)
                    if suffix == '.xml':
                        with open(f_path, 'r', encoding='utf-8') as xml_f:
                            state.set_layout(xml_f.read())
                    elif suffix == '.png':
                        state.set_picture(Image.open(f_path).convert('RGB'))
        # 加载state的activity
        with open(activity_info_file, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                if len(line) == 0:
                    continue
                state_id, activity_name = line.split(' ')
                state_id = int(state_id)
                states[state_id].set_activity_name(activity_name)
        # 加载跳转信息
        transitions = arp.get_transitions()
        with open(jump_pairs_file, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                if len(line) == 0:
                    continue
                trans = line.split(' ')
                source_id = int(trans[0])
                target_id = int(trans[1])
                condition = " ".join(trans[2:])
                if condition.startswith('swipe') or condition.startswith('rotation') or not condition.endswith(')'):
                    action_type = condition
                    action_identifier = ''
                else:
                    action_type, action_identifier = re.findall(r"(.*?)\((.*?)\)", condition)[0]
                trigger_identifier = {}
                if len(action_identifier) != 0:
                    for attr in action_identifier.split(','):
                        key, value = attr.split("=")
                        trigger_identifier[key] = value
                transition = Transition(arp_id, len(transitions))
                transition.set_source_id(source_id)
                transition.set_target_id(target_id)
                transition.set_event(Event(action_type, trigger_identifier))
                transitions[transition.get_transition_id()] = transition
        return arp


if __name__ == '__main__':
    arp = ARPHelper.disk2memory(3)
    print(arp)
