import json
import re
from pathlib import Path
from typing import List

from sketch_module.search.model_analyze import model_analyze
from sketch_module.search.score import get_original_score
from sketch_module.search.total_score import calculate_total_score
# from sketch_module.utils.data import State, Transition
from Model.State import State
from Model.Transition import Transition

repo_w = 768
repo_h = 1280


def generate_jump_array(sketch, jump_record):
    with open(sketch, "r", encoding="utf-8") as f:
        sketch_dict = json.load(f)
    ui_num = len(sketch_dict)
    jump_array = [[{} for _ in range(ui_num)] for _ in range(ui_num)]
    with open(jump_record, "r", encoding="utf-8") as f:
        jump_list = json.load(f)
    for jump in jump_list:
        start = int(jump[0].split("_")[1])
        end = int(jump[1].split("_")[1])
        jump_array[start][end][jump[2]] = jump[3]

    return jump_array


def generate_ui_list(sketch_ui):
    result = {}
    with open(sketch_ui, "r", encoding="utf-8") as f:
        ui_list = json.load(f)
        for ui_k, ui_v in ui_list.items():
            ui_index = int(ui_k.split("_")[1])
            result[ui_index] = ui_v
    return result


def generate_model_jump_array(states: List[State], transitions: List[Transition]):
    ui_num = len(states)
    jump_array = [[{} for _ in range(ui_num)] for _ in range(ui_num)]
    for transition in transitions:
        trigger_identifier = ",".join(transition.get_event().get_trigger_identifier())
        bounds_str = re.search(r'bounds="(.*?)"', trigger_identifier)
        if bounds_str:
            component = f"TriggerButton_{transition.get_transition_id()}"
            bounds = bounds_str.groups()[0]
            coord = re.findall(r"([0-9]+)", bounds)
            coord = list(map(int, coord))
            if len(coord) != 0:
                coord = [
                    coord[0] * (repo_w / 1080),
                    coord[1] * (repo_h / 1920),
                    coord[2] * (repo_w / 1080),
                    coord[3] * (repo_h / 1920),
                ]
                jump_array[transition.get_source_id()][transition.get_target_id()][component] = list(map(int, coord))

    return jump_array


def search(states: List[State], transitions: List[Transition], ui_dir: str, model_dir: str, component: str, jump: str,
           ui: str) -> float:
    """
    获取相似分数

    :param states: 状态
    :param transitions: 跳转
    :param ui_dir: 存放草图 UI 着色图的目录，也就是草图模块输出目录
    :param model_dir: 存放模型着色图的临时目录
    :param component: 组件信息的 json 文件路径
    :param jump: 跳转信息的 json 文件路径
    :param ui: ui 信息的 json 文件路径
    :return: 相似分数
    """
    user_jump_array = generate_jump_array(component, jump)
    user_ui_count = len(user_jump_array)
    user_ui_list = generate_ui_list(ui)
    model_jump_array = generate_model_jump_array(states, transitions)
    original_score_array = get_original_score(ui_dir, user_ui_count, model_dir, states)
    user_anchor, user_anchor_score = calculate_total_score(user_jump_array,
                                                           model_jump_array,
                                                           original_score_array,
                                                           user_ui_list)
    score = model_analyze(user_anchor, user_anchor_score, user_jump_array, model_jump_array, user_ui_list)
    return score


if __name__ == '__main__':
    states = []
    for state in Path("../data/QT/temp-gui-hierarchy").glob("*.xml"):
        s = State(int(state.stem), 0, state.read_text(encoding="utf-8"), bytes())
        states.append(s)
    transitions = []
    transition_id = 0
    with open("../data/QT/jump_pairs.lst", "r", encoding="utf-8") as f:
        for line in f.readlines():
            if line:
                tokens = line.strip().split(" ")
                t = Transition(transition_id, 0, int(tokens[0]), int(tokens[1]), "".join(tokens[2:]),
                               "".join(tokens[2:]))
                transitions.append(t)
                transition_id += 1

    print(search(states,
                 transitions,
                 "../results",
                 "../model_color",
                 "../results/sketch_component.json",
                 "../results/sketch_jump.json",
                 "../results/sketch_ui_info.json"))
