import os
import shutil
import uuid
import zipfile


class FileHelper:
    project_dir = os.path.dirname(os.path.dirname(__file__))
    # project_dir = "/Users/xuhao/SeverProjects/online-android-vm-execution/vm_execution-back"
    storage_dir = os.path.join(project_dir, 'storage')
    users_dir = os.path.join(storage_dir, 'users')
    arps_dir = os.path.join(storage_dir, 'arps')
    apps_dir = os.path.join(storage_dir, 'apps')
    temp_dir = os.path.join(storage_dir, 'temp')
    sketches_dir = os.path.join(storage_dir, 'sketches')

    @classmethod
    def join(cls, *paths):
        return os.path.join(cls.project_dir, *paths)

    @classmethod
    def relative_join(cls, *paths):
        cur_dir = os.getcwd()
        return os.path.join(cur_dir, *paths)

    """
    apps目录
    """

    @classmethod
    def app_dir(cls, app_id):
        return os.path.join(cls.apps_dir, str(app_id))

    @classmethod
    def app_info_file(cls, app_id):
        return os.path.join(cls.app_dir(app_id), 'app.txt')

    @classmethod
    def apk_dir(cls, app_id):
        return os.path.join(cls.app_dir(app_id), 'apk')

    @classmethod
    def source_code_dir(cls, app_id):
        return os.path.join(cls.app_dir(app_id), 'source_code')

    @classmethod
    def source_code_zip_file(cls, app_id):
        return os.path.join(cls.app_dir(app_id), 'source_code.zip')

    @classmethod
    def manifest_file(cls, app_id):
        return os.path.join(cls.source_code_dir(app_id), 'app', 'src', 'main', 'AndroidManifest.xml')

    @classmethod
    def app_script_dir(cls, app_id):
        return os.path.join(cls.app_dir(app_id), 'scripts')

    @classmethod
    def app_script_file(cls, app_id, script_id):
        return os.path.join(cls.app_script_dir(app_id), f'testcase_{script_id}.py')

    """
    users目录
    """

    @classmethod
    def user_dir(cls, user_id):
        return os.path.join(cls.users_dir, str(user_id))

    @classmethod
    def task_dir(cls, user_id, task_id):
        return os.path.join(cls.user_dir(user_id), str(task_id))

    @classmethod
    def task_info_file(cls, user_id, task_id):
        return os.path.join(cls.task_dir(user_id, task_id), 'task.txt')

    @classmethod
    def task_script_dir(cls, user_id, task_id):
        return os.path.join(cls.task_dir(user_id, task_id), 'script')

    @classmethod
    def coverage_dir(cls, user_id, task_id):
        return os.path.join(cls.result_dir(user_id, task_id), 'coverage')

    @classmethod
    def coverage_output_dir(cls, user_id, task_id):
        return os.path.join(cls.coverage_dir(user_id, task_id), 'output')

    @classmethod
    def coverage_report_dir(cls, user_id, task_id):
        return os.path.join(cls.coverage_dir(user_id, task_id), 'report')

    @classmethod
    def coverage_temp_dir(cls, user_id, task_id):
        return os.path.join(cls.coverage_dir(user_id, task_id), 'temp')

    @classmethod
    def log_dir(cls, user_id, task_id):
        return os.path.join(cls.result_dir(user_id, task_id), 'logs')

    @classmethod
    def crash_log_file(cls, user_id, task_id):
        return os.path.join(cls.log_dir(user_id, task_id), 'crash_log.txt')

    @classmethod
    def coverage_log_file(cls, user_id, task_id):
        return os.path.join(cls.log_dir(user_id, task_id), 'icoverage.log')

    @classmethod
    def result_dir(cls, user_id, task_id):
        return os.path.join(cls.task_dir(user_id, task_id), 'result')

    @classmethod
    def result_zip_file(cls, user_id, task_id):
        return os.path.join(cls.task_dir(user_id, task_id), f'result_{task_id}.zip')

    """
    arps目录
    """

    @classmethod
    def arp_dir(cls, arp_id):
        return os.path.join(cls.arps_dir, str(arp_id))

    @classmethod
    def arp_model_dir(cls, arp_id):
        return os.path.join(cls.arp_dir(arp_id), 'model')

    @classmethod
    def screens_dir(cls, arp_id):
        return os.path.join(cls.arp_model_dir(arp_id), 'screens')

    @classmethod
    def screen_file(cls, arp_id, state_id):
        return os.path.join(cls.screens_dir(arp_id), f'{state_id}.png')

    @classmethod
    def layout_file(cls, arp_id, state_id):
        return os.path.join(cls.screens_dir(arp_id), f'{state_id}.xml')

    @classmethod
    def jump_pairs_file(cls, arp_id):
        return os.path.join(cls.arp_model_dir(arp_id), 'jump_pairs.txt')

    @classmethod
    def activity_info_file(cls, arp_id):
        return os.path.join(cls.arp_model_dir(arp_id), 'activity_info.txt')

    @classmethod
    def arp_model_zip(cls, arp_id):
        return os.path.join(cls.arp_dir(arp_id), 'arp_model.zip')

    """
    temp目录
    """

    @classmethod
    def temp_file_dir(cls, temp_id):
        return os.path.join(cls.temp_dir, str(temp_id))

    @classmethod
    def temp_apk_dir(cls, temp_id):
        return os.path.join(cls.temp_file_dir(temp_id), 'apk')

    @classmethod
    def temp_script_dir(cls, temp_id):
        return os.path.join(cls.temp_file_dir(temp_id), 'script')

    @classmethod
    def temp_source_code_dir(cls, temp_id):
        return os.path.join(cls.temp_file_dir(temp_id), 'source_code')

    @classmethod
    def temp_manifest_file(cls, temp_id):
        return os.path.join(cls.temp_source_code_dir(temp_id), 'app', 'src', 'main', 'AndroidManifest.xml')

    """
    sketches目录
    """

    @classmethod
    def sketch_dir(cls, user_id):
        return os.path.join(cls.sketches_dir, str(user_id))

    @classmethod
    def sketch_input_dir(cls, user_id):
        return os.path.join(cls.sketch_dir(user_id), 'input')

    @classmethod
    def sketch_input_image(cls, user_id):
        return os.path.join(cls.sketch_input_dir(user_id), 'sketch.jpg')

    @classmethod
    def sketch_model_dir(cls, user_id):
        return os.path.join(cls.sketch_dir(user_id), 'model_color')

    @classmethod
    def sketch_output(cls, user_id):
        return os.path.join(cls.sketch_dir(user_id), 'output')

    @classmethod
    def sketch_component_json(cls, user_id):
        return os.path.join(cls.sketch_output(user_id), 'sketch_component.json')

    @classmethod
    def sketch_jump_json(cls, user_id):
        return os.path.join(cls.sketch_output(user_id), 'sketch_jump.json')

    @classmethod
    def sketch_ui_json(cls, user_id):
        return os.path.join(cls.sketch_output(user_id), 'sketch_ui_info.json')

    # 将上传的文件保存在指定目录
    @classmethod
    def save(cls, saved_path, file_obj):
        cls.create_dir(saved_path)
        file_path = os.path.join(saved_path, file_obj.filename)
        file_obj.save(file_path)

    @classmethod
    def rename(cls, src, dst):
        os.rename(src, dst)

    @classmethod
    def move(cls, src, dst):
        if os.path.exists(src):
            cls.create_dir(dst)
            shutil.move(src, dst)

    @classmethod
    def zip(cls, src, dst):
        with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zip_f:
            for root, dirs, files in os.walk(src):
                fpath = root.replace(src, '')
                for f in files:
                    zip_f.write(os.path.join(root, f), os.path.join(fpath, f))

    @classmethod
    def unzip(cls, src, dst):
        with zipfile.ZipFile(src, 'r') as zip_f:
            for f in zip_f.namelist():
                zip_f.extract(f, dst)

    @classmethod
    def copy(cls, src, dst):
        if os.path.isfile(src):
            shutil.copy(src, dst)
        else:
            shutil.copytree(src, dst)

    @classmethod
    def copy_file(cls, src, dst):
        shutil.copyfile(src, dst)

    @classmethod
    def remove_file(cls, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    @classmethod
    def remove_dir(cls, dir_path):
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

    @classmethod
    def upload_apk(cls, temp_id, apk_obj):
        temp_apk_path = cls.temp_apk_dir(temp_id)
        cls.save(temp_apk_path, apk_obj)
        return os.path.join(temp_apk_path, apk_obj.filename)

    @classmethod
    def upload_script(cls, temp_id, script_obj):
        temp_script_path = cls.temp_script_dir(temp_id)
        cls.save(temp_script_path, script_obj)
        return os.path.join(temp_script_path, script_obj.filename)

    @classmethod
    def upload_source_code(cls, temp_id, source_code_obj):
        temp_source_code_path = cls.temp_source_code_dir(temp_id)
        cls.save(temp_source_code_path, source_code_obj)
        source_zip_path = os.path.join(temp_source_code_path, source_code_obj.filename)
        cls.unzip(source_zip_path, temp_source_code_path)
        cls.remove_file(source_zip_path)
        return temp_source_code_path

    @classmethod
    def move_temp(cls, temp_id, user_id, task_id, app_id):
        if app_id is not None:
            app_path = cls.app_dir(app_id)
            # 移动apk
            cls.move(cls.temp_apk_dir(temp_id), app_path)
            # 移动source code
            cls.move(cls.temp_source_code_dir(temp_id), app_path)
        if user_id is not None and task_id is not None:
            task_path = cls.task_dir(user_id, task_id)
            # 移动script
            cls.move(cls.temp_script_dir(temp_id), task_path)
        # 删除temp/temp_id目录
        cls.remove_dir(cls.temp_file_dir(temp_id))

    @classmethod
    def create_dir(cls, dir_path, override=False):
        if os.path.exists(dir_path):
            if override:
                shutil.rmtree(dir_path)
                os.makedirs(dir_path)
        else:
            os.makedirs(dir_path)

    @classmethod
    def generate_temp_id(cls):
        return str(uuid.uuid1())

    @classmethod
    def get_file_size(cls, file_path):
        size = 0
        if not os.path.exists(file_path):
            return size
        for root, dirs, files in os.walk(file_path):
            for f in files:
                size += os.path.getsize(os.path.join(root, f))
            for d in dirs:
                size += cls.get_file_size(os.path.join(root, d))
        return size

    @classmethod
    def get_apk_file_path(cls, app_id):
        apk_dir_path = cls.apk_dir(app_id)
        if os.path.exists(apk_dir_path):
            for f in os.listdir(apk_dir_path):
                f_path = os.path.join(apk_dir_path, f)
                if os.path.isfile(f_path) and os.path.splitext(f)[-1] == '.apk':
                    return f_path
        return None

    @classmethod
    def get_script_file_path(cls, user_id, task_id):
        script_dir_path = cls.task_script_dir(user_id, task_id)
        if os.path.exists(script_dir_path):
            for f in os.listdir(script_dir_path):
                f_path = os.path.join(script_dir_path, f)
                if os.path.isfile(f_path) and os.path.splitext(f)[-1] == '.py':
                    return f_path
        return None


if __name__ == '__main__':
    # FileHelper.zip(
    #     '/Users/xuhao/Desktop/Q-testing-benchmark2/notes',
    #     '/Users/xuhao/Desktop/Q-testing-benchmark2/notes.zip')
    # FileHelper.unzip('/Users/xuhao/Downloads/123.zip', '/Users/xuhao/Desktop')
    # FileHelper.remove_file('/Users/xuhao/Downloads/123.zip')
    # FileHelper.copy('/Users/xuhao/Desktop/notes_jacoco.apk', '/Users/xuhao/Documents/专利/ss.apsk')
    i = 43
    for dir in os.listdir('/Users/xuhao/Downloads/演示/2020-秋季-课程实验原始数据经过整理后的数据/研究生'):
        dir_path = os.path.join('/Users/xuhao/Downloads/演示/2020-秋季-课程实验原始数据经过整理后的数据/研究生', dir)
        script_file = os.path.join(dir_path, 'testcase.py')
        if os.path.isdir(dir_path) and os.path.exists(script_file):
            FileHelper.copy(script_file, os.path.join('/Users/xuhao/SeverProjects/online-android-vm-execution/scripts',
                                                      f"testcase_{i}.py"))
            i += 1
