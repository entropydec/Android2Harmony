from pathlib import Path

from search.compare import search
from sketch.analyze import analyze
from sketch_module.utils.data import State, Transition

# if __name__ == '__main__':
#     states = []
#     for state in Path("data/QT/temp-gui-hierarchy").glob("*.xml"):
#         s = State(int(state.stem), 0, state.read_text(encoding="utf-8"), bytes())
#         states.append(s)
#     transitions = []
#     with open("data/QT/jump_pairs.lst", "r", encoding="utf-8") as f:
#         for line in f.readlines():
#             if line:
#                 tokens = line.strip().split(" ")
#                 t = Transition(0, 0, int(tokens[0]), int(tokens[1]), "".join(tokens[2:]), "")
#                 transitions.append(t)
#     p = [
#         Path("data/42.uix").read_text(encoding="utf-8"),
#         Path("data/43.uix").read_text(encoding="utf-8"),
#         Path("data/44.uix").read_text(encoding="utf-8"),
#     ]
#     results = search(states, transitions, p, {
#         (0, 1): 'click(className="android.widget.TextView",instance="2",bounds="[932,73][1080,199]")',
#         (1, 2): 'click(className="android.widget.LinearLayout",instance="3",bounds="[540,451][1080,577]")'
#     })
#     for d, path in results:
#         print(f"distance: {d}, path: {path}")


if __name__ == '__main__':
    # 加载状态和跳转，这里的状态和跳转是一个模型内的，多个模型需要运行多次以计算每个模型的匹配分数，草图模块可以只运行一次
    states = []
    for state in Path("data/QT/temp-gui-hierarchy").glob("*.xml"):
        s = State(int(state.stem), 0, state.read_text(encoding="utf-8"), bytes())
        states.append(s)
    transitions = []
    transition_id = 0
    with open("data/QT/jump_pairs.lst", "r", encoding="utf-8") as f:
        for line in f.readlines():
            if line:
                tokens = line.strip().split(" ")
                t = Transition(transition_id, 0, int(tokens[0]), int(tokens[1]), "".join(tokens[2:]),
                               "".join(tokens[2:]))
                transitions.append(t)
                transition_id += 1

    # 一些存放中间结果的目录
    sketch_output = "results"
    sketch_component = "results/sketch_component.json"
    sketch_jump = "results/sketch_jump.json"
    sketch_ui = "results/sketch_ui_info.json"

    # 草图分析模块，第一个参数是草图的路径
    analyze("data/new_skip_1.jpg",
            sketch_output,
            sketch_component,
            sketch_jump,
            sketch_ui)

    # 草图与模型的匹配分数
    print(search(states,
                 transitions,
                 sketch_output,
                 "model_color",
                 sketch_component,
                 sketch_jump,
                 sketch_ui))
