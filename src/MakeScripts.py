import os,sys
#sys.path.append('./lib/back')
from Model.Transition import Transition
from uiautomator2 import Device
from Model.Event import Event

class MakeScripts:

    def __init__(self,transition:Transition,driver:Device):
        self.el='el'
        self.device='device'
        self.driver=driver
        self.transition=transition
        self.event:Event=self.transition.get_event()

    # 简化生成定位参数的步骤
    def build_param(self,name,var):
        return '('+name+'=\''+var+'\')'

    def make_location(self,identifier,instance):
        location=self.el+'='
        if 'className' in identifier:
            location+=self.make_class_name_location(identifier)
        elif 'resourceId' in identifier:
            location+=self.make_resouce_id_location(identifier)

        if instance==None:
            if 'instance' in identifier:
                location+='['+str(identifier['instance'])+']'
        else:
            location+='['+str(instance)+']'
        return location

    def make_class_name_location(self,identifier):
        return self.device+self.build_param('className',identifier['className'])

    def make_resouce_id_location(self,identifier):
        return self.device+self.build_param('resourceId',identifier['resourceId'])
        
    def make_description_location(self,identifier):
        return self.device+self.build_param('description',identifier['description'])
    
    def make_event(self,action,condition):
        event=self.el+'.'
        if action=='click':
            event+=self.make_click_event()
        if action=='long_click':
            event+=self.make_long_click_event(condition)

        return event

    def make_click_event(self):
        return 'click()'

    def make_long_click_event(self,condition):
        if condition==None:
            return 'long_click()'
        if 'duration' not in condition:
            return 'long_click()'
        else:
            return 'long_click('+self.build_param('duration',condition['duration'])+')'


    def get_scripts(self):
        scripts=[]
        location_script=''
        identifier=self.event.get_trigger_identifier()
        action=self.event.get_trigger_action()
        condition=self.event.get_conditions()
        location_script=self.make_location(identifier,None)
        scripts.append(location_script)
        event_script=self.make_event(action,condition)
        scripts.append(event_script)
        return scripts

if __name__=='__main__':
    trans=Transition()
    identifier={}
    identifier['className']='111'
    identifier['instance']=2
    event=Event('click',identifier)
    trans.set_event(event)
    MakeScripts(trans).get_scripts()