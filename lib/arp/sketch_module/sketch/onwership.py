def determine_ownership(ui_dict: dict, component_dict: dict):
    sketch_dict = {}
    trigger_dict = {}

    for ui_k, ui_v in ui_dict.items():
        for com_k, com_v in component_dict.items():
            if if_in(ui_v, com_v):
                store(ui_k, com_k, com_v, sketch_dict, trigger_dict)
    return sketch_dict, trigger_dict


def if_in(ui_coord, component_coord):
    ux1, uy1, ux2, uy2 = ui_coord
    cx1, cy1, cx2, cy2 = component_coord

    if cx1 > ux1 and \
            cy1 > uy1 and \
            cx2 < ux2 and \
            cy2 < uy2:
        return True
    else:
        return False


def store(ui_k, com_k, com_v, sketch_dict, trigger_dict):
    if ui_k not in sketch_dict:
        sketch_dict[ui_k] = {}
    sketch_dict[ui_k][com_k] = com_v.copy()

    if com_k.startswith("TriggerButton"):
        if ui_k not in trigger_dict:
            trigger_dict[ui_k] = {}
        trigger_dict[ui_k][com_k] = com_v.copy()
