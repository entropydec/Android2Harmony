from web_server import app
from flask_cors import cross_origin
from flask import request, jsonify

from orm.DatabaseModels import TableTask, TableUser, TableApp, TableScenario, TableTransition, TableARP
from web_server.common.util import used_size
from orm.SqlHelper import SqlHelper
from Model.Task import Task
from AutomaticExploringFramework import AutomaticExploringFramework as AEF
from util.FileHelper import FileHelper
from executor.Executor import ExecutionStrategy
from comparison.StateComparison import StateComparisonStrategy
from util.AppHelper import AppHelper
import json
import os
from executor.Executor import ExecutionStrategy
from Model.App import App
from executor.event_extractor.Action import Action
from util.ARPHelper import ARPHelper
from Model.AppRunningPathModel import AppRunningPathModel

af = AEF()
af.start()


# 8.提交任务
# 在完成apk和算法上传之后调用
@app.route('/commit', methods=['post'])
@cross_origin()
def commit_task():
    # 从前端获取用户名
    username = request.form.get('username')
    # 存储上传的文件在后端，并获取在后端的存储路径
    temp_id = FileHelper.generate_temp_id()
    apk_file_obj = request.files.get('app')
    apk_file_path = FileHelper.upload_apk(temp_id, apk_file_obj)
    algorithm = request.form.get('algorithm')
    script_file_obj = None
    coverage_switch = request.form.get('coverage_switch')
    source_code_obj = None
    instrumentation = False
    source_code_path = None
    if coverage_switch == '1':
        source_code_obj = request.files.get('source_code')
        instrumentation = True
        source_code_path = FileHelper.upload_source_code(temp_id, source_code_obj)
        # manifest_file = FileHelper.temp_manifest_file(temp_id)
    user = SqlHelper.get_entity(TableUser, name=username)
    # 创建app
    app = AppHelper.create_app(apk_file_path, source_code_path, True)
    arp = ARPHelper.create_arp(app, True)
    if algorithm == "1":
        time_limit = request.form.get('time')
        parameters = {'time_limit': int(time_limit)}
        task = Task(ExecutionStrategy.RANDOM, StateComparisonStrategy.STRING, parameters, user.id, arp,
                    instrumentation)
    elif algorithm == "2":
        time_limit = request.form.get('time')
        parameters = {'time_limit': int(time_limit)}
        task = Task(ExecutionStrategy.Q_LEARNING, StateComparisonStrategy.XML, parameters, user.id, arp,
                    instrumentation)
    elif algorithm == "3":
        script_file_obj = request.files.get('pyfile')
        script_path = FileHelper.upload_script(temp_id, script_file_obj)
        parameters = {'script_path': script_path}
        task = Task(ExecutionStrategy.APPIUM, StateComparisonStrategy.XML, parameters, user.id, arp, instrumentation)
    elif algorithm == "4":
        time_limit = request.form.get('time')
        parameters = {'time_limit': int(time_limit)}
        task = Task(ExecutionStrategy.MCTS, StateComparisonStrategy.XML, parameters, user.id, arp, instrumentation)
    else:
        print("wrong algorithm")
        return jsonify({"info": "fail"})

    # 添加task到数据库
    key = SqlHelper.add_return_key(TableTask, 'id',
                                   user_id=task.get_user_id(),
                                   arp_id=arp.get_arp_id(),
                                   app_id=app.get_id(),
                                   status=task.get_status(),
                                   strategy=task.get_execution_strategy(),
                                   parameters=json.dumps(task.get_parameters()),
                                   commit_time=task.get_commit_time())
    task.set_task_id(key)
    # 将temp目录中的文件移动到对应的文件夹
    # FileHelper.move_temp(temp_id, user.id, task.get_task_id(), app.get_id())
    task_path = FileHelper.task_dir(user.id, task.get_task_id())
    # 移动script
    FileHelper.move(FileHelper.temp_script_dir(temp_id), task_path)
    # 删除temp/temp_id目录
    FileHelper.remove_dir(FileHelper.temp_file_dir(temp_id))
    # 更新app信息
    # app.set_apk_path(FileHelper.get_apk_file_path(app.get_id()))
    # if source_code_obj is not None:
    #     app.set_source_code_path(FileHelper.source_code_dir(app.get_id()))
    #     # 打包源码
    #     FileHelper.zip(FileHelper.source_code_dir(app.get_id()), FileHelper.source_code_zip_file(app.get_id()))
    # SqlHelper.update(TableApp, {'apk_path': app.get_apk_path(),
    #                             'source_code_path': app.get_source_code_path()}, id=app.get_id())

    # 更新task信息
    if script_file_obj is not None:
        task.set_parameter('script_path', FileHelper.get_script_file_path(user.id, task.task_id))
    # if source_code_obj is not None:
    #     task.set_parameter('manifest_file', FileHelper.manifest_file(app.get_id()))
    #     task.set_parameter('app_source_path', FileHelper.source_code_dir(app.get_id()))
    SqlHelper.update(TableTask, {'parameters': json.dumps(task.get_parameters())}, id=task.task_id)
    # 传入Task对象，启动
    af.receive_task(task)
    # ResourceManager().commit_task(task)
    return jsonify({"info": "success"})


@app.route('/run_app', methods=['post'])
@cross_origin()
def run_app():
    app_id = int(request.form.get('app_id'))
    user_id = int(request.form.get('user_id'))
    algorithm = request.form.get('algorithm')
    coverage_switch = request.form.get('coverage_switch')
    app_record = SqlHelper.get_entity(TableApp, id=app_id)
    app = App(app_record.id, app_record.apk_path, app_record.main_activity, app_record.package_name,
              app_record.version, app_record.source_code_path, [p for p in app_record.permissions.split(',')])
    arp = ARPHelper.create_arp(app, True)
    instrumentation = app.get_source_code_path() is not None and coverage_switch == '1'
    parameters = {}
    temp_id = FileHelper.generate_temp_id()
    script_obj = None
    script_id = None
    if algorithm == '2':
        time_limit = int(request.form.get('time'))
        parameters['time_limit'] = time_limit
        task = Task(ExecutionStrategy.Q_LEARNING, StateComparisonStrategy.XML,
                    parameters, user_id, arp, instrumentation)
    elif algorithm == '3':
        script_id = int(request.form.get('script_id'))
        if script_id != -1:
            parameters['script_path'] = FileHelper.app_script_file(app_id, script_id)
        else:
            script_obj = request.files.get('pyfile')
            temp_script_path = FileHelper.upload_script(temp_id, script_obj)
            parameters['script_path'] = temp_script_path
        task = Task(ExecutionStrategy.APPIUM, StateComparisonStrategy.XML,
                    parameters, user_id, arp, instrumentation)
    elif algorithm == '1':
        time_limit = int(request.form.get('time'))
        parameters['time_limit'] = time_limit
        task = Task(ExecutionStrategy.RANDOM, StateComparisonStrategy.STRING,
                    parameters, user_id, arp, instrumentation)
    elif algorithm == "4":
        time_limit = request.form.get('time')
        parameters = {'time_limit': int(time_limit)}
        task = Task(ExecutionStrategy.MCTS, StateComparisonStrategy.XML, parameters, user_id, arp, instrumentation)
    else:
        print("wrong algorithm")
        return jsonify({"info": "fail"})
    # 添加task到数据库
    key = SqlHelper.add_return_key(TableTask, 'id',
                                   user_id=task.get_user_id(),
                                   app_id=task.get_app().get_id(),
                                   status=task.get_status(),
                                   strategy=task.get_execution_strategy(),
                                   parameters=json.dumps(task.get_parameters()),
                                   commit_time=task.get_commit_time())
    task.set_task_id(key)
    # 将temp目录中的文件移动到对应的文件夹
    FileHelper.move_temp(temp_id, user_id, task.get_task_id(), app_id)
    # 更新task信息
    if script_obj is not None:
        task.set_parameter('script_path', FileHelper.get_script_file_path(user_id, task.task_id))
        SqlHelper.update(TableTask, {'parameters': json.dumps(task.get_parameters())}, id=task.task_id)
    elif script_id is not None and script_id != -1:
        FileHelper.create_dir(FileHelper.task_script_dir(user_id, task.get_task_id()))
        # 移动app中的脚本到task中
        FileHelper.copy(FileHelper.app_script_file(app_id, script_id),
                        FileHelper.task_script_dir(user_id, task.get_task_id()))

    af.receive_task(task)
    return jsonify({"info": "success"})


@app.route('/get_scenario_testcase', methods=["GET"])
@cross_origin()
def get_scenario_testcase():
    arp_id = request.args.get('arp_id')
    user_id = request.args.get('user_id')
    scenario_id = request.args.get('scenario_id')
    print(arp_id, scenario_id)
    row = SqlHelper.get_entity(TableScenario, id=scenario_id, arp_id=arp_id)
    path_nodes = row.path.split('-')
    path_nodes = [int(node) for node in path_nodes]
    transitions = SqlHelper.get_entities(TableTransition, arp_id=arp_id)
    result_actions = []
    ids = []

    # 寻找初始source 节点，在transitions中的下标
    source_id = path_nodes[0]
    start_index = 0
    for i, transition in enumerate(transitions):
        if transition.source_id == source_id:
            start_index = i
            break

    # 回溯, 寻找从0开始，到初始节点的路径
    index = start_index - 1
    while index >= 0:
        transition = transitions[index]
        if transition.target_id == source_id:
            result_actions.insert(0, Action(None, transitions[index].trigger_action,
                                            json.loads(transitions[index].trigger_identifier)))
            ids.insert(0, transition.target_id)
            source_id = transition.source_id
            if source_id == 0:
                ids.insert(0, 0)
                break
        index -= 1
    for i, actions in enumerate(result_actions):
        actions.action_id = i

    # 从初始节点，到最终节点的路径
    index = start_index - 1
    source_index = 0
    target_index = 1
    while index < len(transitions):
        transition = transitions[index]
        if transition.source_id == path_nodes[source_index] \
                and transition.target_id == path_nodes[target_index]:
            result_actions.append(Action(len(result_actions), transitions[index].trigger_action,
                                         json.loads(transitions[index].trigger_identifier)))
            ids.append(transition.target_id)
            source_index += 1
            target_index += 1
            if target_index >= len(path_nodes):
                break
        index += 1

    print(ids)
    for path in result_actions:
        print(path)

    arp_row = SqlHelper.get_entity(TableARP, arp_id=arp_id)
    app_row = SqlHelper.get_entity(TableApp, id=arp_row.app_id)
    app = App(app_row.id, app_row.apk_path, app_row.main_activity, app_row.package_name,
              app_row.version, app_row.source_code_path, [p for p in app_row.permissions.split(',')])
    # arp = AppRunningPathModel(arp_row.arp_id, app, arp_row.create_time, arp_row.update_time)
    arp = ARPHelper.create_arp(app, True)
    parameters = {'actions': result_actions}
    instrumentation = False
    task = Task(ExecutionStrategy.SCRIPT_SEQUENCE, StateComparisonStrategy.STRING,
                parameters, user_id, arp, instrumentation)
    task.set_installed(True)
    # 添加task到数据库
    key = SqlHelper.add_return_key(TableTask, 'id',
                                   user_id=task.get_user_id(),
                                   app_id=task.get_app().get_id(),
                                   status=task.get_status(),
                                   strategy=task.get_execution_strategy(),
                                   # parameters=json.dumps(task.get_parameters()),
                                   commit_time=task.get_commit_time())
    task.set_task_id(key)
    af.receive_task(task)
    return jsonify({
        "code": 200,
        "message": "success",
    })


# 10.删除历史
@app.route('/delete', methods=['post'])
@cross_origin()
def delete_result():
    data = request.get_json(silent=True)
    task_id = data["taskid"]
    print("in delete result, task_id:", task_id)
    SqlHelper.delete(TableTask, id=task_id)
