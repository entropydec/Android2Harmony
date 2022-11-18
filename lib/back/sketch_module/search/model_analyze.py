from sketch_module.search.total_score import calculate_component


def model_analyze(user_anchor, user_anchor_score, user_jump_array, model_jump_array, sketch_ui):
    user_jump_num = 0
    for i in range(len(user_jump_array)):
        for j in range(len(user_jump_array)):
            if len(user_jump_array[i][j]) != 0:
                user_jump_num += 1

    score_base = 100 / user_jump_num
    total_score = 0
    for i in range(len(user_jump_array)):
        for j in range(len(user_jump_array)):
            if len(user_jump_array[i][j]) != 0:
                trigger_num = len(user_jump_array[i][j])
                model_i = user_anchor[i]
                model_j = user_anchor[j]
                component_num = calculate_component(user_jump_array, i, j, model_jump_array, model_i, model_j,
                                                    sketch_ui)
                # print(f"ui {i}-{j} model {model_i}-{model_j}, match component {component_num}")
                weight = 0.5 * float(user_anchor_score[i]) + 0.5 * float(
                    user_anchor_score[j]) * component_num / trigger_num
                total_score += weight * score_base
    return total_score
