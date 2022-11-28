from Model.State import State
import io
import xml.etree.ElementTree as ET
from functools import cmp_to_key


def get_bounds(bounds):
    bounds = bounds.lstrip('[').rstrip(']').split('][')
    res = []
    for bound in bounds:
        b = bound.split(',')
        res.append(int(b[0]))
        res.append(int(b[1]))
    return res


def compare_node(node1, node2):
    bounds1 = get_bounds(node1.get('bounds'))
    bounds2 = get_bounds(node2.get('bounds'))
    if bounds1[0] != bounds2[0]:
        return bounds1[0] - bounds2[0]
    if bounds1[1] != bounds2[1]:
        return bounds1[1] - bounds2[1]
    if bounds1[2] != bounds2[2]:
        return bounds1[2] - bounds2[2]
    return bounds1[3] - bounds2[3]


class StateGenerator:
    def __init__(self, arp_id, states, device, state_comparison=None):
        self.arp_id = arp_id
        self.states = states
        self.device = device
        self.comparison = state_comparison

    # 删除layout可能出现的上下的导航栏 调整节点顺序
    def refine_layout(self, layout):
        root = ET.fromstring(layout)
        children = []
        for child in list(root):
            if child.get('package') != 'com.android.systemui':
                children.append(child)
            root.remove(child)
        sorted(children, key=cmp_to_key(compare_node))
        for child in children:
            root.append(child)
        return ET.tostring(root, encoding='unicode')

    def catch_state(self):
        state = State(self.arp_id)
        state.set_package_name(self.device.info['currentPackageName'])
        state.set_picture(self.device.screenshot())
        layout = self.refine_layout(self.device.dump_hierarchy())
        state.set_layout(layout)
        state.set_activity_name(self.device.app_current()['activity'])
        same_state = self.search_same_state(state)
        if same_state is None:
            state.set_state_id(len(self.states))
            self.states[state.get_state_id()] = state
            return state
        return same_state

    # 找到探索过的相同的state,若不为None 则返回state
    def search_same_state(self, current_state):
        if self.comparison is not None:
            return self.comparison.compare_states(current_state)
        else:
            return None


if __name__ == '__main__':
    print(get_bounds('[28,641][968,1132]'))
