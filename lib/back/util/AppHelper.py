from util.Commander import Commander
import subprocess
from Model.App import App
from Model.Event import Event
from Model.Transition import Transition
from Model.State import State
from orm.SqlHelper import SqlHelper
from orm.DatabaseModels import TableApp, TableScript
from util.FileHelper import FileHelper
from PIL import Image
import os
import re
import xml.etree.ElementTree as ET

attributes = ['index', 'resource-id', 'class', 'package',
              'clickable', 'scrollable', 'long-clickable', 'checkable', 'bounds']


class AppHelper:
    @classmethod
    def package(cls, apk_path):
        cmd = Commander.apk_package_info(apk_path)
        ret = subprocess.run(cmd, shell=True, universal_newlines=True,
                             stdout=subprocess.PIPE)
        package_name = re.findall(r"name='(.*?)'", ret.stdout)[0]
        return package_name

    @classmethod
    def main_activity(cls, apk_path):
        cmd = Commander.apk_launchable_activity(apk_path)
        ret = subprocess.run(cmd, shell=True, universal_newlines=True,
                             stdout=subprocess.PIPE)
        try:
            main_activity_name = re.findall(r"name='(.*?)'", ret.stdout)[0]
        except:
            return None
        main_activity_name = main_activity_name.strip()
        return None if len(main_activity_name) == 0 else main_activity_name

    @classmethod
    def version(cls, apk_path):
        cmd = Commander.apk_version(apk_path)
        ret = subprocess.run(cmd, shell=True, universal_newlines=True,
                             stdout=subprocess.PIPE)
        try:
            version_name = re.findall(r"versionName='(.*?)'", ret.stdout)[0]
        except:
            return None
        version_name = version_name.strip()
        return None if len(version_name) == 0 else version_name

    @classmethod
    def permissions(cls, apk_path):
        cmd = Commander.permissions(apk_path)
        ret = subprocess.run(cmd, shell=True, universal_newlines=True,
                             stdout=subprocess.PIPE)
        _permissions = []
        for line in ret.stdout.splitlines():
            _permissions.append(re.findall(r"name='(.*?)'", line)[0])
        return _permissions

    @classmethod
    def create_app(cls, apk_path, source_code_path=None, persistence=False, move_file=False):
        package_name = cls.package(apk_path)
        version = cls.version(apk_path)
        app_row = SqlHelper.get_entity(TableApp, package_name=package_name, version=version)
        if app_row is not None:
            app = App(app_row.id, app_row.apk_path,
                      app_row.main_activity, app_row.package_name,
                      app_row.version, app_row.source_code_path,
                      app_row.permissions.split(','))
            return app
        app = App(None, apk_path, cls.main_activity(apk_path), package_name,
                  version, source_code_path, cls.permissions(apk_path))
        if persistence:
            # 保存到数据库
            key = SqlHelper.add_return_key(TableApp, 'id', package_name=app.get_package_name(),
                                           version=version,
                                           apk_path=apk_path,
                                           main_activity=app.get_main_activity(),
                                           source_code_path=app.get_source_code_path(),
                                           permissions=','.join(app.get_permissions()))
            # 保存自增主键
            app.set_id(key)
            # 保存到本地
            app_path = FileHelper.app_dir(key)
            FileHelper.create_dir(app_path)
            app_file = os.path.join(app_path, 'app.txt')
            # 保存apk
            new_apk_path = os.path.join(FileHelper.apk_dir(app.get_id()), os.path.basename(apk_path))
            app.set_apk_path(new_apk_path)
            # 路径不存在就创建
            if not os.path.exists(FileHelper.apk_dir(app.get_id())):
                os.makedirs(FileHelper.apk_dir(app.get_id()))
            if not move_file:
                FileHelper.copy(apk_path, new_apk_path)
            else:
                FileHelper.move(apk_path, FileHelper.apk_dir(app.get_id()))
            # 保存源码
            if source_code_path is not None:
                if not move_file:
                    FileHelper.copy(source_code_path, FileHelper.source_code_dir(app.get_id()))
                else:
                    FileHelper.move(source_code_path, FileHelper.app_dir(app.get_id()))
                app.set_source_code_path(FileHelper.source_code_dir(app.get_id()))
                # 打包源码
                FileHelper.zip(FileHelper.source_code_dir(app.get_id()), FileHelper.source_code_zip_file(app.get_id()))
            # 更新app信息
            SqlHelper.update(TableApp, {'apk_path': app.get_apk_path(),
                                        'source_code_path': app.get_source_code_path()}, id=app.get_id())
            # 保存app信息
            with open(app_file, 'w') as f:
                f.write(f"appId {app.get_id()}\n"
                        f"package name {app.get_package_name()}\n"
                        f"mainActivity {app.get_main_activity()}\n"
                        f"version {app.get_version()}\n"
                        f"permissions {app.get_permissions()}")

        return app

    @classmethod
    def init_apps(cls, apps_file_path):
        for file_name in os.listdir(apps_file_path):
            apk_path = os.path.join(apps_file_path, file_name)
            if os.path.isfile(apk_path) and file_name.endswith('apk'):
                cls.create_app(apk_path, None, True)

    @classmethod
    def init_script(cls, script_file_path, app_id):
        key = SqlHelper.add_return_key(TableScript, 'id', app_id=app_id)
        script_id = int(key)
        script_path = FileHelper.app_script_dir(app_id)
        FileHelper.create_dir(script_path)
        new_script_file_path = FileHelper.app_script_file(app_id, script_id)
        FileHelper.copy(script_file_path, new_script_file_path)
        SqlHelper.update(TableScript, {'path': new_script_file_path}, id=script_id)

    @classmethod
    def init_scripts(cls, scripts_dir, app_id):
        for file_name in os.listdir(scripts_dir):
            script_file_path = os.path.join(scripts_dir, file_name)
            cls.init_script(script_file_path, app_id)


if __name__ == '__main__':
    # app = AppHelper.create_app('/Users/xuhao/Desktop/jacoco_apps/alarmclock_jacoco.apk',
    #                            '/Users/xuhao/Desktop/Q-testing-benchmark1/alarmclock-2.2.3_r2.11', True)
    # print(app)
    # AppHelper.init_apps('/Users/xuhao/Downloads/APK/arp_models')
    AppHelper.init_apps('../../apks')
    # AppHelper.init_script(
    #     '/Users/xuhao/SeverProjects/online-android-vm-execution/vm_execution-back/scripts/SolidExplorerFileManagerTestingScript.py',
    #     58)
