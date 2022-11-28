# -*- coding:utf8 -*-

import os
import shutil
import time

# import selenium
from executor.appium_driver.AppiumScriptDriver import AppiumScriptDriver
from executor.appium_driver.TouchAction import TouchAction


# 文件目录第一个item从instance=4开始
class SolidExplorerFileManager:
    def __init__(self, driver: AppiumScriptDriver, screen_path, xml_path, jump_pairs, delete=False):
        self.index = 0  # 当前的截图和xml的编号
        self.driver = driver  # webdriver.Remote()
        self.screen_path = screen_path  # 保存的截图的地址，例如 /Users/lgy/Desktop/测试脚本/RSFileManager/screens/
        self.xml_path = xml_path  # 保存的xml的地址，例如 /Users/lgy/Desktop/测试脚本/RSFileManager/screens/
        self.jump_pairs = jump_pairs  # 跳转文件的地址，例如：'/Users/lgy/Desktop/测试脚本/RSFileManager/jump_pairs.txt'
        # 删除之前保存的信息
        if delete:
            if os.path.exists(screen_path):
                shutil.rmtree(screen_path)
            if os.path.exists(xml_path):
                shutil.rmtree(xml_path)
            if os.path.exists(jump_pairs):
                os.remove(jump_pairs)
        if not os.path.exists(screen_path):
            os.makedirs(screen_path)
        if not os.path.exists(xml_path):
            os.makedirs(xml_path)

    #     self.package_name = driver.desired_capabilities['appPackage']
    #
    # def launch_app(self):
    #     self.driver.terminate(self.package_name)
    #     self.driver.

    def get_screen_info(self):
        # 默认都是在执执行3秒后，再进行截图和保存xml。可能某些操作需要更多的时间，在测试的时候加上
        time.sleep(3)
        screen_name = str(self.index) + ".png"
        self.driver.save_screenshot(os.path.join(self.screen_path, screen_name))
        xml_name = str(self.index) + ".xml"
        with open(os.path.join(self.xml_path, xml_name), 'w+') as fps:
            fps.write(self.driver.page_source)
        time.sleep(2)

    # 相当于每个动作函数为：保存执行动作之前的截图和xml，执行动作，保存执行的动作标号，更新index
    def my_back(self):
        self.get_screen_info()  # 保存执行动作前的截图和xml
        self.driver.back()
        fd = open(self.jump_pairs, 'a')
        fd.write(str(self.index) + ' ' + str(self.index + 1) + ' back\n')
        fd.close()
        self.index += 1

    def my_click_text(self, text):
        # 问题1：如果按照修改参数的形式多次执行同一个简单的脚本，无非获取bounds信息，因为bounds信息是每次需要识别
        self.get_screen_info()  # 保存执行动作前的截图和xml
        temp = 'new UiSelector().text("' + text + '")'  # 'new UiSelector().text("123")'
        self.driver.find_element_by_android_uiautomator(temp).click()
        fd = open(self.jump_pairs, 'a')
        fd.write(str(self.index) + ' ' + str(self.index + 1) + ' click' + '\n')
        fd.close()
        self.index += 1

    def my_click_text_start(self, text):
        self.get_screen_info()  # 保存执行动作前的截图和xml
        temp = 'new UiSelector().textStartsWith("' + text + '")'  # 'new UiSelector().text("123")'
        self.driver.find_element_by_android_uiautomator(temp).click()
        fd = open(self.jump_pairs, 'a')
        fd.write(str(self.index) + ' ' + str(self.index + 1) + ' click' + '\n')
        fd.close()
        self.index += 1

    def my_click_classname(self, classname, instance):
        # 问题1：如果按照修改参数的形式多次执行同一个简单的脚本，无非获取bounds信息，因为bounds信息是每次需要识别
        self.get_screen_info()  # 保存执行动作前的截图和xml
        self.driver.find_elements_by_class_name(classname)[instance].click()
        fd = open(self.jump_pairs, 'a')
        fd.write(str(self.index) + ' ' + str(self.index + 1) + ' click' + '\n')
        fd.close()
        self.index += 1

    def my_long_click_classname(self, classname, classname_index):
        self.get_screen_info()  # 保存执行动作前的截图和xml
        temp = self.driver.find_elements_by_class_name(classname)[classname_index]
        TouchAction(self.driver).long_press(temp).release().perform()
        fd = open(self.jump_pairs, 'a')
        fd.write(str(self.index) + ' ' + str(self.index + 1) + ' long_click' + '\n')
        fd.close()
        self.index += 1

    def my_click_accessibilty_id(self, accessibility_id):
        self.get_screen_info()  # 保存执行动作前的截图和xml
        self.driver.find_element_by_accessibility_id(accessibility_id).click()
        fd = open(self.jump_pairs, 'a')
        fd.write(str(self.index) + ' ' + str(self.index + 1) + ' click' + '\n')
        fd.close()
        self.index += 1

    def my_click_id(self, id):
        self.get_screen_info()  # 保存执行动作前的截图和xml
        self.driver.find_element_by_id(id).click()
        fd = open(self.jump_pairs, 'a')
        fd.write(str(self.index) + ' ' + str(self.index + 1) + ' click' + '\n')
        fd.close()
        self.index += 1

    def my_long_click_id(self, id):
        self.get_screen_info()
        temp = self.driver.find_element_by_id(id)
        TouchAction(self.driver).long_press(temp).perform()
        fd = open(self.jump_pairs, 'a')
        fd.write(str(self.index) + ' ' + str(self.index + 1) + ' long_click' + '\n')
        fd.close()
        self.index += 1

    def my_click_xpath(self, xpath):
        self.get_screen_info()
        self.driver.find_element_by_xpath(xpath).click()
        fd = open(self.jump_pairs, 'a')
        fd.write(str(self.index) + ' ' + str(self.index + 1) + ' click' + '\n')
        fd.close()
        self.index += 1

    def my_long_click_xpath(self, xpath):
        self.get_screen_info()
        temp = self.driver.find_element_by_xpath(xpath)
        TouchAction(self.driver).long_press(temp).release().perform()
        fd = open(self.jump_pairs, 'a')
        fd.write(str(self.index) + ' ' + str(self.index + 1) + ' long_click' + '\n')
        fd.close()
        self.index += 1

    def my_edit_id(self, id, text):
        self.get_screen_info()  # 保存执行动作前的截图和xml
        self.driver.find_element_by_id(id).send_keys(text)
        fd = open(self.jump_pairs, 'a')
        fd.write(str(self.index) + ' ' + str(self.index + 1) + ' edit ' + ' ' + text + '\n')
        fd.close()
        self.index += 1

    def my_edit_classname(self, classname, instance, text):
        self.get_screen_info()  # 保存执行动作前的截图和xml
        self.driver.find_elements_by_class_name(classname)[instance].send_keys(text)
        fd = open(self.jump_pairs, 'a')
        fd.write(str(self.index) + ' ' + str(self.index + 1) + ' edit ' + ' ' + text + '\n')
        fd.close()
        self.index += 1

    def my_edit_xpath(self, xpath, text):
        self.get_screen_info()  # 保存执行动作前的截图和xml
        self.driver.find_element_by_xpath(xpath).send_keys(text)
        fd = open(self.jump_pairs, 'a')
        fd.write(str(self.index) + ' ' + str(self.index + 1) + ' edit ' + ' ' + text + '\n')
        fd.close()
        self.index += 1

    def my_clear_id(self, id):
        self.get_screen_info()  # 保存执行动作前的截图和xml
        self.driver.find_element_by_id(id).clear()
        fd = open(self.jump_pairs, 'a')
        fd.write(str(self.index) + ' ' + str(self.index + 1) + ' clear' + '\n')
        fd.close()
        self.index += 1

    def my_clear_classname(self, classname, instance):

        self.get_screen_info()  # 保存执行动作前的截图和xml
        self.driver.find_elements_by_class_name(classname)[instance].clear()
        fd = open(self.jump_pairs, 'a')
        fd.write(str(self.index) + ' ' + str(self.index + 1) + ' clear' + '\n')
        fd.close()
        self.index += 1

    def my_clear_xpath(self, xpath):
        self.get_screen_info()  # 保存执行动作前的截图和xml
        self.driver.find_element_by_xpath(xpath).clear()
        fd = open(self.jump_pairs, 'a')
        fd.write(str(self.index) + ' ' + str(self.index + 1) + ' clear' + '\n')
        fd.close()
        self.index += 1

    def my_press_code(self, code_num):
        self.get_screen_info()
        self.driver.press_keycode(code_num)
        fd = open(self.jump_pairs, 'a')
        fd.write(str(self.index) + ' ' + str(self.index + 1) + ' press_code ' + str(code_num) + '\n')
        fd.close()
        self.index += 1

    def my_back_home(self):
        # 该函数是方便回到主界面
        # 点击home按钮
        self.my_click_xpath(
            "/hierarchy/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.ViewFlipper[1]/android.widget.RelativeLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.widget.ImageButton[1]")
        # 点击 0，到达文件浏览的主界面
        self.my_click_classname("android.widget.RelativeLayout", 1)

    # 接下来定义每个场景的描述。
    # 该场景可修改的参数。

    # 文件浏览：前序状态算是无
    # 可以修改的参数：进入的文件夹的序列
    # 1代表第一个item，2代表第二个item，以此类推。。。
    def file_browse_0(self, move_list, offset=2):
        '''
        :param move_list: [-1,1,2,3]，取值为-1和正数，其中-1表示进入当前界面的上层目录，1表示进入当前界面的第1个子文件夹
        '''
        for i in move_list:
            if i == -1:
                self.my_back()
            else:
                # 文件目录item 从instance=3开始
                self.my_click_xpath(f'//*[@resource-id="android:id/list"]/android.widget.RelativeLayout[{i}]')

    # 长按选中：前序状态0：在文件浏览的状态下进行长按选中
    # 可以修改的参数：当前界面可供选中的行数，需要选中的列表，最后选中的数量为1还是多个
    def long_click_1(self, select_list=None):
        '''
        :param select_list: 表示在当前界面需要选中的index，例如【2，3】。注意这个标号是从【1，sum】
        '''

        for i in select_list:
            if i == select_list[0]:
                self.my_long_click_xpath(f'//*[@resource-id="android:id/list"]/android.widget.RelativeLayout[{i}]')
            else:
                self.my_click_xpath(f'//*[@resource-id="android:id/list"]/android.widget.RelativeLayout[{i}]')
            # 最后的状态就是，选中提供的select_list中的行数，根据select_list的长度，判断是选中1个还是多个。

    # select_list=None表示，长按后取消选中，相当于最后没有选中

    # 文件压缩：前序状态13，点击menu后的界面
    # 可以修改的参数：压缩包的名称，是否压缩成功
    def compress_2(self, name=None, is_success=None):
        '''
        :param name: 压缩的名称, 取值为None:直接点击cancel，相当于取消压缩。取值不为None：需要输入压缩的名称，再判断是否需要确认压缩
        :param is_success: 是否压缩成功 True， False
        :return:
        '''
        # 两种调用方式，compress_2() 或者 compress_2("123",True)
        # 之前长按的数量为1和多个的时候，对应的menu是不一样的，其中compress的位置是不一样的，用text定位
        self.my_click_xpath('//android.widget.ListView/android.widget.LinearLayout[1]')
        if name is None:
            self.my_click_id('pl.solidexplorer2:id/button2')
        else:
            self.my_clear_id("pl.solidexplorer2:id/name")
            self.my_edit_id("pl.solidexplorer2:id/name", name)
            if is_success:
                self.my_click_id("pl.solidexplorer2:id/button1")
                time.sleep(8)
            else:
                self.my_click_id('pl.solidexplorer2:id/button2')

    # 文件搜索：前序状态0，是文件浏览的界面，点击search
    # 可以修改的参数：搜索的名称
    def search_3(self, text=None, move_to=None):
        '''
        :param text:取值为None:直接点击返回，相当于取消搜索。取值不为None：需要输入搜索的名称
        :return:
        '''
        # 点击文件浏览中的search按钮进入search界面
        self.my_click_id("pl.solidexplorer2:id/action_search")
        if text is not None:
            # 输入文本
            self.my_edit_id("pl.solidexplorer2:id/input", text)
            # 点击清除
            # self.my_click_id("com.github.uiautomator:id/keyboard")
            # # 点击语音输入
            # self.my_click_id("android:id/search_voice_btn")
            # 点击返回
            # self.my_back()
            # 再次输入文本
            # self.my_edit_id("pl.solidexplorer2:id/input", text)
            # 点击回车键，到达搜索结果界面
            self.my_press_code(66)
            if move_to is not None:
                time.sleep(2)
                self.file_browse_0(move_to, 2)
        # 回到搜索之前的界面
        self.my_click_id("pl.solidexplorer2:id/ab_icon")

    # 文件待粘贴：前序状态1：长按选择的界面点击剪切按钮  前序状态13：点击menu上的copy按钮
    # 可以修改的参数：前序状态，最后是否需要粘贴，要粘贴的文件夹
    def to_paste_4(self, is_paste, move_list):
        '''
        :param pre_num: 1为前序状态长按选中的界面然后进去剪切，2为前序状态为点击menu上的copy进行复制
        :param is_paste: True表示需要粘贴，False表示不需要
        :param move_list: [-1,1,2,3]，取值为-1和正数，其中-1表示进入当前界面的上层目录，1表示进入当前界面的第1个子文件夹
                  最后的状态是 根据move_list到达的界面，没有进入主界面。
        '''
        # if pre_num == 1:  # 前序状态是长按选择的界面，点击剪切【为了防止错误，剪切的都不粘贴】
        #     self.my_click_id("org.openintents.filemanager:id/menu_move")
        #     # org.openintents.filemanager:id/clipboard_action
        # else:
        #     self.my_click_text("Copy")
        #     # org.openintents.filemanager:id/clipboard_action
        self.my_click_id('pl.solidexplorer2:id/action_copy')
        self.file_browse_0(move_list, 0)
        if is_paste:
            # 点击menu
            # self.my_click_accessibilty_id("More options")
            # 点击Paste
            # self.my_click_text("Paste")
            self.my_click_id('pl.solidexplorer2:id/action_paste')
            time.sleep(5)
        else:  # 取消粘贴
            self.my_click_id("pl.solidexplorer2:id/ab_icon")

    # 侧边栏 前序状态是0 文件浏览
    def sidebar_6(self):
        self.my_click_id('pl.solidexplorer2:id/ab_icon')

    # 文件删除：前序状态1，长按选择的界面
    # 可以修改的参数：删除是否成功还是不成功
    def delete_file_7(self, is_success):
        '''
        :param is_success: 是否成功 True, False
        :return:
        '''
        # 点击长按选择界面的删除按钮
        self.my_click_id("pl.solidexplorer2:id/action_delete")
        # 点击永久删除按钮
        self.my_click_id("pl.solidexplorer2:id/delete_permanently")
        if is_success:
            self.my_click_id("pl.solidexplorer2:id/button1")
        else:
            self.my_click_id("pl.solidexplorer2:id/button2")

    # 创建文件夹：前序状态0
    # 可以修改的参数，是否成功，文件名
    def new_folder_10(self, folder_name=None, is_success=None):
        '''
        :param folder_name: 取值为None:直接点击cancel，相当于取消创建。取值不为None：需要输入创建的名称，再判断是否需要确认创建
        :param is_success: 是否成功 True, False
        :return:
        '''
        # 点击create folder
        self.my_click_id("pl.solidexplorer2:id/fab_expand_menu_button")
        self.my_click_id("pl.solidexplorer2:id/action_new_folder")
        if folder_name is None:
            self.my_click_id("pl.solidexplorer2:id/button2")
        else:
            # 输入文件名
            self.my_edit_classname('android.widget.EditText', 0, folder_name)
            if is_success:
                self.my_click_id("pl.solidexplorer2:id/button1")  # 点击ok
            else:
                self.my_click_id("pl.solidexplorer2:id/button2")  # 点击cancel

    # 查看文件属性：前序状态13，是长按选中一个后点击menu，才有Details按钮
    # 可以修改的参数：无
    def properties_browse_11(self):
        # 点击details按钮。
        self.my_click_xpath("//android.widget.ListView/android.widget.LinearLayout[6]/android.widget.LinearLayout[1]")
        # 点击OK
        # self.my_click_id("android:id/button1")

    # 重命名：前序状态13，是长按选中一个后点击menu，才会有rename。
    # 可以修改的参数，修改的文件名，是否修改
    def rename_12(self, name=None, is_success=None):
        '''
        :param name: 取值为None: 直接点击ok，相当于不修改。取值不为None：需要输入修改的名称，再判断是否需要确认修改
        :param is_success: 是否修改，True,False
        :return:
        '''
        # 点击Rename
        self.my_click_id("pl.solidexplorer2:id/action_rename")
        if name is None:  # 直接点击OK，相当于不修改
            self.my_click_id("pl.solidexplorer2:id/button2")
        else:
            # 清除原来的文件名
            self.my_click_classname("android.widget.EditText", 0)
            # 输入文件名
            self.my_edit_classname("android.widget.EditText", 0, name)
            if is_success:  # 确认修改
                self.my_click_id("pl.solidexplorer2:id/button1")
            else:
                self.my_click_id("pl.solidexplorer2:id/button2")

    # 点击menu：前序状态0或者1，文件浏览的界面的menu/文件长按后的界面的menu。
    # 可以修改的参数：无
    def menu_13(self):
        self.my_click_id("pl.solidexplorer2:id/action_overflow")

    # 设置：前序状态为6 侧边栏
    # 可以修改的参数：排序的选项，点击的checkbox，是否清理历史
    def settings_14(self, theme, primary_color, accent_color, icon_set):
        '''
        :param theme: [0,7]区间内一个数字 代表一种theme
        :param primary_color: [x,y]表示选项位置(因为选项排列是一个方型) 其中x属于[0,4] y属于[0,3]
        :param accent_color:[x,y]表示选项位置(因为选项排列是一个方型) 其中x属于[0,4] y属于[0,3]
        :param icon_set:[0,3]区间内一个数字 表示一种icon
        '''
        # 点击侧边栏上的settings
        self.my_click_id("pl.solidexplorer2:id/ab_icon")
        self.my_click_id("pl.solidexplorer2:id/action_settings")
        # 设置theme
        self.my_click_xpath(
            '//*[@resource-id="android:id/list"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]')
        self.my_click_classname('android.widget.CheckedTextView', theme)
        # 设置primary color
        self.my_click_xpath(
            '//*[@resource-id="android:id/list"]/android.widget.LinearLayout[2]/android.widget.LinearLayout[1]')
        try:
            self.my_click_xpath(
                f'//*[@content-desc="Color {primary_color[0] * 4 + primary_color[1] + 1}"]/android.widget.ImageView[1]')
        except Exception:
            self.my_click_xpath(
                f'//*[@content-desc="Color {primary_color[0] * 4 + primary_color[1] + 1} selected"]/android.widget.ImageView[1]')
        # 设置accent color
        self.my_click_xpath(
            '//*[@resource-id="android:id/list"]/android.widget.LinearLayout[3]/android.widget.RelativeLayout[1]')
        try:
            self.my_click_xpath(
                f'//*[@content-desc="Color {accent_color[0] * 4 + accent_color[1] + 1}"]/android.widget.ImageView[1]')
        except Exception:
            self.my_click_xpath(
                f'//*[@content-desc="Color {accent_color[0] * 4 + accent_color[1] + 1} selected"]/android.widget.ImageView[1]')
        # 设置icon set
        self.my_click_xpath(
            '//*[@resource-id="android:id/list"]/android.widget.LinearLayout[4]/android.widget.RelativeLayout[1]')
        self.my_click_classname('android.widget.TextView', icon_set)
        self.my_back()

    # bookmarks：前序状态为13menu，分为两种：
    def bookmarks_15(self, long_click_list=None, is_delete=None):
        '''
        :param long_click_list: 需要长按删除的列表，初始是有2个bookmarks【对应的classname标号为0，1】，所以从2开始标号
        :param is_delete: 是否需要删除，如果删除的话，就重新长按选中
        :return:
        '''
        # 第一种是点击Bookmark，第二种是点击Bookmarks
        self.my_click_text_start("Bookmark")
        self.my_click_xpath('//android.widget.ListView/android.widget.LinearLayout[6]')
        if long_click_list is not None:  # 说明是第二种情况
            # 长按选择第一个emulated
            self.my_long_click_classname("android.widget.RelativeLayout", 0)
            # 点击选择第二个0EE600BD
            self.my_click_classname("android.widget.RelativeLayout", 1)
            # 取消选择第一个emulated【此时状态是选中第二个】
            self.my_click_classname("android.widget.RelativeLayout", 0)
            # 选中要删除的行
            for i in long_click_list:  # 【2，3】
                self.my_click_classname("android.widget.RelativeLayout", i)
            # 取消选中第二个，就剩下选中要删除的
            self.my_click_classname("android.widget.RelativeLayout", 1)
            # 点击左上角的done
            self.my_click_id("android:id/action_mode_close_button")
            if is_delete:  # 需要删除的话
                # 重新长按选中需要删除的行
                for i in long_click_list:  # 【2，3】
                    if i == long_click_list[0]:
                        self.my_long_click_classname("android.widget.RelativeLayout", i)
                    else:
                        self.my_click_classname("android.widget.RelativeLayout", i)
                # 点击删除
                self.my_click_id("org.openintents.filemanager:id/menu_delete")
            # 点击返回，到文件浏览界面
            self.my_click_id("android:id/up")
