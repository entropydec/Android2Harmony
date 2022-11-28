# -*- coding:utf8 -*-

import time

from executor.appium_driver.AppiumScriptDriver import AppiumScriptDriver

from scripts.SEFM import SolidExplorerFileManager

# 配置信息
desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '9.0'
desired_caps['deviceName'] = 'Pixel 2 API 29'
desired_caps['appPackage'] = 'pl.solidexplorer2'
desired_caps['appActivity'] = 'pl.solidexplorer.SolidExplorer'
# desired_caps['noReset'] = True
# desired_caps['unicodeKeyboard'] = True

screen_path = 'screen/'
xml_path = 'xml/'
jump_pairs = './jump_pairs.txt'

# driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
driver = AppiumScriptDriver.build(desired_caps)
driver.implicitly_wait(5)
# time.sleep(20)

sefm = SolidExplorerFileManager(driver, screen_path, xml_path, jump_pairs, True)


def pre_testing():
    driver.find_element_by_id("pl.solidexplorer2:id/btn_skip").click()
    time.sleep(2)
    driver.find_element_by_id("pl.solidexplorer2:id/cb_license").click()
    driver.find_element_by_id("pl.solidexplorer2:id/button1").click()
    driver.find_element_by_id("pl.solidexplorer2:id/btn_next").click()
    driver.find_element_by_id("com.android.packageinstaller:id/permission_allow_button").click()


# pre_testing()


def compress_cancel(selected_list, name=None):
    sefm.long_click_1(selected_list)
    sefm.menu_13()
    # 文件压缩 压缩不要成功
    sefm.compress_2(name)
    # 回到0 文件浏览
    sefm.my_back()


def search(text, move_list):
    sefm.search_3(text, move_list)
    # 回到0 文件浏览
    sefm.my_back()


def to_paste(selected_list, move_to):
    sefm.long_click_1(selected_list)
    sefm.to_paste_4(False, move_to)
    sefm.my_back()


def delete_rename(selected_list, name):
    sefm.long_click_1(selected_list)
    sefm.delete_file_7(False)
    sefm.rename_12(name)
    sefm.my_back()


def delete(select_index, is_suceess=False):
    sefm.long_click_1([select_index])
    time.sleep(1)
    sefm.delete_file_7(is_suceess)


def batch_delete(selected_list, is_success=False):
    sefm.long_click_1(selected_list)
    time.sleep(1)
    sefm.delete_file_7(is_success)
    sefm.my_back()


def check_property(selected_list):
    sefm.long_click_1(selected_list)
    sefm.menu_13()
    sefm.properties_browse_11()
    sefm.my_back()
    sefm.my_back()


def create_folder(name):
    sefm.new_folder_10(name, False)


def setting(theme, primary_color, accent_color, icon_set):
    sefm.sidebar_6()
    sefm.settings_14(theme, primary_color, accent_color, icon_set)
    sefm.my_back()
    sefm.my_back()


# driver.find_elements_by_class_name('android.widget.RelativeLayout')[3].click()


sefm.file_browse_0([2, 1, 1, 1, -1, -1, -1, -1])
# sefm.file_browse_0([1, -1])
# sefm.file_browse_0([3, -1])
# sefm.file_browse_0([4, -1])
# sefm.file_browse_0([5, -1])

compress_cancel([2, 1, 4])
# compress_cancel([1, 5, 8])
# compress_cancel([3, 4, 8])
# compress_cancel([4, 3, 6])
# compress_cancel([5, 1, 3, 2])
# compress_cancel([1, 4, 6, 7])
# compress_cancel([3, 8, 2, 4])
# compress_cancel([1, 5])
# compress_cancel([3, 8])
# compress_cancel([6, 7, 8])

search('Android', [1, 1, 1, 1, -1, -1, -1, -1])
# search('Alarms', [1, -1])
# search('anymemo', [1, -1])
# search('Download', [1, -1])
# search('DCIM', [1, 1, -1, -1])
# search('Movies', [1, -1])
# search('Music', [1, -1])
# search('Movies', [1, -1])
# search('Notifications', [1, -1])
# search('Pictures', [1, -1])
# search('Podcasts', [1, -1])

to_paste([1], [2, 1, 1, 1, -1, -1, -1, -1])
# to_paste([2], [4, -1])
# to_paste([3], [1, -1])
# to_paste([4], [3, -1])
# to_paste([5], [6, -1])
# to_paste([6], [7, -1])
# to_paste([7], [4, -1])
# to_paste([8], [8, -1])
# to_paste([9], [5, -1])

for i in range(1, 8):
    delete_rename([i], f'rename_{i}')

create_folder('dasd')
# create_folder('12312')
# create_folder('fasda')
# create_folder('234dd')
# create_folder('yyyyyyy')
# create_folder('234')
# create_folder('3432d')
# create_folder('wqerw')
# create_folder('ewqe324')
# create_folder('fsd2')

check_property([1, 2, 3, 4])
# check_property([2, 4, 5, 4])
# check_property([7, 6, 2, 3])
# check_property([4, 5, 6, 2])
# check_property([3, 1, 2, 6])
# check_property([5, 8])
# check_property([1, 7])
# check_property([2, 5])
# check_property([8, 6])
# check_property([1, 4])

compress_cancel([1, 2, 3], 'asdas')
# compress_cancel([1, 2, 3, 4], 'asda213')
# compress_cancel([1, 2, 3, 4, 5], 'weqw21321')
# compress_cancel([1, 2, 3, 4, 5, 6], 'adsa213')
# compress_cancel([1, 4, 6], 'awewqe123')
# compress_cancel([1, 4, 5], 'sad22')
# compress_cancel([2, 4, 5], 'wqeq22')
# compress_cancel([2, 4, 6], 'wqe22')
# compress_cancel([2, 3, 7], '21312sad')
# compress_cancel([2, 3, 6], 'wsewq222')

# sefm.file_browse_0([1])
# for i in range(1, 11):
#     sefm.new_folder_10(f"{i}-folder", True)
#     time.sleep(2)
#     delete(1, True)
#     time.sleep(1)
# sefm.file_browse_0([-1])

batch_delete([1])
# batch_delete([1, 2])
# batch_delete([1, 2, 3])
# batch_delete([1, 2, 3, 4])
# batch_delete([1, 2, 3, 4, 5])
# batch_delete([1, 2, 3, 4, 5, 6])
# batch_delete([1, 2, 3, 4, 5, 6, 7])
# batch_delete([1, 2, 3, 4, 5, 6, 7, 8])

setting(5, [2, 3], [1, 2], 2)
# setting(2, [1, 2], [2, 1], 1)
# setting(3, [2, 2], [3, 1], 3)
# setting(1, [1, 3], [1, 1], 1)
# setting(0, [2, 3], [1, 2], 0)
# setting(1, [1, 2], [2, 2], 1)
# setting(2, [2, 2], [3, 1], 2)
# setting(3, [1, 3], [1, 3], 3)
# setting(4, [1, 3], [1, 2], 0)
# setting(5, [1, 3], [2, 3], 1)
# setting(6, [1, 3], [2, 1], 2)
# setting(7, [1, 3], [3, 2], 3)
# setting(0, [1, 3], [2, 3], 0)
# setting(1, [1, 3], [3, 1], 1)
# setting(2, [1, 3], [2, 2], 2)

# 最后一定要加入保存最后一个状态的图片的代码
sefm.get_screen_info()

driver.save_result('../result')
