#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/1/8 9:39 下午
# @Author  : Wang Guoxin

from web_server import app
from flask_cors import cross_origin
from flask import request, jsonify, send_file, make_response
from orm.DatabaseModels import TableApp, TableScenario, TableARP, TableTransition, TableTask
from orm.SqlHelper import SqlHelper
from util.FileHelper import FileHelper
from sketch_module.SketchSearch import SketchSearch
import time


@app.route('/get_repo_app_list', methods=["GET"])
@cross_origin()
def get_repo_app_list():
    # arps = SqlHelper.get_entities(TableARP)
    # tasks = SqlHelper.get_entities(TableTask)
    tasks = SqlHelper.get_entities(TableTask, status='end')
    data = []
    for task in tasks:
        app = SqlHelper.get_entity(TableApp, id=task.app_id)
        data.append({
            'app_id': app.id,
            'arp_id': task.arp_id,
            'name': app.package_name,
            'package': app.package_name,
            'version': app.version
        })
    # for arp in arps:
    #     app = SqlHelper.get_entity(TableApp, id=arp.app_id)
    #     data.append({
    #         'app_id': app.id,
    #         'arp_id': arp.arp_id,
    #         'name': app.name,
    #         'package': app.package_name,
    #         'version': app.version,
    #     })
    return jsonify({
        "code": 200,
        "message": "get success",
        "data": data
    })


@app.route('/get_scenario_list', methods=["GET", "POST"])
@cross_origin()
def get_scenario_list():
    arp_id = request.args.get('arp_id')
    package_name = request.args.get('app_name')[1:-1]  # 去除双引号
    result_data = []
    rows = SqlHelper.get_entities(TableScenario, arp_id=arp_id)
    for row in rows:
        path_str = row.path
        result_data.append({
            'id': row.id,
            'arp_id': row.arp_id,
            "name": row.name,
            'desc': row.description,
            'base64str_4_pictures': get_base64str_of_pictures(arp_id, path_str.split('-'))
        })
    return jsonify({
        "code": 200,
        "message": "get success",
        "data": result_data
    })


@app.route('/sketch_search', methods=["GET", "POST"])
@cross_origin()
def sketch_search():
    try:
        arp_ids = request.form.get('arp_ids')
        arp_ids = [int(arp_id) for arp_id in arp_ids.split(',')]
        sketch_img_obj = request.files.get('sketch_img')
        sketch_img_obj.filename = 'sketch.jpg'
        user_id = request.form.get('user_id')
        FileHelper.save(FileHelper.sketch_input_dir(user_id), sketch_img_obj)
        scores = SketchSearch.compute_scores(user_id, *arp_ids)
        # time.sleep(10)
        # scores = {2: 30.333, 3: 45.224,4:323,5:3213,6:3232,7:2342,8:2121,9:122,10:121,11:112}
        result_data = []
        result_data.append(scores)
        return jsonify({
            "info": 'success',
            "data": result_data
        })
    except Exception as e:
        print(e.args)
        return jsonify({
            "info": 'error',
            "msg": e.args
        })


def get_base64str_of_pictures(arp_id, path_list):
    base64strs_of_pic = []
    for index in path_list:
        pic_path = FileHelper.screen_file(arp_id, index)
        base64strs_of_pic.append(image2base64(pic_path))
    return base64strs_of_pic


def image2base64(path):
    """
    将图片转化为二进制格式，然后再转化成base64编码
    :param path: 图片地址
    :return: base64编码
    """
    import base64
    with open(path, 'rb') as file:
        binary_data = file.read()
        encodestring = base64.b64encode(binary_data)
    return encodestring.decode('utf-8')
