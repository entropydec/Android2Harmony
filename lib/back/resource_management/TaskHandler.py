from monitor.AndroidEventMonitor import AndroidEventMonitor
from uiautomator2 import Device
from util.Commander import Commander
import subprocess
import os
import time
import sys
# import signal
from executor.Executor import Executor
from executor.Executor import ExecutionStrategy
import threading
from orm.SqlHelper import SqlHelper
from orm.DatabaseModels import TableTask, TableApp
from Model.Task import TaskStatus, Task, PersistenceType
from util.FileHelper import FileHelper
import uiautomator2 as u2
import logging
from util.AppHelper import AppHelper


# 处理task任务 启动一个线程 让executor和monitor去执行task
class TaskHandler(threading.Thread):
    def __init__(self, task: Task, device: Device, resource_manager, result_manager, container):
        super().__init__()
        self.task = task
        self.arp = task.get_arp()
        self.app = task.get_app()
        self.device = device
        self.resource_manager = resource_manager
        self.result_manager = result_manager
        self.container = container
        self.executor = self.__pre_run()
        self.logging = logging.getLogger()
        self.logging.setLevel(logging.INFO)

    """
    更新app的信息
    """

    def __update_app_info(self):
        app_list = self.device.app_list()
        if self.app.get_apk_path() is not None:
            if len(self.app.get_permissions()) == 0:
                self.app.permissions = AppHelper.permissions(self.app.get_apk_path())
            if self.app.get_version() is None:
                self.app.set_version(AppHelper.version(self.app.get_apk_path()))
            if self.app.get_package_name() is None:
                self.app.set_package_name(AppHelper.package(self.app.get_apk_path()))
            if self.app.get_main_activity() is None:
                self.app.set_main_activity(AppHelper.main_activity(self.app.get_apk_path()))

        if self.app.package_name in app_list:
            app_info = self.device.app_info(self.app.get_package_name())
            if app_info['versionName'] != self.app.get_version() or \
                    app_info['mainActivity'] != self.app.get_main_activity():
                self.app.set_version(app_info['versionName'])
                self.app.main_activity = app_info['mainActivity']
                # 更新数据库
                if self.task.persistence == PersistenceType.DATABASE_DISK:
                    SqlHelper.update(TableApp,
                                     {'version': self.app.get_version(),
                                      'main_activity': self.app.get_main_activity()},
                                     id=self.app.get_id())
        else:
            raise Exception(f'{self.task.get_app().package_name} is not installed!')

    """
    给app授权
    """

    def __grant_permissions(self):
        for permission in self.app.get_permissions():
            self.device.shell(['pm', 'grant', '--user', '0', self.app.get_package_name(), permission])

    """
    启动线程前 创建executor和monitor
    :return executor 
    """

    def __pre_run(self) -> Executor:
        # 获取注册好的state comparsion和executor的class
        state_comparison_class = self.container.get_state_comparison(self.task.get_state_comparison_strategy())
        execution_strategy_class = self.container.get_execution_strategy(self.task.get_execution_strategy())
        state_comparison = None
        executor = None
        # 创建对应的executor和monitor
        if state_comparison_class is not None:
            state_comparison = state_comparison_class(arp=self.arp, device=self.device)
        monitor = AndroidEventMonitor(self.arp, self.device, state_comparison)
        if execution_strategy_class is not None:
            executor = execution_strategy_class(arp=self.arp, device=self.device, monitor=monitor,
                                                parameters=self.task.get_parameters())
        if executor is not None:
            return executor
        else:
            raise Exception('No matching strategy!')

    def __code_coverage_detection(self):
        coverage_path = FileHelper.coverage_output_dir(self.task.get_user_id(), self.task.get_task_id())
        log_path = FileHelper.log_dir(self.task.get_user_id(), self.task.get_task_id())
        FileHelper.create_dir(coverage_path)
        FileHelper.create_dir(log_path)
        coverage_log_file = FileHelper.coverage_log_file(self.task.get_user_id(), self.task.get_task_id())
        cmd = Commander.dump_coverage(coverage_path, self.device, self.app.package_name, coverage_log_file)
        dump_coverage_process = subprocess.Popen(cmd, shell=True, universal_newlines=True,
                                                 stdout=subprocess.PIPE)
        return dump_coverage_process

    def __dump_crash_log(self):
        log_path = FileHelper.log_dir(self.task.get_user_id(), self.task.get_task_id())
        FileHelper.create_dir(log_path)
        crash_log_file = FileHelper.crash_log_file(self.task.get_user_id(), self.task.get_task_id())
        serial_num = self.device.serial
        clear_cmd = Commander.clear_crash_log(serial_num)
        dump_cmd = Commander.dump_crash_log(serial_num, crash_log_file)
        cmd = Commander.merge(clear_cmd, dump_cmd)
        # 清除日志缓存 并 dump日志到指定目录
        dump_crash_log_process = subprocess.Popen(cmd, shell=True, universal_newlines=True,
                                                  stdout=subprocess.PIPE)
        return dump_crash_log_process

    # 杀死进程及其所有子进程
    def __kill_process(self, process):
        if sys.platform.startswith('win'):
            os.system(f"taskkill /t /f /pid {process.pid}")
        # elif sys.platform in ['linux', 'darwin']:
        #     os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        process.kill()

    # 杀死指定的所有进程
    def __kill_processes(self, *processes):
        for process in processes:
            if process is not None:
                self.__kill_process(process)

    def __install_apk(self):
        if self.app.get_apk_path() is not None and not self.task.is_installed():
            system_apps = self.device.app_list('-s')
            # 不是系统应用就安装
            if self.app.package_name not in system_apps:
                self.device.app_install(self.app.get_apk_path())

    def __uninstall_apk(self):
        if self.app.get_apk_path() is not None and not self.task.is_installed():
            system_apps = self.device.app_list('-s')
            # 不是系统应用就卸载
            if self.app.package_name not in system_apps:
                self.device.app_uninstall(self.app.get_package_name())

    def __launch_app(self):
        self.device.app_stop(self.app.package_name)
        self.device.press('home')
        self.device.app_start(self.app.package_name, self.app.main_activity, use_monkey=True)

    # 处理弹出的对话框
    def __handle_dialog_box(self):
        # 启动应用
        self.__launch_app()
        time.sleep(5)
        # 如果出现弹出的对话框 点击ALLOW
        allow_button = self.device(resourceId="com.android.packageinstaller:id/permission_allow_button")
        while allow_button.exists:
            allow_button.click()
            time.sleep(2)
            allow_button = self.device(resourceId="com.android.packageinstaller:id/permission_allow_button")

    def __stop_app(self):
        self.device.app_stop(self.app.package_name)
        self.device.press('home')

    def __connect_device(self):
        try:
            self.device = u2.connect_usb(self.device.serial)
        except Exception as e:
            print(e)

    def __release_resource(self):
        self.resource_manager.recycle(self.device)

    def run(self):
        dump_coverage_process = None
        dump_crash_log_process = None
        try:
            # 更新task状态
            self.task.set_status(TaskStatus.RUNNING)
            self.task.set_start_time(time.asctime())
            if self.task.persistence == PersistenceType.DATABASE_DISK:
                SqlHelper.update(TableTask,
                                 {'status': self.task.get_status(), 'start_time': self.task.get_start_time()},
                                 id=self.task.get_task_id())
            # 如果提供apk就安装
            self.__uninstall_apk()
            self.__install_apk()
            # 更新app信息
            self.__update_app_info()
            # 处理弹出的对话框 常见于第一次安装app之后需要授予权限
            # self.__handle_dialog_box()
            # 给权限
            self.__grant_permissions()
            # 启动app
            self.__launch_app()
            # 启动代码覆盖度检测
            if self.task.instrumentation:
                dump_coverage_process = self.__code_coverage_detection()
            # 启动崩溃日志获取
            dump_crash_log_process = self.__dump_crash_log()
            time.sleep(5)
            # 执行Executor
            self.executor.execute()
            # 更新task状态
            self.task.set_status(TaskStatus.FINISHED)
            self.task.set_finished_time(time.asctime())
            if self.task.persistence == PersistenceType.DATABASE_DISK:
                SqlHelper.update(TableTask,
                                 {'status': self.task.get_status(), 'finished_time': self.task.get_finished_time()},
                                 id=self.task.get_task_id())
            # 提交任务给result manager
            self.result_manager.receive_completed_task(self.task)
            self.logging.info('end!!')
        except Exception as e:
            self.logging.error(f"task-{self.task.get_task_id()}:{e}")
            self.task.set_status(TaskStatus.ERROR)
            self.task.set_end_time(time.asctime())
            if self.task.persistence == PersistenceType.DATABASE_DISK:
                SqlHelper.update(TableTask, {'status': self.task.get_status(), 'end_time': self.task.get_end_time()},
                                 id=self.task.get_task_id())
            raise e
        finally:
            try:
                # 杀死覆盖率收集进程,停止dump崩溃日志
                self.__kill_processes(dump_coverage_process, dump_crash_log_process)
                # 终止应用
                self.__stop_app()
                # 如果安装了apk就卸载
                self.__uninstall_apk()
            except Exception as e:
                self.logging.error(f"Error:task-{self.task.get_task_id()}:{e}")
            finally:
                # 执行结束释放资源
                self.__release_resource()
