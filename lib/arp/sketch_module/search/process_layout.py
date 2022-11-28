import os.path
import xml.dom.minidom
import io

import cv2
import numpy as np

repo_w = 768
repo_h = 1280


def generate_color_image(layouts, output):
    for state_id, layout in layouts:
        list_info = dfs_parse_xml(layout)
        img = np.ones((repo_h, repo_w), dtype=np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        img[:, :, 0] = 255
        img[:, :, 1] = 255
        img[:, :, 2] = 255
        getWidgetAttri(list_info, img, False)
        cv2.imwrite(os.path.join(output, f"{state_id}.jpg"), img)


def dfs_parse_xml(path):  # 读取UI的xml文件
    list = []
    with io.StringIO(path) as f:
        dom = xml.dom.minidom.parse(f)
    root = dom.documentElement
    getItemNode(root, list)
    return list


def getItemNode(node, list):  # 递归读取并处理xml所有节点
    flag = node.hasChildNodes()
    if (flag):  # 有子节点才处理节点的属性信息
        for child in node.childNodes:
            if child.nodeType == 1:  # 是否是元素节点
                dictAttr = {}
                for key in child.attributes.keys():  # child.attrbutes.keys()查看所有属性，返回一个列表
                    attr = child.attributes[key]  # 返回属性地址
                    dictAttr[attr.name] = attr.value  # attr.name为属性名  attr.value为属性值
                list.append({child.nodeName: dictAttr})
                getItemNode(child, list)


def getWidgetAttri(list, im, isStandardSize):  # 读取出class属性并判断是否需要画框
    for dict in list:
        # print(dict['node'])
        attri_dict = dict['node']  # 每个UI的每个控件信息
        # print(attri_dict['class'])
        s = attri_dict['class'].lower()
        clickable = attri_dict["clickable"]
        long_clickable = attri_dict["long-clickable"]
        if_layout = False
        if "layout" in s or "listview" in s:
            if_layout = True
        # 认为只要是可点击的都视作button
        if "button" in s or "checkedtextview" in s:
            left, right = process_bounds(attri_dict['bounds'])
            # print(left, right)
            draw_color("Button", left, right, im, isStandardSize)
        elif (
                clickable == "true" or long_clickable == "true") and "textview" in s and if_layout == False:  # 如果是可点击的textview，视作button，因为Button继承自textview
            left, right = process_bounds(attri_dict['bounds'])
            # print(left, right)
            draw_color("Button", left, right, im, isStandardSize)
        elif "textview" in s:
            left, right = process_bounds(attri_dict['bounds'])
            # print(left, right)
            draw_color("TextView", left, right, im, isStandardSize)
        elif "imageview" in s:
            left, right = process_bounds(attri_dict['bounds'])
            # print(left, right)
            draw_color("ImageView", left, right, im, isStandardSize)
        elif "edittext" in s:
            left, right = process_bounds(attri_dict['bounds'])
            # print(left, right)
            draw_color("EditText", left, right, im, isStandardSize)
        elif "switch" in s:
            left, right = process_bounds(attri_dict['bounds'])
            # print(left, right)
            draw_color("Switch", left, right, im, isStandardSize)
        elif "radiobutton" in s:
            left, right = process_bounds(attri_dict['bounds'])
            # print(left, right)
            draw_color("RadioButton", left, right, im, isStandardSize)
        elif "checkbox" in s:
            left, right = process_bounds(attri_dict['bounds'])
            # print(left, right)
            draw_color("CheckBox", left, right, im, isStandardSize)
        elif "toolbar" in s:
            left, right = process_bounds(attri_dict['bounds'])
            # print(left, right)
            draw_color("ToolBar", left, right, im, isStandardSize)


def process_bounds(bound):  # 分析得到需要绘制的控件边界字符串
    each_bound = bound.split("][")
    for each in each_bound:
        if "[" in each:
            left = each[1:]
        elif "]" in each:
            right = each[0:-1]
    return left, right


def draw_color(Widget_type, left, right, im, isStandardSize):  # 根据控件类型在相应区域内绘制相应颜色矩形
    left_bound_x = int(left.split(",")[0])
    left_bound_y = int(left.split(",")[1])
    right_bound_x = int(right.split(",")[0])
    right_bound_y = int(right.split(",")[1])
    if isStandardSize == False:  # 不是标准的768*1280 要同比变化绘制
        left_bound_x = int((left_bound_x * repo_w) / 1080)
        left_bound_y = int((left_bound_y * repo_h) / 1920)
        right_bound_x = int((right_bound_x * repo_w) / 1080)
        right_bound_y = int((right_bound_y * repo_h) / 1920)

    # print(left_bound_x,left_bound_y,right_bound_x,right_bound_y)

    # 用cv2根据左上角与右下角绘制颜色块
    #################
    if Widget_type == "Button":
        # print("This is Button!")
        # print(left_bound_x,left_bound_y,right_bound_x,right_bound_y)
        cv2.rectangle(im, (left_bound_x, left_bound_y), (right_bound_x, right_bound_y), (0, 0, 255), -1)
    elif Widget_type == "TextView":
        # print("This is TextView!")
        # print(left_bound_x, left_bound_y, right_bound_x, right_bound_y)
        cv2.rectangle(im, (left_bound_x, left_bound_y), (right_bound_x, right_bound_y), (255, 0, 0), -1)
    elif Widget_type == "Toolbar":
        cv2.rectangle(im, (left_bound_x, left_bound_y), (right_bound_x, right_bound_y), (0, 125, 0), -1)
    elif Widget_type == "EditText":
        cv2.rectangle(im, (left_bound_x, left_bound_y), (right_bound_x, right_bound_y), (0, 125, 255), -1)
    elif Widget_type == "CheckBox":
        cv2.rectangle(im, (left_bound_x, left_bound_y), (right_bound_x, right_bound_y), (0, 255, 125), -1)
    elif Widget_type == "RadioButton":
        cv2.rectangle(im, (left_bound_x, left_bound_y), (right_bound_x, right_bound_y), (0, 0, 125), -1)
    elif Widget_type == "ImageView":
        # print("This is ImageView!")
        # print(left_bound_x, left_bound_y, right_bound_x, right_bound_y)
        cv2.rectangle(im, (left_bound_x, left_bound_y), (right_bound_x, right_bound_y), (0, 0, 0), -1)
    elif Widget_type == "Switch":
        cv2.rectangle(im, (left_bound_x, left_bound_y), (right_bound_x, right_bound_y), (125, 0, 125), -1)
    # elif Widget_type=="List":
    #     cv2.rectangle(im, (left_bound_x, left_bound_y), (right_bound_x, right_bound_y), (125, 125, 255), -1)
