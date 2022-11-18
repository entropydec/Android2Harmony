import json
import os
from typing import List

import cv2
import numpy as np
import torch
from PIL import Image
from torch import Tensor
from torchvision.transforms import functional as func

from sketch_module.sketch.model import resnet18
from sketch_module.sketch.onwership import determine_ownership
from sketch_module.sketch.trigger import determine_trigger
import importlib.resources
from util.FileHelper import FileHelper

names = {
    0: "Checkmark"
    , 1: "Circle"
    , 2: "Cross"
    , 3: "Down_arrow"
    , 4: "Left_arrow"
    , 5: "Line"
    , 6: "Right_arrow"
    , 7: "Solid_circle"
    , 8: "Triangle"
    , 9: "Up_arrow"
}

# 加载模型
model = resnet18()
model.change_classes(len(names))
# checkpoint = torch.load(importlib.resources.open_binary("sketch_module.sketch", "model_best.pth.tar"))
model_file = FileHelper.join("models", "model_best.pth.tar")
checkpoint = torch.load(model_file)
pretrained_params = checkpoint["state_dict"]
model.load_state_dict(pretrained_params)
model.eval()

# 边框颜色？
index_dict = {}
color_dict = {
    "Button": (0, 0, 255),
    "TriggerButton": (0, 0, 255),
    "TextView": (255, 0, 0),
    "Toolbar": (0, 125, 0),
    "EditText": (0, 125, 255),
    "CheckBox": (0, 255, 125),
    "RadioButton": (0, 0, 125),
    "ImageView": (0, 0, 0),
    "Switch": (125, 0, 125)
}


def get_contours(img: np.ndarray):
    # 转为灰度
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 转为二值图
    _, dist = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return cv2.findContours(dist, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)


def get_component_contours(img: np.ndarray):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, dist = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    return cv2.findContours(dist, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)


def recognize_sketch(img: np.ndarray, output: str):
    arrow_dict = {}
    ui_dict = {}
    component_dict = {}

    contours, hierarchy = get_contours(img)
    hierarchy = hierarchy[0]
    # hierarchy 四个分量代表 next previous first_child parent
    for index, contour in enumerate(contours):

        if cv2.contourArea(contour) < 500:
            continue

        if hierarchy[index, 2] < 0 and hierarchy[index, 3] > 0:
            # 轮廓外接矩形
            x, y, width, height = cv2.boundingRect(contour)
            cv2.rectangle(img, (x, y), (x + width, y + height), (0, 0, 255), 1)
            rect = img[y + 1:y + height - 1, x + 1: x + width - 1]
            component = get_component(rect)

            if component == "empty":
                if_arrow_img = img[y + 1:y + height - 1, x + 1:x + width - 1]
                component = if_arrow(if_arrow_img)
                if component == "DownArrow" or component == "UpArrow" or component == "LeftArrow" or component == "RightArrow":
                    store_image(component, output, rect, x, y, width, height, arrow_dict)
                    cv2.rectangle(img, (x, y), (x + width, y + height), (125, 125, 255), -1)
                elif cv2.contourArea(contour) > 20000:
                    store_image("UI", output, rect, x, y, width, height, ui_dict)
            else:
                if cv2.contourArea(contour) > 20000:
                    store_image("UI", output, rect, x, y, width, height, ui_dict)

                else:
                    store_image(component, output, rect, x, y, width, height, component_dict)
                    cv2.rectangle(img, (x, y), (x + width, y + height), color_dict[component], -1)
    # cv2.imwrite("../cut/color.jpg", img)
    return ui_dict, arrow_dict, component_dict


def store_image(component: str, output: str, img: np.ndarray, x: int, y: int, w: int, h: int, d: dict):
    if component not in index_dict:
        index_dict[component] = 0
    des = f"{component}_{index_dict[component]}"
    index_dict[component] += 1
    # if component == "UI":
    #     cv2.imwrite(os.path.join(output, f"{des}.jpg"), img)
    cv2.imwrite(os.path.join(output, f"{des}.jpg"), img)

    d[des] = [x, y, x + w, y + h]


def reshape_120(h: int, w: int):
    min_h = 120
    min_w = 120
    if h < min_h:
        w = int(min_h / h * w)
        h = min_h

    if w < min_w:
        h = int(min_w / w * h)
        w = min_w
    return h, w


def get_rect(img: np.ndarray):
    height, width, _ = img.shape
    flag = 0
    dif = 0
    if height < width:
        dif = width - height
        flag = 1
    if height > width:
        dif = height - width
        flag = -1
    dif = int(dif / 2)
    if flag == 1:
        img = cv2.copyMakeBorder(img, dif, dif, 0, 0, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    elif flag == -1:
        img = cv2.copyMakeBorder(img, 0, 0, dif, dif, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    return img


def get_component(img: np.ndarray):
    h, w, _ = img.shape
    h, w = reshape_120(h, w)

    # 放大
    img = Image.fromarray(img)
    img = img.resize((w, h), Image.ANTIALIAS)
    img = np.asarray(img.getdata(), dtype="uint8").reshape((h, w, 3))

    # 检查内部控件
    cropped = img[7:h - 7, 7:w - 7]
    contours, hierarchy = get_component_contours(cropped)
    hierarchy = hierarchy[0]

    results = []
    for index, contour in enumerate(contours):
        if hierarchy[index, 2] < 0 and hierarchy[index, 3] > 0:
            if cv2.contourArea(contour) < 160:
                continue

            x, y, width, height = cv2.boundingRect(contour)
            cv2.rectangle(cropped, (x, y), (x + width, y + height), (0, 0, 255), 1)
            rect = cropped[y + 1:y + height - 1, x + 1:x + width - 1]

            rect = get_rect(rect)

            rect = Image.fromarray(rect)
            rect = rect.resize((224, 224), Image.ANTIALIAS)
            rect_tensor = func.to_tensor(rect)
            rect_tensor = torch.unsqueeze(rect_tensor, 0)
            results.append(rect_tensor)
    return recognize_component(results)


def recognize_component(imgs: List[Tensor]):
    if len(imgs) == 0:
        return "empty"

    data = torch.cat(imgs, 0)
    output = model(data)
    _, pred = output.max(1)
    pred = pred.cpu().data.numpy()

    # Step4:Calculate the total number of each symbol

    total_num = 0
    temp = {}

    for i in range(data.size(0)):
        label = pred[i]  # int
        class_name = names[label]  # str
        if class_name not in temp:
            temp[class_name] = 0
        temp[class_name] += 1
        total_num += 1

    # Step 5:逻辑判断 控件类型
    component_type = "any"

    if temp.get("Line", 0) == 1 and total_num == 1:
        component_type = "EditText"
    elif temp.get("Cross", 0) >= 1:
        if temp.get("Circle", 0) == 1:
            component_type = "RadioButton"
        elif temp.get("Checkmark", 0) == 1:
            component_type = "CheckBox"
        else:
            component_type = "TextView"
    elif temp.get("Circle", 0) == 1:
        if temp.get("Line", 0) == 3:
            component_type = "Toolbar"
        elif temp.get("Line", 0) == 1:
            component_type = "Switch"
        else:
            component_type = "Button"
    elif temp.get("Triangle", 0) == 1:
        component_type = "ImageView"
    elif temp.get("Solid_circle", 0) == 1:
        component_type = "TriggerButton"
    elif temp.get("Down_arrow", 0) == 1:
        component_type = "DownArrow"
    elif temp.get("Up_arrow", 0) == 1:
        component_type = "UpArrow"
    elif temp.get("Left_arrow", 0) == 1:
        component_type = "LeftArrow"
    elif temp.get("Right_arrow", 0) == 1:
        component_type = "RightArrow"

    return component_type


def if_arrow(img: np.ndarray):
    imgs = []

    img = get_rect(img)
    new_image = Image.fromarray(img)
    image = new_image.resize((224, 224), Image.ANTIALIAS)  # 将其转换为要求的输入大小224*224
    t = func.to_tensor(image)  # 转为Tensor
    t = torch.unsqueeze(t, 0)  # 如果存在要求输入图像为4维的情况，使用resize函数增加一维
    imgs.append(t)

    return recognize_component(imgs)


def update_component_bounds(ui_dict, sketch_dict, jump_record):
    for ui_k, ui_v in sketch_dict.items():
        x1 = ui_dict[ui_k][0]
        y1 = ui_dict[ui_k][1]

        for com_k, com_v in ui_v.items():
            com_v[0] -= x1
            com_v[1] -= y1
            com_v[2] -= x1
            com_v[3] -= y1
    for record in jump_record:
        ui_index = record[0]
        com_index = record[2]
        record[3] = sketch_dict[ui_index][com_index]


def analyze(image: str, output: str, component_json: str, jump_json: str, ui_json: str):
    """
    草图分析

    :param image: 输入草图路径
    :param output: 输出的图片的路径
    :param component_json: 组件信息的 json 文件保存路径
    :param jump_json: 跳转信息的 json 文件保存路径
    :param ui_json: ui 信息的 json 文件保存路径
    :return:
    """
    global index_dict
    index_dict = {}
    i = cv2.imread(image)
    ui, arrow, component = recognize_sketch(i, output)
    sketch, trigger = determine_ownership(ui, component)
    jump_record = determine_trigger(ui, arrow, trigger)
    update_component_bounds(ui, sketch, jump_record)
    # save component
    with open(component_json, "w", encoding="utf-8") as f:
        json.dump(sketch, f, ensure_ascii=False, indent=2)
    # save skip
    # print(sketch)
    with open(jump_json, "w", encoding="utf-8") as f:
        json.dump(jump_record, f, ensure_ascii=False, indent=2)
    # save ui
    with open(ui_json, "w", encoding="utf-8") as f:
        json.dump(ui, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    analyze("../data/new_skip_1.jpg",
            "../results",
            "../results/sketch_component.json",
            "../results/sketch_jump.json",
            "../results/sketch_ui_info.json")
