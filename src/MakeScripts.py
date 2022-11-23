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

    def make_location(self,identifer,instance):
        location=self.el+'='
        if 'className' in identifer:
            location+=self.make_class_name_location(identifer)
        
        if instance==None:
            if 'instance' in identifer:
                location+='['+str(identifer['instance'])+']'
        else:
            location+='['+str(instance)+']'
        return location

    def make_class_name_location(self,identifer):
        return self.device+self.build_param('className',identifer['className'])
        
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