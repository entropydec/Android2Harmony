class UIExecutableObject:
    def __init__(self, node, instance, ancestor_executable_attributes):
        self.package_name = node.get('package')
        self.class_name = node.get('class')
        self.isListView = self.class_name == 'android.widget.ListView'

        self.clickable = self.str2bool(node.get('clickable')) or ancestor_executable_attributes['clickable']
        self.long_clickable = self.str2bool(node.get('long-clickable')) or ancestor_executable_attributes[
            'long-clickable']
        self.scrollable = self.str2bool(node.get('scrollable')) or ancestor_executable_attributes['scrollable']
        self.checkable = self.str2bool(node.get('checkable')) or ancestor_executable_attributes['checkable']

        self.text = node.get('text')
        self.resource_id = node.get('resource-id')
        self.content_desc = node.get('content-desc')
        self.index = int(node.get('index'))
        self.bounds = node.get('bounds')

        self.instance = instance

    def str2bool(self, string):
        return string == 'true'

    def has_multi_lines_text(self):
        if '\n' in self.text:
            return True
        else:
            return False

    def get_first_line_text(self):
        return self.text.split('\n')[0]
