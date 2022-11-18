from Model.Task import Task
from uiautomator2 import Device
from monitor.Monitor import Monitor
from enum import Enum
from executor.DeviceWrapper import DeviceWrapper
from executor.Watcher import Watcher
from Model.AppRunningPathModel import AppRunningPathModel


class ExecutionStrategy(Enum):
    Q_LEARNING = 'q_learning'
    RANDOM = 'random_strategy'
    APPIUM = 'appium_strategy'
    SIMPLE_SCRIPT = 'simple_script_strategy'
    DYNAMIC_MODEL = 'dynamic_model_driver'
    SCRIPT_SEQUENCE = 'script_sequence_Driver'
    MCTS = "mcts_strategy"


allow_identifier = {'resourceId': "com.android.permissioncontroller:id/permission_allow_button"}
continue_identifier = {'resourceId': "com.android.permissioncontroller:id/continue_button"}
open_with_identifier = {'resourceId': "android:id/title",
                        'textMatches': 'Open with|open with|Share|share|Complete action using|complete action using'}
close_app_identifier = {'resourceId': 'android:id/aerr_close', 'textMatches': 'Close app|close app|Close App|CLOSE APP'}
check_box_identifier = {'resourceId': 'android:id/switch_widget', 'checked': False}
use_this_folder_identifier = {
    # 'resourceId': "android:id/title",
    'textMatches': 'USE THIS FOLDER|use this folder|Use This Folder|Use this folder'}
ok_identifier = {'textMatches': 'Y|y|ALLOW|allow|Allow|OK|ok|Ok|是|确认|确定|同意|Continue|continue|CONTINUE|继续'}


class Executor(DeviceWrapper):

    def __init__(self, arp: AppRunningPathModel, device: Device, monitor: Monitor, parameters: dict):
        super().__init__(device, monitor, arp.get_app())
        self.arp = arp
        self.parameters = parameters
        self.device = device
        self.monitor = monitor
        self.watchers = []
        self.__init_watchers()

    def __init_watchers(self):
        allow_watcher = Watcher(self.device, self.monitor, self.arp.get_app()) \
            .when(resourceId="com.android.permissioncontroller:id/permission_allow_button") \
            .click(resourceId="com.android.permissioncontroller:id/permission_allow_button")

        while_using_this_app_watcher = Watcher(self.device, self.monitor, self.arp.get_app()) \
            .when(resourceId="com.android.permissioncontroller:id/permission_allow_foreground_only_button") \
            .click(resourceId="com.android.permissioncontroller:id/permission_allow_foreground_only_button")

        continue_watcher = Watcher(self.device, self.monitor, self.arp.get_app()) \
            .when(resourceId="com.android.permissioncontroller:id/continue_button") \
            .click(resourceId="com.android.permissioncontroller:id/continue_button")

        open_with_watcher = Watcher(self.device, self.monitor, self.arp.get_app()) \
            .when(resourceId="android:id/title",
                  textMatches='Open with|open with|Share|share|Complete action using|complete action using') \
            .back()

        close_app_watcher = Watcher(self.device, self.monitor, self.arp.get_app()) \
            .when(resourceId='android:id/aerr_close', textMatches='Close app|close app|Close App|CLOSE APP') \
            .click(resourceId='android:id/aerr_close', textMatches='Close app|close app|Close App|CLOSE APP')

        check_box_watcher = Watcher(self.device, self.monitor, self.arp.get_app()) \
            .when(resourceId='android:id/switch_widget', checked=False) \
            .click(resourceId='android:id/switch_widget', checked=False)

        use_this_folder_watcher = Watcher(self.device, self.monitor, self.arp.get_app()) \
            .when(textMatches='USE THIS FOLDER|use this folder|Use This Folder|Use this folder') \
            .click(textMatches='USE THIS FOLDER|use this folder|Use This Folder|Use this folder')

        folders_watcher = Watcher(self.device, self.monitor, self.arp.get_app()) \
            .when(resourceId='com.google.android.documentsui:id/icon_mime_sm') \
            .click(resourceId='com.google.android.documentsui:id/icon_mime_sm')

        no_items_watcher = Watcher(self.device, self.monitor, self.arp.get_app()) \
            .when(resourceId="com.google.android.documentsui:id/message",
                  textMatches="No items|no items|No Items|NO ITEMS") \
            .back()

        cancel_installation_watcher = Watcher(self.device, self.monitor, self.arp.get_app()) \
            .when(packageName="com.google.android.packageinstaller", textMatches="Cancel|cancel|CANCEL|取消") \
            .click(packageName="com.google.android.packageinstaller", textMatches="Cancel|cancel|CANCEL|取消")

        ok_watcher = Watcher(self.device, self.monitor, self.arp.get_app()) \
            .when(textMatches='Y|y|ALLOW|allow|Allow|OK|ok|Ok|是|确认|确定|同意|Continue|continue|CONTINUE|继续') \
            .click(textMatches='Y|y|ALLOW|allow|Allow|OK|ok|Ok|是|确认|确定|同意|Continue|continue|CONTINUE|继续')

        back_watcher = Watcher(self.device, self.monitor, self.arp.get_app()) \
            .when(className='android.widget.ImageButton', descriptionMatches='back|Back|BACK|返回|Navigate up') \
            .click(className='android.widget.ImageButton', descriptionMatches='back|Back|BACK|返回|Navigate up')

        default_watcher = Watcher(self.device, self.monitor, self.arp.get_app()) \
            .home().stop().launch()

        self.watchers.append(allow_watcher)
        self.watchers.append(while_using_this_app_watcher)
        self.watchers.append(continue_watcher)
        self.watchers.append(open_with_watcher)
        self.watchers.append(close_app_watcher)
        self.watchers.append(check_box_watcher)
        self.watchers.append(use_this_folder_watcher)
        self.watchers.append(folders_watcher)
        self.watchers.append(no_items_watcher)
        self.watchers.append(cancel_installation_watcher)
        self.watchers.append(ok_watcher)
        self.watchers.append(back_watcher)
        self.watchers.append(default_watcher)

    def execute(self):
        pass
