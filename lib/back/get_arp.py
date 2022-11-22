from Model.Task import Task, PersistenceType
from AutomaticExploringFramework import AutomaticExploringFramework as AEF
import os
import re
import time
from Model.App import App
from executor.Executor import ExecutionStrategy
from comparison.StateComparison import StateComparisonStrategy
from util.AppHelper import AppHelper
from Model.AppRunningPathModel import AppRunningPathModel
from resource_management.ResourceManager import ResourceManager
from resource_management.TaskHandler import TaskHandler
from result_management.ResultManager import ResultManager
from container.Container import Container
from executor.appium_driver.AppiumScriptExecutor import AppiumScriptExecutor
import uiautomator2 as u2
from util.FileHelper import FileHelper
from werkzeug.datastructures import FileStorage

old_action='from appium.webdriver.common.touch_action import TouchAction\n'
new_action='from executor.appium_driver.TouchAction import TouchAction\n'

class MyARP():
    def __init__(self) -> None:
        pass
    def getARP(apk,script):
        apk_path = os.path.abspath(apk)
        script_file=None
        with open(script,'r+',encoding='utf-8') as fp:
            tmp=open('tmp.py','w+',encoding='utf-8')
            for line in fp.readlines():
                if line==old_action:
                    line=new_action
                tmp.write(line)
            tmp.close()
        with open('tmp.py','rb') as fp:
            script_file = FileStorage(fp)
            script_path = FileHelper.upload_script(10, script_file)
        os.remove('tmp.py')
        device=u2.connect_usb('emulator-5554')
        result=ResultManager()
        container=Container()
        container.put_execution_strategy(ExecutionStrategy.APPIUM.value, AppiumScriptExecutor)
        resource=ResourceManager(container,result)
        parameters = {'script_path': script_path}
        app = App(None, apk_path, None, AppHelper.package(apk_path), None)
        arp = AppRunningPathModel(None, app)
        task = Task(ExecutionStrategy.APPIUM, StateComparisonStrategy.XML, parameters, None, arp, False)
        task.set_task_id(12)
        task.set_persistence(PersistenceType.DISK)
        handler = TaskHandler(task, device, resource, result, container)
        handler.start()
        handler.join()
        #result.return_result()
        #print(task.get_arp().get_transitions()[0])
        return task.get_arp()

if __name__ == '__main__':
    MyARP.getARP()
