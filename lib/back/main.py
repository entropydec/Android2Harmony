from Model.Task import Task, PersistenceType
from AutomaticExploringFramework import AutomaticExploringFramework as AEF
import os
import time
from Model.App import App
from executor.Executor import ExecutionStrategy
from comparison.StateComparison import StateComparisonStrategy
from util.AppHelper import AppHelper
from Model.AppRunningPathModel import AppRunningPathModel

if __name__ == '__main__':
    # 结果文件存放路径
    # result_path = 'result'
    # android项目的manifest文件路径
    # manifest_file = os.path.abspath('../instrumentation/source_code/app/src/main/AndroidManifest.xml')
    # android项目的根目录
    # app_source_path = os.path.abspath('../instrumentation/source_code')
    apk_path = os.path.abspath('/Users/suou/study/Android2Harmony/online-android-vm-execution/apks/2-filemanagerpro.apk')
    # apk_path = '/Users/xuhao/SeverProjects/online-android-vm-execution/vm_execution-back/apk/SolidExplorerFileManager.apk'
    # task的参数，其中time_limit是运行时间(单位是s,测试时请设置为1h),manifest_file,app_source_path含义如上
    # parameters = {
    #     'arp_model_path': '/Users/xuhao/SeverProjects/online-android-vm-execution/vm_execution-back/storage/users/None/4/result'}
    # parameters = {
    #     'jump_pairs': '/Users/xuhao/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/2702e42ab6679d41bee105f942a07107/Message/MessageTemp/d27a621839521901125f48e2663d18df/File/jump_pairs.lst'}
    parameters = {'time_limit': 2400}
    # parameters = {
    #     'script_path': '/Users/xuhao/SeverProjects/online-android-vm-execution/vm_execution-back/scripts/SolidExplorerFileManagerTestingScript.py'}
    # app = App(None, apk_path, None, 'org.asdtm.goodweather', None)
    app = App(None, apk_path, None, AppHelper.package(apk_path), None)
    arp = AppRunningPathModel(None, app)
    af = AEF()
    af.start()
    # 只需要更改 'org.secuso.privacyfriendlynotes'(package name) 这一项，将其改为要执行的app的packagename即可
    task = Task(ExecutionStrategy.MCTS, StateComparisonStrategy.XML, parameters, None, arp, False)
    task.set_task_id(12)
    task.set_persistence(PersistenceType.DISK)
    # parameters2 = {'manifest_file': manifest_file, 'app_source_path': app_source_path,
    #                'script_path': 'scripts/SolidExplorerFileManagerTestingScript.py'}
    # app2 = App(None, None, 'pl.solidexplorer.SolidExplorer', 'pl.solidexplorer2', None)
    # task = Task(ExecutionStrategy.APPIUM, StateComparisonStrategy.XML,
    #             parameters2, None, app2, False)
    af.receive_task(task)
    time.sleep(1)
    print('aa')
