from executor.event_extractor.Action import Action
import re
from Model.Transition import Transition
from Model.Event import Event


class ScriptConverter:

    @classmethod
    def convert2action(cls, event, action_id=None):
        action = None
        event = event.strip()
        if event == 'back':
            action = Action(action_id, Action.back, None)
        elif event.startswith('click') or event.startswith('longClick'):
            action_type, class_name, instance, bounds = \
                re.findall(r'(.*?)\(className="(.*?)",instance="(.*?)",bounds="(.*?)"\)', event)[0]
            identifier = {'className': class_name, 'instance': instance}
            if action_type == 'click':
                action_type = Action.click
            else:
                action_type = Action.longClick
            action = Action(action_id, action_type, identifier)
        elif event.startswith('edit'):
            class_name, instance, _, input_text = \
                re.findall(r'edit\(className="(.*?)",instance="(.*?)",bounds="(.*?)"\)@"(.*?)"', event)[0]
            identifier = {'className': class_name, 'instance': instance, 'input': input_text}
            action = Action(action_id, Action.editText, identifier)
        elif event.startswith('tap'):
            x, y = \
                re.findall(r'tap\(\[\((.*?),(.*?)\)]\)', event)[0]
            identifier = {'x': x, 'y': y}
            action = Action(action_id, Action.click, identifier)
        elif event.startswith('swipe'):
            action = Action(action_id, Action.swipeDown, None)
        return action

    @classmethod
    def convert2transitions(cls, jump_pairs_file, task_id=None):
        transitions = {}
        with open(jump_pairs_file, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                if len(line) == 0:
                    continue
                trans = line.split(' ')
                source_id = int(trans[0].strip())
                target_id = int(trans[1].strip())
                event = trans[2]
                action = cls.convert2action(event, len(transitions))
                transition = Transition(None, action.action_id)
                transition.set_event(Event(action.action_type, action.trigger_identify))
                transition.set_source_id(source_id)
                transition.set_target_id(target_id)
                transition.set_task_id(task_id)
                transitions[transition.get_transition_id()] = transition
        return transitions

    @classmethod
    def convert2actions(cls, jump_pairs_file):
        actions = []
        with open(jump_pairs_file, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                if len(line) == 0:
                    continue
                *_, event = line.split(' ')
                actions.append(cls.convert2action(event, len(actions)))
        return actions


if __name__ == '__main__':
    actions = ScriptConverter.convert2actions(
        '/Users/xuhao/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/2702e42ab6679d41bee105f942a07107/Message/MessageTemp/d27a621839521901125f48e2663d18df/File/jump_pairs.lst')
    print(actions)
