from web_server import app
from flask_cors import cross_origin
from flask import request, jsonify, make_response
from orm.DatabaseModels import TableResult, TableTask, TableUser, TableApp, TableARP
import os, zipfile
from flask import send_file
from orm.SqlHelper import SqlHelper
import datetime
from util.FileHelper import FileHelper


@app.route('/download_result', methods=["GET", "POST"])
@cross_origin()
def download_result():
    try:
        task_id = request.form.get('task_id')
        print("in download,task_id:", task_id)
        # 获取结果地址，将其目录下所有文件打包成一个压缩包,就存放在那个目录下
        result = SqlHelper.get_entity(TableResult, task_id=task_id)
        # 返回压缩包
        response = make_response(send_file(result.url,
                                           mimetype='application/octet-stream',  # 类型检测可以不在这里进行
                                           as_attachment=True,
                                           attachment_filename="result_" + task_id + ".zip"
                                           ))
        response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
        return response
    except Exception as E:
        return "下载失败"


@app.route('/download_arp', methods=["GET", "POST"])
@cross_origin()
def download_arp():
    try:
        task_id = request.form.get('task_id')
        print("in download,task_id:", task_id)
        # 获取结果地址，将其目录下所有文件打包成一个压缩包,就存放在那个目录下
        task_row = SqlHelper.get_entity(TableTask, id=task_id)
        arp_row = SqlHelper.get_entity(TableARP, arp_id=task_row.arp_id)
        arp_zip_file = FileHelper.arp_model_zip(arp_row.arp_id)
        # 返回压缩包
        response = make_response(send_file(arp_zip_file,
                                           mimetype='application/octet-stream',  # 类型检测可以不在这里进行
                                           as_attachment=True,
                                           attachment_filename="result_" + task_id + ".zip"
                                           ))
        response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
        return response
    except Exception as E:
        return "下载失败"


def get_time_cost(start_time, end_time):
    if start_time is not None and end_time is not None:
        start_struct_time = datetime.datetime.strptime(start_time, '%a %b %d %H:%M:%S %Y')
        end_struct_time = datetime.datetime.strptime(end_time, '%a %b %d %H:%M:%S %Y')
        return (end_struct_time - start_struct_time).seconds
    else:
        return -1


# 6.历史记录
# TODO：这里的data从后端获得
# 根据user的信息 获取 task 记录
# 后端接口：Task.Get_Task
# 跟前端对接一下表格的数据结构
@app.route('/history', methods=['post'])
@cross_origin()
def get_history():
    data = []
    front = request.get_json(silent=True)
    user_id = int(front["UserId"])
    # 获取user_id对应的所有task
    tasks = SqlHelper.get_entities(TableTask, user_id=user_id)
    for task in tasks:
        print(str(task.commit_time))
        print("task.start_time:", task.start_time, "task.end_time:", task.end_time)
        time_cost = get_time_cost(task.start_time, task.end_time)
        # 获取排队的任务数
        # task_num = SqlHelper.get_entities(TableTask, id=)
        # task对应的app
        app = SqlHelper.get_entity(TableApp, id=task.app_id)
        # arp_row = SqlHelper.get_entity(TableARP, arp_id=task.arp_id)
        # task对应的result
        result = SqlHelper.get_entity(TableResult, task_id=task.id)
        if result is None:
            instruction_coverage = None
            branch_coverage = None
            cxty_coverage = None
            line_coverage = None
            method_coverage = None
            class_coverage = None
            activity_coverage = None
        else:
            instruction_coverage = result.instruction_coverage
            branch_coverage = result.branch_coverage
            cxty_coverage = result.cxty_coverage
            line_coverage = result.line_coverage
            method_coverage = result.method_coverage
            class_coverage = result.class_coverage
            activity_coverage = result.activity_coverage

        data.append(
            {
                "performNum": task.id,  # 这个就是前端下载的时候需要给我的task_id
                "app": app.package_name,
                "algorithms": task.strategy,

                "time": task.commit_time,  # 需要从数据库获取
                "time_end": task.end_time,
                "state": task.status,
                "task_id": task.id,

                "task_queue": str(0),
                "time_cost": str(time_cost),
                "instruction_coverage": str(instruction_coverage),
                "branch_coverage": str(branch_coverage),
                "cxty_coverage": str(cxty_coverage),
                "line_coverage": str(line_coverage),
                "method_coverage": str(method_coverage),
                "class_coverage": str(class_coverage),
                "activity_coverage": str(activity_coverage),
            }, )

    return jsonify({
        "message": "history get success",
        "data": data
    })


@app.route('/result', methods=['post'])
@cross_origin()
def result():
    front = request.get_json(silent=True)
    task_id = int(front["task_id"])
    result = SqlHelper.get_entity(TableResult, task_id=task_id)
    task = SqlHelper.get_entity(TableTask, id=task_id)
    app = SqlHelper.get_entity(TableApp, id=task.app_id)
    data = [{
        'appname': app.package_name,
        'algorithm': task.strategy,
        'committime': task.commit_time,
        'endtime': task.end_time,
        'timecost': str(get_time_cost(task.start_time, task.end_time)),
        'instruction_coverage': str(result.instruction_coverage),
        'branch_coverage': str(result.branch_coverage),
        'cxty_coverage': str(result.cxty_coverage),
        'line_coverage': str(result.line_coverage),
        'method_coverage': str(result.method_coverage),
        'class_coverage': str(result.class_coverage),
        'activity_coverage': str(result.activity_coverage)
    }]
    return jsonify({
        "message": "history get success",
        "data": data
    })
