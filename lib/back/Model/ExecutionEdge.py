class ExecutionEdge:
    def __init__(self, e_id, action_type, trigger_identifier, next_vertex):
        self.e_id = e_id
        self.action_type = action_type
        self.trigger_identifier = trigger_identifier
        self.next_vertex = next_vertex
        self.visited = False
