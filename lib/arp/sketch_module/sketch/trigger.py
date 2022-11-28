def determine_trigger(ui_dict, arrow_dict, trigger_dict):
    results = []
    for a_k, a_v in arrow_dict.items():
        start, end = get_ui(a_k, a_v, ui_dict)
        button = get_button(start, a_k, a_v, trigger_dict)
        result = [start, end, button]
        if start in trigger_dict and button in trigger_dict[start]:
            result.append(trigger_dict[start][button])
        results.append(result)
    return results


def get_ui(arrow_k, arrow_v, ui_dict):
    x1, y1, x2, y2 = arrow_v
    ui_start = ""
    ui_end = ""
    start = 100000
    end = 100000

    y_mid = (y1 + y2) / 2
    x_mid = (x1 + x2) / 2

    if arrow_k.startswith("RightArrow"):
        for ui_k, ui_v in ui_dict.items():
            cur_dis_s = x1 - ui_v[2]
            if 0 < cur_dis_s < start and ui_v[1] < y_mid < ui_v[3]:
                start = cur_dis_s
                ui_start = ui_k
            cur_dis_e = ui_v[0] - x2
            if 0 < cur_dis_e < end and ui_v[1] < y_mid < ui_v[3]:
                end = cur_dis_e
                ui_end = ui_k
        return ui_start, ui_end

    if arrow_k.startswith("LeftArrow"):
        for ui_k, ui_v in ui_dict.items():
            cur_dis_s = ui_v[0] - x2
            if 0 < cur_dis_s < start and ui_v[1] < y_mid < ui_v[3]:
                start = cur_dis_s
                ui_start = ui_k
            cur_dis_e = x1 - ui_v[2]
            if 0 < cur_dis_e < end and ui_v[1] < y_mid < ui_v[3]:
                end = cur_dis_e
                ui_end = ui_k
        return ui_start, ui_end

    if arrow_k.startswith("UpArrow"):
        for ui_k, ui_v in ui_dict.items():
            cur_dis_s = ui_v[1] - y2
            if 0 < cur_dis_s < start and ui_v[0] < x_mid < ui_v[2]:
                start = cur_dis_s
                ui_start = ui_k
            cur_dis_e = y1 - ui_v[3]
            if 0 < cur_dis_e < end and ui_v[0] < x_mid < ui_v[2]:
                end = cur_dis_e
                ui_end = ui_k
        return ui_start, ui_end

    if arrow_k.startswith("DownArrow"):
        for ui_k, ui_v in ui_dict.items():
            cur_dis_s = y1 - ui_v[3]
            if 0 < cur_dis_s < start and ui_v[0] < x_mid < ui_v[2]:
                start = cur_dis_s
                ui_start = ui_k
            cur_dis_e = ui_v[1] - y2
            if 0 < cur_dis_e < end and ui_v[0] < x_mid < ui_v[2]:
                end = cur_dis_e
                ui_end = ui_k
        return ui_start, ui_end

    return ui_start, ui_end


def get_button(ui_start, arrow_k, arrow_v, trigger_dict):
    button = ""
    min_x = 100000
    min_y = 100000
    x1, y1, x2, y2 = arrow_v
    y_mid = (y1 + y2) / 2
    x_mid = (x1 + x2) / 2

    if arrow_k.startswith("RightArrow") or arrow_k.startswith("LeftArrow"):
        candidates = {}
        for t_k, t_v in trigger_dict[ui_start].items():
            y_t_mid = (t_v[1] + t_v[3]) / 2
            if (y1 - 5) < y_t_mid < (y2 + 5):
                candidates[t_k] = t_v

        for c_k, c_v in candidates.items():
            x_t_mid = (c_v[0] + c_v[2]) / 2
            x_dif = abs(x_t_mid - x_mid)
            if x_dif < min_x:
                min_x = x_dif
                button = c_k
        return button

    if arrow_k.startswith("UpArrow") or arrow_k.startswith("DownArrow"):
        candidates = {}
        for t_k, t_v in trigger_dict[ui_start].items():
            x_t_mid = (t_v[0] + t_v[2]) / 2
            if (x1 - 5) < x_t_mid < (x2 + 5):
                candidates[t_k] = t_v

        for c_k, c_v in candidates.items():
            y_t_mid = (c_v[1] + c_v[3]) / 2
            y_dif = abs(y_t_mid - y_mid)
            if y_dif < min_y:
                min_y = y_dif
                button = c_k
        return button

    return button
