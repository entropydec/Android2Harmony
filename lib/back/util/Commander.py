import sys, os
from uiautomator2 import Device
from util.FileHelper import FileHelper


class Commander:

    # 合并多条指令
    @classmethod
    def merge(cls, *cmds):
        return "&&".join(cmds)

    @classmethod
    def devices(cls):
        return "adb devices"

    @classmethod
    def reboot(cls, serial):
        return f"adb -s {serial} reboot"

    @classmethod
    def save_snapshot(cls, serial, name):
        return f"adb -s {serial} emu avd snapshot save {name}"

    @classmethod
    def load_snapshot(cls, serial, name):
        return f"adb -s {serial} emu avd snapshot load {name}"

    # example:  package: name='org.asdtm.goodweather' versionCode='13' versionName='4.4' platformBuildVersionName='7.1.1'
    @classmethod
    def apk_package_info(cls, apk_path):
        if sys.platform.startswith('win'):
            return f'aapt dump badging {apk_path} | find "package"'
        else:
            return f"aapt dump badging {apk_path} | grep 'package'"

    # example: launchable-activity: name='org.asdtm.goodweather.MainActivity'  label='Good Weather' icon=''
    @classmethod
    def apk_launchable_activity(cls, apk_path):
        if sys.platform.startswith('win'):
            return f'aapt dump badging {apk_path} | find "launchable-activity"'
        else:
            return f"aapt dump badging {apk_path} | grep 'launchable-activity'"

    @classmethod
    def apk_version(cls, apk_path):
        if sys.platform.startswith('win'):
            return f'aapt dump badging {apk_path} | find "version"'
        else:
            return f"aapt dump badging {apk_path} | grep 'version'"

    @classmethod
    def dump_coverage(cls, dumped_path, device: Device, package_name, log_path=None):
        serial_num = device.serial
        # coverage_log_file = os.path.join(dumped_path, 'icoverage.log')
        shell_path = FileHelper.join('util', 'dumpCoverage.sh')
        if log_path is None:
            return f"{shell_path} {dumped_path} {serial_num} {package_name}"
        else:
            return f"{shell_path} {dumped_path} {serial_num} {package_name} &> {log_path} &"

    @classmethod
    def clear_crash_log(cls, serial):
        return f"adb -s {serial} logcat -c"

    @classmethod
    def dump_crash_log(cls, serial, log_path):
        log_filer = 'AndroidRuntime:E CrashAnrDetector:D ActivityManager:E SQLiteDatabase:E WindowManager:E ActivityThread:E Parcel:E *:F *:S'
        return f"adb -s {serial} logcat {log_filer} >> {log_path} &"

    @classmethod
    def coverage_test_report(cls, coverage_file_path):
        return f"gradle jacocoTestReportMergeWithParameter -PnewCoverageFilePath={coverage_file_path}"

    @classmethod
    def permissions(cls, apk_path):
        if sys.platform.startswith('win'):
            return f'aapt d permissions {apk_path} | find "uses-permission"'
        else:
            return f"aapt d permissions {apk_path} | grep 'uses-permission'"
