from comparison.StateComparison import StateComparison
import xml.etree.ElementTree as ET

attributes = ['index', 'resource-id', 'class', 'package',
              'clickable', 'scrollable', 'long-clickable', 'checkable']


class XMLBasedStateComparison(StateComparison):

    def __init__(self, arp, device):
        super().__init__(arp, device)
        self.states = self.arp.get_states()
        self.simply_layouts = {}

    def delete_system_node(self, root):
        for child in list(root):
            if child.get('package') == 'com.android.systemui' and (
                    child.get('class') == 'android.widget.LinearLayout'
                    or child.get('class') == 'android.widget.FrameLayout'):
                root.remove(child)
            else:
                self.delete_system_node(child)

    def refine_xml(self, root):
        for child in list(root):
            child.set('content-desc', 'default')
            child.set('text', 'default')
            child.set('bounds', 'default')
            child.set('checked', 'default')
            child.set('focused', 'default')
            self.refine_xml(child)

    def simplify_layout(self, layout):
        tree = ET.fromstring(layout)
        self.delete_system_node(tree)
        # self.refine_xml(tree)
        return tree

    def compare_states(self, current_state):
        layout = current_state.get_layout()
        simply_layout = self.simplify_layout(layout)
        for state_id in self.simply_layouts:
            pre_layout = self.simplify_layout(self.simply_layouts[state_id])
            if self.is_similar(simply_layout, pre_layout):
                return self.states[state_id]
        self.simply_layouts[len(self.states)] = layout
        return None

    def is_similar(self, root1, root2):
        if root1.tag != root2.tag or len(root1) != len(root2):
            return False
        if root1.tag == 'node':
            for attr in attributes:
                if root1.get(attr) != root2.get(attr):
                    return False
        for child1, child2 in zip(list(root1), list(root2)):
            if not self.is_similar(child1, child2):
                return False
        return True
