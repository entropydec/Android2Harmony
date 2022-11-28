# from appium_driver import webdriver
# from appium_driver.webdriver.common.touch_action import TouchAction
#
# from utils import ScriptTool
from executor.appium_driver.TouchAction import TouchAction


def skip_introduction(driver):
    # tool.save_page_and_path_info(0, None, None)
    el1 = driver.find_element_by_id("pl.solidexplorer2:id/btn_skip")
    el1.click()
    # tool.save_page_and_path_info(0, 'click', [664, 1658, 784, 1783])
    el2 = driver.find_element_by_id("pl.solidexplorer2:id/cb_license")
    el2.click()
    # tool.save_page_and_path_info(0, 'click', [42, 1518, 1038, 1602])
    el3 = driver.find_element_by_id("pl.solidexplorer2:id/button1")
    el3.click()
    # tool.save_page_and_path_info(0, 'click', [452, 1635, 628, 1730])
    el4 = driver.find_element_by_id("pl.solidexplorer2:id/btn_next")
    el4.click()
    # tool.save_page_and_path_info(0, 'click', [806, 1658, 1069, 1783])
    # el5 = driver.find_element_by_id("com.android.permissioncontroller:id/permission_allow_button")
    # el5.click()
    # el6 = driver.find_element_by_id("pl.solidexplorer2:id/button2")
    # el6.click()
    # el6 = driver.find_element_by_id("pl.solidexplorer2:id/button1")
    # el6.click()
    # el7 = driver.find_element_by_id("android:id/button1")
    # el7.click()
    # el8 = driver.find_element_by_id("android:id/button1")
    # el8.click()
    # tool.save_page_and_path_info(0, 'click', [70, 981, 968, 1128])
    # time.sleep(2)
    # el6 = driver.find_element_by_id('android:id/button1')
    # el6.click()


def fun1(driver):
    # skip_introduction(driver)
    el1 = driver.find_element_by_id("pl.solidexplorer2:id/action_search")
    el1.click()
    # tool.save_page_and_path_info(1, 'click', [828, 63, 954, 210])
    el2 = driver.find_element_by_id("pl.solidexplorer2:id/input")
    el2.send_keys("ooiw")
    # tool.save_page_and_path_info(1, 'edit', [147, 84, 954, 189, 1])
    el3 = driver.find_element_by_id("pl.solidexplorer2:id/action_overflow")
    el3.click()
    # tool.save_page_and_path_info(2, 'click', [954, 63, 1080, 210])
    driver.back()
    # tool.save_page_and_path_info(1, 'back', None)
    el4 = driver.find_element_by_id("pl.solidexplorer2:id/ab_icon")
    el4.click()
    # tool.save_page_and_path_info(0, 'click', [0, 63, 147, 210])


def fun2(driver):
    # skip_introduction(driver)
    el1 = driver.find_element_by_xpath(
        "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/pl.solidexplorer.common.gui.drawer.DrawerLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.GridView/android.widget.RelativeLayout[1]/android.widget.ImageView")
    el1.click()
    # tool.save_page_and_path_info(3, 'click', [42, 357, 168, 483])
    el2 = driver.find_element_by_id("pl.solidexplorer2:id/action_overflow")
    el2.click()
    # tool.save_page_and_path_info(3, 'click', [900, 1647, 1080, 1794])
    driver.back()
    # tool.save_page_and_path_info(3, 'back')
    el3 = driver.find_element_by_id("pl.solidexplorer2:id/action_copy")
    el3.click()
    # tool.save_page_and_path_info(4, 'click', [180, 1647, 360, 1794])
    el4 = driver.find_element_by_id("pl.solidexplorer2:id/action_new_folder")
    el4.click()
    # tool.save_page_and_path_info(5, 'click', [819, 1647, 945, 1794])
    el5 = driver.find_element_by_xpath(
        "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.FrameLayout/android.widget.ScrollView/android.widget.EditText")
    el5.send_keys("123_2")
    # tool.save_page_and_path_info(5, 'edit', [122, 906, 958, 1027, '123_2'])
    el6 = driver.find_element_by_id("pl.solidexplorer2:id/button1")
    el6.click()
    # tool.save_page_and_path_info(4, 'click', [853, 1085, 979, 1180])
    el7 = driver.find_element_by_id("pl.solidexplorer2:id/action_copy")
    el7.click()
    # tool.save_page_and_path_info(4, 'click', [945, 1647, 1080, 1794])
    el8 = driver.find_element_by_id("pl.solidexplorer2:id/button1")
    el8.click()
    # tool.save_page_and_path_info(4, 'click', [477, 1062, 603, 1157])
    el9 = driver.find_element_by_id("pl.solidexplorer2:id/action_paste")
    el9.click()
    # tool.save_page_and_path_info(3, 'click', [0, 1647, 819, 1794])
    el10 = driver.find_element_by_id("pl.solidexplorer2:id/remember")
    el10.click()
    # tool.save_page_and_path_info(3, 'click', [122, 1133, 418, 1217])
    el11 = driver.find_element_by_id("pl.solidexplorer2:id/option_old_label")
    el11.click()
    # tool.save_page_and_path_info(0, 'click', [560, 875, 938, 969])
    el12 = driver.find_element_by_xpath(
        "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/pl.solidexplorer.common.gui.drawer.DrawerLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.GridView/android.widget.RelativeLayout[10]/android.widget.ImageView")
    el12.click()
    # tool.save_page_and_path_info(3, 'click', [42, 1647, 168, 1773])
    el13 = driver.find_element_by_id("pl.solidexplorer2:id/action_delete")
    el13.click()
    # tool.save_page_and_path_info(7, 'click', [360, 1647, 540, 1794])
    el14 = driver.find_element_by_id("pl.solidexplorer2:id/button1")
    el14.click()
    # tool.save_page_and_path_info(0, 'click', [628, 1070, 979, 1165])


def fun3(driver):
    # skip_introduction(driver)
    el1 = driver.find_element_by_xpath(
        "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/pl.solidexplorer.common.gui.drawer.DrawerLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.GridView/android.widget.RelativeLayout[1]/android.widget.ImageView")
    el1.click()
    # tool.save_page_and_path_info(3, 'click', [42, 357, 168, 483])
    el2 = driver.find_element_by_id("pl.solidexplorer2:id/action_share")
    el2.click()
    # tool.save_page_and_path_info(8, 'click', [540, 1647, 720, 1794])
    driver.back()
    # tool.save_page_and_path_info(3, 'back')
    el3 = driver.find_element_by_id("pl.solidexplorer2:id/action_rename")
    el3.click()
    # tool.save_page_and_path_info(9, 'click', [720, 1647, 900, 1794])
    el4 = driver.find_element_by_xpath(
        "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.FrameLayout/android.widget.ScrollView/android.widget.EditText")
    el4.clear()
    el4.send_keys("123_1")
    # tool.save_page_and_path_info(9, 'edit', [122, 906, 958, 1027, '123_1'])
    el5 = driver.find_element_by_id("pl.solidexplorer2:id/button1")
    el5.click()
    # tool.save_page_and_path_info(0, 'click', [853, 1085, 979, 1180])
    el6 = driver.find_element_by_xpath(
        "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/pl.solidexplorer.common.gui.drawer.DrawerLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.GridView/android.widget.RelativeLayout[1]/android.widget.ImageView")
    el6.click()
    # tool.save_page_and_path_info(3, 'click', [42, 357, 168, 483])
    el7 = driver.find_element_by_id("pl.solidexplorer2:id/action_rename")
    el7.click()
    # tool.save_page_and_path_info(9, 'click', [720, 1647, 900, 1794])
    el8 = driver.find_element_by_xpath(
        "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.FrameLayout/android.widget.ScrollView/android.widget.EditText")
    el8.clear()
    el8.send_keys("123")
    # tool.save_page_and_path_info(9, 'edit', [122, 906, 958, 1027, '123'])
    el9 = driver.find_element_by_id("pl.solidexplorer2:id/button1")
    el9.click()
    # tool.save_page_and_path_info(0, 'click', [853, 1085, 979, 1180])


def fun4(driver):
    # skip_introduction(driver)
    TouchAction(driver).press(x=500, y=1721).move_to(x=400, y=839).release().perform()
    # tool.save_page_and_path_info(0, 'swipe', [500, 1721, 400, 839])
    TouchAction(driver).press(x=461, y=272).move_to(x=514, y=1655).release().perform()
    # tool.save_page_and_path_info(0, 'swipe', [461, 272, 514, 1655])
    el1 = driver.find_element_by_xpath(
        "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/pl.solidexplorer.common.gui.drawer.DrawerLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.GridView/android.widget.RelativeLayout[1]/android.widget.ImageView")
    el1.click()
    # tool.save_page_and_path_info(3, 'click', [42, 357, 168, 483])
    el2 = driver.find_element_by_id("pl.solidexplorer2:id/action_cut")
    el2.click()
    # tool.save_page_and_path_info(3, 'click', [0, 1647, 180, 1794])
    el3 = driver.find_element_by_id("pl.solidexplorer2:id/action_cut")
    el3.click()
    # tool.save_page_and_path_info(4, 'click', [945, 1647, 1080, 1794])
    el4 = driver.find_element_by_id("pl.solidexplorer2:id/button1")
    el4.click()
    # tool.save_page_and_path_info(3, 'click', [477, 1062, 603, 1157])
    el5 = driver.find_element_by_id("pl.solidexplorer2:id/action_paste")
    el5.click()
    # tool.save_page_and_path_info(0, 'click', [0, 1647, 819, 1794])
    el6 = driver.find_element_by_id("pl.solidexplorer2:id/fab_expand_menu_button")
    el6.click()
    # tool.save_page_and_path_info(6, 'click', [865, 1579, 1059, 1773])
    driver.back()
    # tool.save_page_and_path_info(0, 'back')
    el6.click()
    # tool.save_page_and_path_info(3, 'click', [865, 1579, 1059, 1773])
    el7 = driver.find_element_by_id("pl.solidexplorer2:id/action_new_folder")
    el7.click()
    # tool.save_page_and_path_info(5, 'click', [886, 1093, 1038, 1245])
    el8 = driver.find_element_by_xpath(
        "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.FrameLayout/android.widget.ScrollView/android.widget.EditText")
    el8.send_keys("hello_123")
    # tool.save_page_and_path_info(5, 'edit', [122, 906, 958, 1027, 'hello_123'])
    el9 = driver.find_element_by_id("pl.solidexplorer2:id/button1")
    el9.click()
    # tool.save_page_and_path_info(0, 'click', [853, 1085, 979, 1180])
    el10 = driver.find_element_by_xpath(
        "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/pl.solidexplorer.common.gui.drawer.DrawerLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.GridView/android.widget.RelativeLayout[10]/android.widget.ImageView")
    el10.click()
    # tool.save_page_and_path_info(3, 'click', [42, 1647, 168, 1773])
    el11 = driver.find_element_by_id("pl.solidexplorer2:id/action_delete")
    el11.click()
    # tool.save_page_and_path_info(7, 'click', [360, 1647, 540, 1794])
    el12 = driver.find_element_by_id("pl.solidexplorer2:id/delete_permanently")
    el12.click()
    # tool.save_page_and_path_info(7, 'click', [122, 928, 958, 1012])
    el13 = driver.find_element_by_id("pl.solidexplorer2:id/button1")
    el13.click()
    # tool.save_page_and_path_info(7, 'click', [790, 1070, 979, 1165])


def fun5(driver):
    # skip_introduction(driver)
    el1 = driver.find_element_by_id("pl.solidexplorer2:id/fab_expand_menu_button")
    el1.click()
    # tool.save_page_and_path_info(3, 'click', [865, 1579, 1059, 1773])
    el2 = driver.find_element_by_id("pl.solidexplorer2:id/action_new_file")
    el2.click()
    # tool.save_page_and_path_info(10, 'click', [886, 1255, 1038, 1407])
    el3 = driver.find_element_by_xpath(
        "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.FrameLayout/android.widget.ScrollView/android.widget.EditText")
    el3.send_keys("hello_123")
    # tool.save_page_and_path_info(10, 'edit', [122, 906, 958, 1027, 'hello_123'])
    el4 = driver.find_element_by_id("pl.solidexplorer2:id/button1")
    el4.click()
    # tool.save_page_and_path_info(0, 'click', [853, 1085, 979, 1180])
    el5 = driver.find_element_by_xpath(
        "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/pl.solidexplorer.common.gui.drawer.DrawerLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.GridView/android.widget.RelativeLayout[10]/android.widget.ImageView")
    el5.click()
    # tool.save_page_and_path_info(3, 'click', [42, 1647, 168, 1773])
    el6 = driver.find_element_by_id("pl.solidexplorer2:id/action_overflow")
    el6.click()
    # tool.save_page_and_path_info(3, 'click', [900, 1647, 1080, 1794])
    driver.back()
    # tool.save_page_and_path_info(3, 'back')
    el7 = driver.find_element_by_id("pl.solidexplorer2:id/action_delete")
    el7.click()
    # tool.save_page_and_path_info(7, 'click', [360, 1647, 540, 1794])
    el8 = driver.find_element_by_id("pl.solidexplorer2:id/delete_permanently")
    el8.click()
    # tool.save_page_and_path_info(7, 'click', [122, 928, 958, 1012])
    el9 = driver.find_element_by_id("pl.solidexplorer2:id/button1")
    el9.click()
    # tool.save_page_and_path_info(0, 'click', [790, 1070, 979, 1165])
    driver.back()
    # tool.save_page_and_path_info(0, 'back')
    TouchAction(driver).press(x=457, y=395).move_to(x=457, y=1655).release().perform()
    # tool.save_page_and_path_info(0, 'swipe', [457, 395, 457, 1655])
    el10 = driver.find_element_by_xpath(
        "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/pl.solidexplorer.common.gui.drawer.DrawerLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.GridView/android.widget.RelativeLayout[1]/android.widget.ImageView")
    el10.click()
    # tool.save_page_and_path_info(3, 'click', [42, 357, 168, 483])
    el11 = driver.find_element_by_id("pl.solidexplorer2:id/action_overflow")
    el11.click()
    # tool.save_page_and_path_info(3, 'click', [900, 1647, 1080, 1794])
    el12 = driver.find_element_by_xpath(
        "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[6]/android.widget.LinearLayout")
    el12.click()
    # tool.save_page_and_path_info(0, 'click', [534, 1212, 996, 1338])


def fun6(driver):
    # skip_introduction(driver)
    el1 = driver.find_element_by_id("pl.solidexplorer2:id/ab_icon")
    el1.click()
    # tool.save_page_and_path_info(0, 'click', [0, 63, 147, 210])
    el2 = driver.find_element_by_xpath(
        "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/pl.solidexplorer.common.gui.drawer.DrawerLayout/android.widget.ListView/android.widget.RelativeLayout[5]")
    el2.click()
    # tool.save_page_and_path_info(2, 'click', [0, 1315, 788, 1462])
    el3 = driver.find_element_by_xpath(
        "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/pl.solidexplorer.common.gui.drawer.DrawerLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.GridView/android.widget.RelativeLayout[1]")
    el3.click()
    # tool.save_page_and_path_info(8, 'click', [0, 431, 360, 791])
    el4 = driver.find_element_by_id("pl.solidexplorer2:id/button2")
    el4.click()
    # tool.save_page_and_path_info(8, 'click', [530, 1678, 802, 1773])
    el5 = driver.find_element_by_id("pl.solidexplorer2:id/btn_play")
    el5.click()
    # tool.save_page_and_path_info(8, 'click', [629, 1452, 755, 1578])
    driver.back()
    # tool.save_page_and_path_info(2, 'back')
    el6 = driver.find_element_by_xpath(
        "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/pl.solidexplorer.common.gui.drawer.DrawerLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.GridView/android.widget.RelativeLayout[3]/android.widget.ImageView")
    el6.click()
    # tool.save_page_and_path_info(8, 'click', [21, 1383, 339, 1567])
    el7 = driver.find_element_by_id("pl.solidexplorer2:id/button2")
    el7.click()
    # tool.save_page_and_path_info(8, 'click', [530, 1678, 802, 1773])
    driver.back()
    # tool.save_page_and_path_info(8, 'back')
    el8 = driver.find_element_by_id("pl.solidexplorer2:id/action_overflow")
    el8.click()
    # tool.save_page_and_path_info(0, 'click', [954, 63, 1080, 210])
    el9 = driver.find_element_by_xpath(
        "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[3]/android.widget.LinearLayout")
    el9.click()
    # tool.save_page_and_path_info(0, 'click', [534, 315, 996, 441])


desired_caps = {
    "platformName": "Android",
    "platformVersion": "9.0",
    "deviceName": "Pixel 2 API 29",
    "appPackage": "pl.solidexplorer2",
    "appActivity": "pl.solidexplorer.SolidExplorer"
}

import time


# from executor.appium_driver.AppiumScriptDriver import AppiumScriptDriver
#
# driver = AppiumScriptDriver.build(desired_caps)

def run(driver):
    # skip_introduction(driver)
    # driver.close_app()
    for fun in [skip_introduction, fun1, fun2, fun3]:
        # driver.launch_app()
        # time.sleep(2)
        fun(driver)
        # driver.close_app()


if __name__ == '__main__':

    from executor.appium_driver.AppiumScriptDriver import AppiumScriptDriver

    # driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    driver = AppiumScriptDriver.build(desired_caps)

    driver.close_app()
    for fun in [skip_introduction, fun1, fun2, fun3]:
        driver.launch_app()
        time.sleep(2)
        fun(driver)
        driver.close_app()
    driver.save_result('../result')
