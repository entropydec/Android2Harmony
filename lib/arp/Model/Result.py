class Result:

    def __init__(self, task, url):
        self.task = task
        self.url = url
        self.coverage = {'instruction_coverage': None,
                         'branch_coverage': None,
                         'cxty_coverage': None,
                         'line_coverage': None,
                         'method_coverage': None,
                         'class_coverage': None,
                         'activity_coverage': None}

    def get_task(self):
        return self.task

    def get_url(self):
        return self.url

    def set_url(self, url):
        self.url = url

    def set_instruction_coverage(self, instruction_coverage):
        self.coverage['instruction_coverage'] = instruction_coverage

    def set_branch_coverage(self, branch_coverage):
        self.coverage['branch_coverage'] = branch_coverage

    def set_cxty_coverage(self, cxty_coverage):
        self.coverage['cxty_coverage'] = cxty_coverage

    def set_line_coverage(self, line_coverage):
        self.coverage['line_coverage'] = line_coverage

    def set_method_coverage(self, method_coverage):
        self.coverage['method_coverage'] = method_coverage

    def set_class_coverage(self, class_coverage):
        self.coverage['class_coverage'] = class_coverage

    def set_activity_coverage(self, activity_coverage):
        self.coverage['activity_coverage'] = activity_coverage

    def get_instruction_coverage(self):
        return self.coverage['instruction_coverage']

    def get_branch_coverage(self):
        return self.coverage['branch_coverage']

    def get_cxty_coverage(self):
        return self.coverage['cxty_coverage']

    def get_line_coverage(self):
        return self.coverage['line_coverage']

    def get_method_coverage(self):
        return self.coverage['method_coverage']

    def get_class_coverage(self):
        return self.coverage['class_coverage']

    def get_activity_coverage(self):
        return self.coverage['activity_coverage']
