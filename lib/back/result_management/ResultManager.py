import threading
from Model.Result import Result
import os, logging
from util.ARPPersistence import ARPPersistence
from util.CoverageAnalysis import CoverageAnalysis
from orm.SqlHelper import SqlHelper
from orm.DatabaseModels import TableResult, TableTask
from Model.Task import TaskStatus, PersistenceType
import time
from util.FileHelper import FileHelper
from util.ARPHelper import ARPHelper


class ResultManager(threading.Thread):
    def __init__(self):
        super().__init__()
        self.to_return = []
        self.r_lock = threading.Lock()
        self.r_sema = threading.Semaphore(0)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    def receive_completed_task(self, task):
        result = Result(task, None)
        self.r_lock.acquire()
        self.to_return.append(result)
        self.r_lock.release()
        self.r_sema.release()

    def return_result(self):
        while True:
            self.r_sema.acquire()
            result = self.to_return.pop(0)
            try:
                self.save_result(result)
                self.logger.info(f'the result-{result.get_task().get_task_id()} has been returned to client')
            except Exception as error:
                self.logger.error(f"Error:task-{result.get_task().get_task_id()}:{error}")
                task = result.get_task()
                task.set_status(TaskStatus.ERROR)
                task.set_end_time(time.asctime())
                if result.get_task().persistence == PersistenceType.DATABASE_DISK:
                    SqlHelper.update(TableTask, {'status': task.get_status(), 'end_time': task.get_end_time()},
                                     id=task.get_task_id())

    def save_result(self, result: Result):
        # 更新task状态
        result.get_task().set_status(TaskStatus.SAVING)
        if result.get_task().persistence == PersistenceType.DATABASE_DISK:
            SqlHelper.update(TableTask, {'status': result.get_task().get_status()}, id=result.get_task().get_task_id())
        # 保存arp信息
        task = result.get_task()
        app = task.get_app()
        arp = task.get_arp()
        ARPHelper.save2disk(arp)
        if result.get_task().persistence == PersistenceType.DATABASE_DISK:
            ARPHelper.save2database(arp)
        # 更新result的url
        result.set_url(FileHelper.result_zip_file(task.get_user_id(), task.get_task_id()))
        self.save2disk(result)
        self.save2db(result)
        # 更新task
        result.task.set_status(TaskStatus.END)
        result.task.set_end_time(time.asctime())
        if result.get_task().persistence == PersistenceType.DATABASE_DISK:
            SqlHelper.update(TableTask, {'status': result.task.get_status(), 'end_time': result.task.get_end_time(),
                                         'app_id': app.get_id(), 'arp_id': arp.get_arp_id()},
                             id=result.get_task().get_task_id())

    def save2disk(self, result: Result):
        task = result.get_task()
        app = task.get_app()
        # 保存task信息
        task_path = FileHelper.task_info_file(task.get_user_id(), task.get_task_id())
        FileHelper.create_dir(FileHelper.task_dir(task.get_user_id(), task.get_task_id()))
        with open(task_path, 'w', encoding='utf-8') as f:
            f.write(f"task id: {task.get_task_id()}\n")
            f.write(f"execution strategy: {task.get_execution_strategy()}\n")
            f.write(f"apk path: {app.get_apk_path()}\n")
            f.write(f"parameters: {task.get_parameters()}\n")
            f.write(f"package name: {app.get_package_name()}\n")
            f.write(f"main_activity: {app.get_main_activity()}")
        # 如果使用插桩就输出覆盖度文件
        if task.instrumentation:
            manifest_file = FileHelper.manifest_file(app.get_id())
            app_source_path = FileHelper.source_code_dir(app.get_id())
            if manifest_file is not None and app_source_path is not None and os.path.exists(
                    manifest_file) and os.path.exists(app_source_path):
                analysis = CoverageAnalysis(task.get_user_id(), app.get_id(), task.get_task_id())
                analysis.output_coverage_report(result)
        # 将reuslt目录打包至上级目录
        FileHelper.zip(FileHelper.result_dir(task.get_user_id(), task.get_task_id()),
                       FileHelper.result_zip_file(task.get_user_id(), task.get_task_id()))
        self.logger.info(f"task-{task.get_task_id()} has been executed successfully!")
        self.logger.info(
            f'the task information is saved in the path of {FileHelper.task_dir(task.get_user_id(), task.get_task_id())}.')

    def save2db(self, result: Result):
        # 保存result
        if result.get_task().persistence == PersistenceType.DATABASE_DISK:
            SqlHelper.add(TableResult, task_id=result.get_task().get_task_id(), url=result.get_url(),
                          instruction_coverage=result.get_instruction_coverage(),
                          branch_coverage=result.get_branch_coverage(),
                          cxty_coverage=result.get_cxty_coverage(),
                          line_coverage=result.get_line_coverage(),
                          method_coverage=result.get_method_coverage(),
                          class_coverage=result.get_class_coverage(),
                          activity_coverage=result.get_activity_coverage())

    def run(self):
        self.return_result()
