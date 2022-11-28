from util.FileHelper import FileHelper
from sketch_module.sketch.analyze import analyze
from sketch_module.search.compare import search
from util.ARPHelper import ARPHelper


class SketchSearch:

    @classmethod
    def analyze(cls, user_id):
        image = FileHelper.sketch_input_image(user_id)
        output = FileHelper.sketch_output(user_id)
        component_json = FileHelper.sketch_component_json(user_id)
        jump_json = FileHelper.sketch_jump_json(user_id)
        ui_json = FileHelper.sketch_ui_json(user_id)
        FileHelper.create_dir(output, True)
        analyze(image, output, component_json, jump_json, ui_json)

    @classmethod
    def compute_scores(cls, user_id, *arp_ids):
        cls.analyze(user_id)
        output = FileHelper.sketch_output(user_id)
        model_dir = FileHelper.sketch_model_dir(user_id)
        component_json = FileHelper.sketch_component_json(user_id)
        jump_json = FileHelper.sketch_jump_json(user_id)
        ui_json = FileHelper.sketch_ui_json(user_id)
        scores = {}
        for arp_id in arp_ids:
            FileHelper.create_dir(model_dir, True)
            arp = ARPHelper.disk2memory(arp_id)
            states = arp.get_states()
            if len(states) == 0:
                scores[arp_id] = 0
                continue
            transitions = arp.get_transitions()
            states_list = [0] * len(states)
            for state_id in states:
                states_list[state_id] = states[state_id]
            transitions_list = [0] * len(transitions)
            for transition_id in transitions:
                transitions_list[transition_id] = transitions[transition_id]
            score = search(states_list, transitions_list, output, model_dir, component_json, jump_json, ui_json)
            scores[arp_id] = score
        FileHelper.remove_dir(FileHelper.sketch_dir(user_id))
        return scores


if __name__ == '__main__':
    scores = SketchSearch.compute_scores(1, 1, 2, 3, 4, 5, 7, 8, 10, 11, 12)
    print(scores)
