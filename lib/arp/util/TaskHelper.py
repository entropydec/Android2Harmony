import os
from Model.Task import Task
from Model.Task import TaskStatus
from Model.Task import PersistenceType
from Model.App import App
from Model.State import State
from Model.Transition import Transition
from PIL import Image
from util.ScriptConverter import ScriptConverter
import re
from Model.Scenario import Scenario
import time
from orm.SqlHelper import SqlHelper
from orm.DatabaseModels import TableTask, TableScenario, TableApp
from util.FileHelper import FileHelper
from util.ARPPersistence import ARPPersistence
import json
from util.AppHelper import AppHelper


class TaskHelper:

    @classmethod
    def create_scenarios(cls, file_path, task_id):
        scenarios = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                if len(line) == 0:
                    continue
                scenario_name, description, path = re.findall(r'\[(.*?)] \[(.*?)] \[(.*?)]', line)[0]
                scenario = Scenario(len(scenarios), task_id, scenario_name, description, path)
                scenarios.append(scenario)
        return scenarios

    @classmethod
    def create_task(cls, user_id, file_path, persistence=False):
        app_info_file = os.path.join(file_path, 'app_info.lst')
        jump_pairs_file = os.path.join(file_path, 'jump_pairs.lst')
        scenarios_file = os.path.join(file_path, 'scenarios.lst')
        activity_file = os.path.join(file_path, 'window_info.lst')
        screen_shot_dir = os.path.join(file_path, 'temp-screen-shot')
        layout_dir = os.path.join(file_path, 'temp-gui-hierarchy')
        apk_path = None
        for filename in os.listdir(file_path):
            abs_path = os.path.join(file_path, filename)
            if os.path.isfile(abs_path) and filename.endswith('.apk'):
                apk_path = abs_path
                break
        app = AppHelper.create_app(apk_path, None, persistence)
        task = Task(None, None, None, user_id, app, False)
        task.set_commit_time(time.asctime())
        task.set_status(time.asctime())
        task.set_finished_time(time.asctime())
        task.set_end_time(time.asctime())
        task.set_status(TaskStatus.END)
        if persistence:
            task_id = SqlHelper.add_return_key(TableTask, 'id',
                                               user_id=user_id,
                                               app_id=app.get_id(),
                                               status=task.get_status(),
                                               commit_time=task.get_commit_time(),
                                               start_time=task.get_start_time(),
                                               finished_time=task.get_finished_time(),
                                               end_time=task.get_end_time())
            task.set_task_id(task_id)
        with open(app_info_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            app.set_package_name(lines[1].strip())
            app.set_version(lines[2].strip())
        states = app.get_states()
        with open(activity_file, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                state_activity = line.split(' ')
                state_id = int(state_activity[0].strip())
                activity_name = state_activity[1].strip()
                layout = ''
                with open(os.path.join(layout_dir, f"{state_id}.xml"), 'r', encoding='utf-8') as lf:
                    for layout_line in lf.readlines():
                        layout += layout_line.strip()
                picture = Image.open(os.path.join(screen_shot_dir, f'{state_id}.png'))
                states[state_id] = State(task.get_task_id(), state_id, activity_name, picture, layout)
        app.transitions = ScriptConverter.convert2transitions(jump_pairs_file, task.get_task_id())
        scenarios = TaskHelper.create_scenarios(scenarios_file, task.get_task_id())
        task.set_scenarios(scenarios)
        return task

    @classmethod
    def save(cls, task: Task):
        user_id = task.get_user_id()
        task_id = task.get_task_id()
        result_path = FileHelper.result_dir(user_id, task_id)
        arp_persistence = ARPPersistence(task.get_app(), task)
        app = task.get_app()
        # 路径不存在就创建
        FileHelper.create_dir(result_path)
        # 保存至磁盘
        task_path = os.path.join(result_path, 'task.txt')
        with open(task_path, 'w', encoding='utf-8') as f:
            f.write(f"task id: {task.get_task_id()}\n")
            f.write(f"execution strategy: {task.get_execution_strategy()}\n")
            f.write(f"apk path: {app.get_apk_path()}\n")
            f.write(f"parameters: {task.get_parameters()}\n")
            f.write(f"package name: {app.get_package_name()}\n")
            f.write(f"main_activity: {app.get_main_activity()}")
        scenarios_path = os.path.join(result_path, 'scenarios.txt')
        with open(scenarios_path, 'w', encoding='utf-8') as f:
            for scenario in task.get_scenarios():
                f.write(f"[{scenario.get_name()}] [{scenario.get_des()}] [{scenario.get_path()}]\n")
        arp_persistence.save2disk()
        # 将reuslt目录打包至上级目录
        FileHelper.zip(result_path,
                       FileHelper.result_zip_file(task.get_user_id(), task.get_task_id()))
        # 保存至数据库
        if task.persistence == PersistenceType.DATABASE_DISK:
            scenarios_info = [{'id': scenario.get_id(),
                               'task_id': scenario.get_task_id(),
                               'name': scenario.get_name(),
                               'description': scenario.get_des(),
                               'path': scenario.get_path()} for scenario in task.get_scenarios()]
            SqlHelper.add_all(TableScenario, *scenarios_info)
            arp_persistence.save2database()


if __name__ == '__main__':
    task = TaskHelper.create_task(1, '/Users/xuhao/Downloads/大厂面试八股文合集/data_for_VM/BudgetWatch', True)
    TaskHelper.save(task)
    print()
