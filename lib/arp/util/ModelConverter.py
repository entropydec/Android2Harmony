from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import ElementTree
import re


class ModelConverter:
    def __init__(self, app):
        self.app = app

    def convert2running_path_xml(self):
        application = Element('application')
        package = SubElement(application, 'package')
        package.text = self.app.get_package_name()
        main_activity = SubElement(application, 'mainActivity')
        main_activity.text = self.app.get_main_activity()
        version = SubElement(application, 'version')
        version.text = self.app.get_version()
        # permissions = SubElement(application, 'permissions')
        # for permission in self.app.get_permissions():
        #     permission_title = SubElement(permissions, 'permission')
        #     permission_title.text = permission
        transitions = self.app.get_transitions()
        records = SubElement(application, 'records')
        for transition in transitions.values():
            record = SubElement(records, 'record')
            trigger_action = transition.get_event().get_trigger_action()
            action = SubElement(record, 'action')
            condition = None
            if '(' in trigger_action and ')' in trigger_action:
                action_type, attribute = re.findall(r"(.*?)[(](.*?)[)]", trigger_action)[0]
                action.text = action_type
                condition = SubElement(record, 'condition')
                if action_type == 'swipe':
                    direction_title = SubElement(condition, 'direction')
                    direction_title.text = attribute
                else:
                    orientation = SubElement(condition, 'orientation')
                    orientation.text = attribute
            else:
                action.text = transition.get_event().get_trigger_action()
            identifier = transition.get_event().get_trigger_identifier()
            if identifier is not None and len(identifier) > 0:
                if condition is None:
                    condition = SubElement(record, 'condition')
                for item in identifier.items():
                    title = SubElement(condition, item[0])
                    title.text = str(item[1])
        return ElementTree(application)

    def pretty_xml(self, element, indent, newline, level=0):  # elemnt???????????????Elment????????????indent???????????????newline????????????
        if element:  # ??????element??????????????????
            if element.text == None or element.text.isspace():  # ??????element???text????????????
                element.text = newline + indent * (level + 1)
            else:
                element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
                # else:  # ????????????????????????????????????Element???text??????????????????
            # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
        temp = list(element)  # ???elemnt??????list
        for subelement in temp:
            if temp.index(subelement) < (len(temp) - 1):  # ????????????list???????????????????????????????????????????????????????????????????????????????????????
                subelement.tail = newline + indent * (level + 1)
            else:  # ?????????list???????????????????????? ????????????????????????????????????????????????????????????
                subelement.tail = newline + indent * level
            self.pretty_xml(subelement, indent, newline, level=level + 1)  # ??????????????????????????????

    def dump_xml(self, file_path=None):
        tree = self.convert2running_path_xml()
        root = tree.getroot()
        self.pretty_xml(root, '\t', '\n')
        if file_path is not None:
            tree.write(file_path, encoding='utf-8')
        return tree


if __name__ == '__main__':
    from util.AppHelper import AppHelper

    app = AppHelper.disk2memory(
        '/Users/xuhao/SeverProjects/online-android-vm-execution/vm_execution-back/storage/users/None/12/result')
    converter = ModelConverter(app)
    converter.dump_xml(
        '/Users/xuhao/SeverProjects/online-android-vm-execution/vm_execution-back/storage/users/None/12/result/running_path.xml')
