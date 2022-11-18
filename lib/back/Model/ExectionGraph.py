from Model.App import App
from Model.ExecutionEdge import ExecutionEdge
from Model.ExecutionVertex import ExecutionVertex
from Model.State import State


class ExecutionGraph:
    def __init__(self, app: App):
        self.vertexes = {}
        self.edges = {}
        self.table = {}
        self.__build_graph(app)

    def compress_layout(self, layout):
        return "".join([line.strip() for line in layout.splitlines()])

    def __build_graph(self, app: App):
        for state in app.get_states().values():
            vertex = ExecutionVertex(state.get_state_id(), state.get_activity_name(),
                                     state.get_picture(), self.compress_layout(state.get_layout()))
            self.vertexes[state.get_state_id()] = vertex
            self.table[state.get_state_id()] = []
        for transition in app.get_transitions().values():
            edge = ExecutionEdge(transition.get_transition_id(),
                                 transition.get_event().get_trigger_action(),
                                 transition.get_event().get_trigger_identifier(),
                                 self.vertexes[transition.get_target_id()])
            self.edges[transition.get_transition_id()] = edge
            self.table[transition.get_source_id()].append(edge)

    @property
    def vertex_num(self):
        return len(self.vertexes)

    @property
    def edge_num(self):
        return len(self.edges)

    @property
    def visited_vertex_num(self):
        visited = 0
        for vertex in self.vertexes.values():
            if vertex.visited:
                visited += 1
        return visited

    @property
    def visited_edge_num(self):
        visited = 0
        for edge in self.edges.values():
            if edge.visited:
                visited += 1
        return visited

    @property
    def vertex_coverage(self):
        return self.visited_vertex_num / self.vertex_num

    @property
    def edge_coverage(self):
        return self.visited_edge_num / self.edge_num

    def similar_vertex(self, state: State):
        current_layout = self.compress_layout(state.get_layout())
        for vertex in self.vertexes.values():
            if vertex.layout == current_layout:
                return vertex
        return None

    def update_status(self, source_state, target_state, action):
        begin = self.similar_vertex(source_state)
        if begin is not None:
            begin.visited = True
            end = self.similar_vertex(target_state)
            for edge in self.table[begin.v_id]:
                if edge.action_type == action.action_type \
                        and edge.trigger_identifier == action.trigger_identify \
                        and end is edge.next_vertex:
                    edge.visited = True
                    end.visited = True
                    break

    def executable_edges(self, state: State):
        vertex = self.similar_vertex(state)
        # unvisited = []
        edges = []
        if vertex is not None:
            # for edge in self.table[vertex.v_id]:
            #     if not edge.visited:
            #         unvisited.append(edge)
            edges = self.table[vertex.v_id]
        return edges
        # return unvisited
