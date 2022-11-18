from executor.event_extractor.UIExecutableObject import UIExecutableObject
from executor.event_extractor.Action import Action
from Model.State import State
import xml.etree.ElementTree as ET


# from Model.Event import Event


class EventExtractor:
    def __init__(self, current_state: State, package_name, entry_activity_name):
        self.activity_name = current_state.activity_name
        self.package_name = package_name
        self.entry_activity_name = entry_activity_name
        self.hierarchy = current_state.layout

        self.isScrollable = False

        self.class_type_count = {}

        # 可执行的actions
        self.executable_actions = []

    def extract_actions(self):
        root = ET.fromstring(self.hierarchy)
        ancestor_executable_attributes = {'clickable': False, 'long-clickable': False,
                                          'scrollable': False, 'checkable': False}
        self.analyze_node(root, ancestor_executable_attributes)
        self.add_system_actions()
        return self.executable_actions

    def str2bool(self, string):
        return string == 'true'

    def update_instance(self, class_name):
        if class_name not in self.class_type_count:
            self.class_type_count[class_name] = 0
        else:
            self.class_type_count[class_name] += 1
        return self.class_type_count[class_name]

    # analyze the UI xml nodes
    def analyze_node(self, root, ancestor_executable_attributes):
        for node in list(root):
            self.update_instance(node.get('class'))
            if node.get('scrollable') == 'true':
                self.isScrollable = True
            if len(node) > 0:  # non-leaf nodes
                # depth-first search on the UI tree
                # self.ui_layout_objects.append(UIlo)  # if its parent has a true property, pass it on to its child
                # 祖先节点中的可执行属性向下传递
                executable_attributes = {}
                for attr in ancestor_executable_attributes:
                    executable_attributes[attr] = ancestor_executable_attributes[attr] or self.str2bool(node.get(attr))

                self.analyze_node(node, executable_attributes)
            else:  # leaf nodes --> ui executable object
                # 属于当前app的组件才收集
                if self.package_name == node.get('package'):
                    executable_obj = UIExecutableObject(node, self.class_type_count[node.get('class')],
                                                        ancestor_executable_attributes)
                    self.detect_executable_actions(executable_obj)

    def generate_action(self, action_type, trigger_identify):
        action = Action(len(self.executable_actions), action_type, trigger_identify)
        self.executable_actions.append(action)

    def generate_click_action(self, executable_obj, action_type):
        trigger_identify = {}
        if executable_obj.text:
            trigger_identify['className'] = executable_obj.class_name
            trigger_identify['instance'] = executable_obj.instance
        elif executable_obj.resource_id:
            trigger_identify['resourceId'] = executable_obj.resource_id
        elif executable_obj.content_desc:
            trigger_identify['description'] = executable_obj.content_desc
        if len(trigger_identify) > 0:
            self.generate_action(action_type, trigger_identify)

    def generate_click_image_action(self, executable_obj, action_type):
        trigger_identify = {}
        if executable_obj.resource_id:
            trigger_identify['resourceId'] = executable_obj.resource_id
        elif executable_obj.content_desc:
            trigger_identify['description'] = executable_obj.content_desc
        elif executable_obj.text:
            trigger_identify['className'] = executable_obj.class_name
            trigger_identify['instance'] = executable_obj.instance
        if len(trigger_identify) > 0:
            self.generate_action(action_type, trigger_identify)

    def generate_edit_text_action(self, executable_obj, action_type):
        trigger_identify = {}
        if executable_obj.resource_id:
            trigger_identify['resourceId'] = executable_obj.resource_id
        elif executable_obj.content_desc:
            trigger_identify['description'] = executable_obj.content_desc
        elif executable_obj.text:
            trigger_identify['className'] = executable_obj.class_name
            trigger_identify['instance'] = executable_obj.instance
        if len(trigger_identify) > 0:
            self.generate_action(action_type, trigger_identify)

    def generate_check_action(self, executable_obj, action_type):
        trigger_identify = {}
        if executable_obj.resource_id:
            trigger_identify['resourceId'] = executable_obj.resource_id
        elif executable_obj.text:
            if executable_obj.has_multi_lines_text():
                trigger_identify['textContains'] = executable_obj.get_first_line_text()
            else:
                trigger_identify['text'] = executable_obj.text
        elif executable_obj.content_desc:
            trigger_identify['description'] = executable_obj.content_desc
        else:
            trigger_identify['className'] = executable_obj.class_name
            trigger_identify['instance'] = executable_obj.instance
        if len(trigger_identify) > 0:
            self.generate_action(action_type, trigger_identify)

    def generate_check_textview_action(self, executable_obj, action_type):
        trigger_identify = {}
        if executable_obj.text:
            trigger_identify['className'] = executable_obj.class_name
            trigger_identify['instance'] = executable_obj.instance
        elif executable_obj.resource_id:
            trigger_identify['resourceId'] = executable_obj.resource_id
        elif executable_obj.content_desc:
            trigger_identify['description'] = executable_obj.content_desc
        if len(trigger_identify) > 0:
            self.generate_action(action_type, trigger_identify)

    def generate_seekbar_action(self, executable_obj, action_type):
        trigger_identify = {}
        if executable_obj.resource_id:
            trigger_identify['resourceId'] = executable_obj.resource_id
        elif executable_obj.content_desc:
            trigger_identify['description'] = executable_obj.content_desc
        else:
            trigger_identify['className'] = executable_obj.class_name
            trigger_identify['instance'] = executable_obj.instance
        if len(trigger_identify) > 0:
            self.generate_action(action_type, trigger_identify)

    def detect_executable_actions(self, executable_obj):
        view_type = executable_obj.class_name
        if '.TextView' in view_type or '.Button' in view_type or '.ToggleButton' in view_type:
            if executable_obj.clickable:
                self.generate_click_action(executable_obj, Action.click)
            if executable_obj.long_clickable:
                self.generate_click_action(executable_obj, Action.longClick)
        elif '.ImageView' in view_type or '.ImageButton' in view_type:
            if executable_obj.clickable:
                self.generate_click_image_action(executable_obj, Action.click)
            if executable_obj.long_clickable:
                self.generate_click_image_action(executable_obj, Action.longClick)
        elif '.EditText' in view_type or '.MultiAutoCompleteTextView' in view_type:
            self.generate_edit_text_action(executable_obj, Action.editText)
        elif '.CheckBox' in view_type or '.RadioButton' in view_type:
            if executable_obj.checkable or executable_obj.clickable:
                self.generate_check_action(executable_obj, Action.click)
        elif '.CheckedTextView' in view_type:
            if executable_obj.checkable or executable_obj.clickable:
                self.generate_check_textview_action(executable_obj, Action.click)
        elif '.SeekBar' in view_type:
            if executable_obj.clickable:
                self.generate_seekbar_action(executable_obj, Action.click)

    def add_system_actions(self):
        # add 'menu' action
        if self.activity_name == self.entry_activity_name:
            self.generate_action(Action.menu, None)
        # add 'back' action
        self.generate_action(Action.back, None)
        # add "scroll up/down" action
        if self.isScrollable:
            self.generate_action(Action.swipeDown, None)
            self.generate_action(Action.swipeUp, None)
            self.generate_action(Action.swipeLeft, None)
            self.generate_action(Action.swipeRight, None)


if __name__ == '__main__':
    print("I: start android app static analysis to detect actions.... ")
    file_path = '/Users/xuhao/PycharmProjects/vm_module-core/result/d60407b0-b3c2-11eb-a26e-acde48001122/org.asdtm.goodweather/screens/3.uix'
    from Model.State import State

    state = State(-1)
    state.activity_name = '.MainActivity'
    state.layout = ET.tostring(ET.parse(file_path).getroot(), encoding='utf-8', method='xml')
    e = EventExtractor(state, 'org.asdtm.goodweather', '.MainActivity')
    events = e.extract_actions()
    print(events)
