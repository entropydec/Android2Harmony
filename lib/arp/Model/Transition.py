'''

迁移类，与数据库transition表的对应关系：
appId->app_id
transitionId->transition_id
sourceId->source_id
targetId->target_id
triggerAction->trigger_action
triggerIdentifier->trigger_identifier
condition->conditions

author zhouxinyu

'''

from Model.Event import Event


class Transition:

    def __init__(self, arp_id=-1, id=-1):
        self.transition_id = id
        self.arp_id = arp_id
        self.source_id = -1
        self.target_id = -1
        self.event = None

    def set_arp_id(self, arp_id):
        self.arp_id = arp_id

    def set_transition_id(self, id):
        self.transition_id = id

    def set_source_id(self, id):
        self.source_id = id

    def set_target_id(self, id):
        self.target_id = id

    def set_event(self, eve):
        self.event = eve

    def get_transition_id(self):
        return self.transition_id

    def get_source_id(self):
        return self.source_id

    def get_target_id(self):
        return self.target_id

    def get_event(self):
        return self.event

    def get_arp_id(self):
        return self.arp_id

    def __str__(self):
        return "[transition_id:" + str(self.transition_id) + " task_id:" + str(self.arp_id) + " source->target:" + str(
            self.source_id) + "->" + str(self.target_id) + " trigger_action:" + str(
            self.event.get_trigger_action()) + " trigger_identifier:" + str(
            self.event.get_trigger_identifier()) + " conditions:" + str(self.event.get_conditions()) + "]"
