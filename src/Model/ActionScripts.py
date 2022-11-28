from Model.Transition import Transition

class ActionScripts:
    def __init__(self,transition:Transition,location,event):
        self.transition=transition
        self.location=location
        self.event=event

    def get_transition(self)->Transition:
        return self.transition

    def get_location_stmt(self):
        return self.location

    def get_event_stmt(self):
        return self.event