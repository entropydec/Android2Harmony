import os,sys
sys.path.append('./lib/back')
from Model.Transition import Transition
from Model.Event import Event

class MakeScripts:

    def __init__(self,transition:Transition):
        self.el='el'
        self.device='device'
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
        
    def make_event(self):
        pass

    def get_scripts(self):
        scripts=[]
        location_script=''
        identifier=self.event.get_trigger_identifier()
        location_script=self.make_location(identifier,None)

if __name__=='__main__':
    trans=Transition()
    identifier={}
    identifier['className']='111'
    identifier['instance']=2
    event=Event('click',identifier)
    trans.set_event(event)
    MakeScripts(trans).get_scripts()