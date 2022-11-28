from Model.AppRunningPathModel import AppRunningPathModel
from util.ARPHelper import ARPHelper


class DisJointSet:
    def __init__(self, n):
        self.parent = [0] * n
        for i in range(n):
            self.parent[i] = i

    def find(self, i):
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        self.parent[self.find(i)] = self.find(j)

    def __len__(self):
        return len(self.parent)


class ModelCombination:

    def __init__(self):
        pass

    def compare_states(self, state1, state2):
        return True

    def compare_transitions(self, transition1, transition2, offset, states_set):
        s1 = states_set.find(transition1.get_source_id())
        t1 = states_set.find(transition1.get_target_id())
        s2 = states_set.find(transition2.get_source_id() + offset)
        t2 = states_set.find(transition2.get_target_id() + offset)
        if s1 != s2 or t1 != t2:
            return False

    def merge(self, arp1: AppRunningPathModel, arp2: AppRunningPathModel):
        """
        合并arp模型
        """
        # 合并states
        states1 = arp1.get_states()
        states2 = arp2.get_states()
        s_len1 = len(states1)
        s_len2 = len(states2)
        states_set = DisJointSet(s_len1 + s_len2)
        for state1 in states1.values():
            for state2 in states2.values():
                if self.compare_states(state1, state2):
                    states_set.union(state1.get_state_id(), state2.get_state_id() + s_len1)

        states_map = {}
        for i in range(s_len1 + s_len2):
            idx = states_set.find(i)
            if idx not in states_map:
                states_map[idx] = len(states_map)
        states = {}
        for idx in states_map:
            if idx < s_len1:
                states[states_map[idx]] = states1[idx]
            else:
                states[states_map[idx]] = states2[idx - s_len1]

        # 合并transitions
        transitions1 = arp1.get_transitions()
        transitions2 = arp2.get_transitions()
        t_len1 = len(transitions1)
        t_len2 = len(transitions2)
        transitions_set = DisJointSet(t_len1 + t_len2)
        for transition1 in transitions1.values():
            for transition2 in transitions2.values():
                if self.compare_transitions(transition1, transition2, s_len1, states_set):
                    transitions_set.union(transition1.get_transition_id(), transition2.get_transition_id() + t_len1)
        transitions_map = {}
        for i in range(t_len1 + t_len2):
            idx = transitions_set.find(i)
            if idx not in transitions_map:
                transitions_map[idx] = len(transitions_map)
        transitions = {}
        for idx in transitions_map:
            if idx < t_len1:
                transitions[transitions_map[idx]] = transitions1[idx]
            else:
                transitions[transitions_map[idx]] = transitions2[idx - t_len1]

        app = arp1.get_app()
        arp = ARPHelper.create_arp(app)
        arp.set_states(states)
        arp.set_transitions(transitions)
        return arp
