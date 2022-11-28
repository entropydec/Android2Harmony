class ExecutionVertex:
    def __init__(self, v_id, activity_name, screenshot, layout):
        self.v_id = v_id
        self.activity_name = activity_name
        self.screenshot = screenshot
        self.layout = layout
        self.visited = False
