import subprocess
from util.Commander import Commander
import uiautomator2 as  u2
import threading
import logging
from resource_management.TaskHandler import TaskHandler
from concurrent.futures import ThreadPoolExecutor
from orm.SqlHelper import SqlHelper
from orm.DatabaseModels import TableTask
from Model.Task import TaskStatus, PersistenceType
import time
import re


class ResourceManager(threading.Thread):
    def __init__(self, container, result_manager):
        super().__init__()
        # device空闲队列
        self.free = []
        # task等待队列
        self.wait = []
        # 记录可分配的device的数量的信号量
        self.free_sema = threading.Semaphore(0)
        # 记录需要执行的task的数量的信号量
        self.wait_sema = threading.Semaphore(0)
        # free队列访问锁
        self.free_lock = threading.Lock()
        # wait队列访问锁
        self.wait_lock = threading.Lock()

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.container = container
        self.result_manager = result_manager
        # self.execution_time = {}

        cmd = Commander.devices()
        ret = subprocess.run(cmd, shell=True, universal_newlines=True,
                             stdout=subprocess.PIPE)
        for line in ret.stdout.split('\n')[1:]:
            line = line.strip()
            if line != '':
                device_id = re.findall(r"(.*?)\t", line)[0]
                device = u2.connect_usb(device_id)
                self.save_snapshot(device)
                self.free.append(device)
                self.free_sema.release()
                # self.execution_time[device_id] = 0
        time.sleep(10)

        self.thread_pool = ThreadPoolExecutor()

    def commit_task(self, task):
        self.append_wait(task)

    def add_device(self, device_id):
        device = u2.connect_usb(device_id)
        self.append_free(device)

    def reboot(self, device_id):
        cmd = Commander.reboot(device_id)
        subprocess.run(cmd, shell=True, universal_newlines=True,
                       stdout=subprocess.PIPE)
        time.sleep(60)

    def handle_tasks(self):
        while True:
            # 从wait队列选择一个task
            self.wait_sema.acquire()
            # 从free队列选择一个device
            self.free_sema.acquire()
            task = self.wait.pop(0)
            device = self.free.pop(0)
            try:
                if not self.alive(device):
                    device = self.recovery(device, 600)
                if not self.alive(device):
                    self.recycle(device)
                    self.commit_task(task)
                    continue
                handler = TaskHandler(task, device, self, self.result_manager, self.container)
                handler.start()
                self.logger.info(f'the task({task.get_task_id()}) is being executed...')
            except Exception as error:
                logging.error(f'Due to an error,the task-({task.get_task_id()}) scheduling failed!')
                logging.error(f"Error:task-{task.get_task_id()}:{error}")
                self.recycle(device)
                task.set_status(TaskStatus.ERROR)
                task.set_end_time(time.asctime())
                if task.persistence == PersistenceType.DATABASE_DISK:
                    SqlHelper.update(TableTask, {'status': task.get_status(),
                                                 'end_time': task.get_end_time()},
                                     id=task.get_task_id())

    def load_snapshot(self, device):
        cmd = Commander.load_snapshot(device.serial, 'vm_initial_state')
        subprocess.run(cmd, shell=True, universal_newlines=True,
                       stdout=subprocess.PIPE)
        time.sleep(10)

    def save_snapshot(self, device):
        cmd = Commander.save_snapshot(device.serial, 'vm_initial_state')
        subprocess.run(cmd, shell=True, universal_newlines=True,
                       stdout=subprocess.PIPE)

    def append_wait(self, task):
        self.wait_lock.acquire()
        self.wait.append(task)
        self.wait_lock.release()
        self.wait_sema.release()

    def append_free(self, device):
        self.free_lock.acquire()
        self.free.append(device)
        self.free_lock.release()
        self.free_sema.release()

    def alive(self, device):
        if device is None:
            return False
        try:
            device.info
        except Exception as e:
            print(e)
            return False
        return True

    def connect_device(self, device):
        cur_device = None
        try:
            cur_device = u2.connect_usb(device.serial)
        except Exception as e:
            print(e)
        return cur_device if cur_device is not None else device

    def recovery(self, device, time_out=None):
        start_time = time.time()
        while (time_out is None or time.time() - start_time <= time_out) \
                and not self.alive(device):
            time.sleep(30)
            device = self.connect_device(device)
        return device

    # def release(self, device, task):
    #     start_time = task.get_start_time()
    #     time_cost = 0
    #     if start_time is not None:
    #         end_time = time.asctime() if task.get_end_time() is None else task.get_end_time()
    #         start_struct_time = datetime.datetime.strptime(start_time, '%a %b %d %H:%M:%S %Y')
    #         end_struct_time = datetime.datetime.strptime(end_time, '%a %b %d %H:%M:%S %Y')
    #         time_cost = (end_struct_time - start_struct_time).seconds
    #     self.execution_time[device.serial] += time_cost
    #     self.recycle_device(device)

    # def recycle_device(self, device, max_time=3600):
    #     device_id = device.serial
    #     # 如果执行时间不少于指定时间就重启设备
    #     if self.execution_time[device_id] >= max_time:
    #         print(f'reboot {device_id}')
    #         self.reboot(device_id)
    #         self.load_snapshot(device)
    #         device = self.connect_device(device)
    #         device = self.recovery(device)
    #         self.execution_time[device_id] = 0
    #     else:
    #         self.load_snapshot(device)
    #         # 如果设备连接有问题 先连接
    #         if not self.alive(device):
    #             device = self.recovery(device)
    #     self.append_free(device)

    def recycle(self, device):
        self.load_snapshot(device)
        if self.alive(device):
            device = self.recovery(device)
        self.append_free(device)

    def run(self):
        self.logger.info('Resource Manager is Started!')
        self.handle_tasks()


if __name__ == '__main__':
    device = u2.connect_usb('emulator-5554')
    device.app_stop('com.simplemobiletools.filemanager.pro')
