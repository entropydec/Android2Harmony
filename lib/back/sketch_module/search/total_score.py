import pprint

T_max = 10
repo_w = 768
repo_h = 1280


def calculate_total_score(user_jump_array, model_jump_array, original_score_array, sketch_ui):
    anchor_list = []
    anchor_score = []

    user_has_jump = [any(user_jump_array[i]) for i in range(len(user_jump_array))]
    model_has_jump = [any(model_jump_array[i]) for i in range(len(model_jump_array))]

    # print(user_has_jump)
    # print(model_has_jump)

    for i in range(len(user_jump_array)):
        score = {}
        if not user_has_jump[i]:
            for j in range(len(model_jump_array)):
                score[j] = float(original_score_array[i][j])
        else:
            for j in range(len(model_jump_array)):
                if not model_has_jump[j]:
                    score[j] = float(original_score_array[i][j])
                else:
                    score[j] = calculate_score(user_jump_array, i, model_jump_array, j, original_score_array, sketch_ui,
                                               user_has_jump, model_has_jump, 0)
        score = sorted(score.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        # pprint.pprint(score)
        for index, value in score:
            if index not in anchor_list:
                anchor_list.append(index)
                anchor_score.append(format(value, ".4f"))
                break

    return anchor_list, anchor_score


def calculate_score(user_jump_array, i, model_jump_array, j, original_score_array, sketch_ui, user_has_jump,
                    model_has_jump, t):
    if not user_has_jump[i] or not model_has_jump[j] or t >= T_max:
        return float(original_score_array[i][j])

    next_score = 0
    for p in range(len(user_jump_array)):
        if len(user_jump_array[i][p]) != 0:
            count = {}
            for q in range(len(model_jump_array)):
                if len(model_jump_array[j][q]) != 0:
                    component_num = calculate_component(user_jump_array, i, p, model_jump_array, j, q, sketch_ui)
                    count[q] = component_num

            count_list = sorted(count.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
            index = count_list[0][0]
            weight = 0.5 * count_list[0][1]
            next_score += weight * calculate_score(user_jump_array, p, model_jump_array, index, original_score_array,
                                                   sketch_ui, user_has_jump, model_has_jump, t + 1)
    score = float(original_score_array[i][j]) + next_score
    return score


def calculate_component(user_jump_array, i, p, model_jump_array, j, q, sketch_ui):
    user_jump = user_jump_array[i][p]
    model_jump = model_jump_array[j][q]
    count = 0
    for user_k, user_v in user_jump.items():
        for model_k, model_v in model_jump.items():
            if match(user_v, model_v, sketch_ui, i):
                count += 1
                break
    return count


def match(bounds1, bounds2, sketch_ui, i):
    x1 = bounds2[0]
    y1 = bounds2[1]
    x2 = bounds2[2]
    y2 = bounds2[3]

    ui_bounds = sketch_ui[i]
    # print(ui_bounds)
    width = ui_bounds[2] - ui_bounds[0]
    height = ui_bounds[3] - ui_bounds[1]

    dif_x = repo_w / 10
    dif_y = repo_h / 10

    x3 = (bounds1[0] * repo_w) / width - dif_x
    y3 = (bounds1[1] * repo_h) / height - dif_y
    x4 = (bounds1[2] * repo_w) / width + dif_x
    y4 = (bounds1[3] * repo_h) / height + dif_y

    return x1 >= x3 and x2 <= x4 and y1 >= y3 and y2 <= y4
