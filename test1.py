# -*- coding:utf8 -*-
import time
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
# appium 配置信息

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '11.0'
desired_caps['deviceName'] = 'Pixel 2 API 30'
desired_caps['noReset'] = True
desired_caps["unicodeKeyboard"] = True
desired_caps["resetKeyboard"] = True
desired_caps['appPackage'] = 'com.michaldabski.filemanager'
desired_caps['appActivity'] = '.folders.FolderActivity'

def fun0(driver):
    el = driver.find_elements_by_class_name("android.widget.RelativeLayout")[4]
    TouchAction(driver).long_press(el).perform()

def fun1(driver):
    # test case1: 启动webdriver执⾏行行测试脚本
    # driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

    # test case2: 文件浏览
    el = driver.find_elements_by_class_name("android.widget.RelativeLayout")[4]
    el.click()
    time.sleep(1)

    el = driver.find_elements_by_class_name("android.widget.RelativeLayout")[0]
    el.click()

    el = driver.find_element_by_id("com.michaldabski.filemanager:id/menu_navigate_up")
    el.click()

def fun2(driver):
    # test case3: 查看文件属性
    el = driver.find_elements_by_class_name("android.widget.RelativeLayout")[1]
    TouchAction(driver).long_press(el).perform()
    # el.long_press()

    el = driver.find_element_by_accessibility_id("More options")
    el.click()

    el = driver.find_elements_by_class_name("android.widget.LinearLayout")[5]
    el.click()

    el = driver.find_element_by_id("android:id/button1")
    el.click()

    el = driver.find_element_by_id("android:id/action_mode_close_button")
    el.click()

def fun3(driver):
    # test case4: 文件重命名
    el = driver.find_elements_by_class_name("android.widget.RelativeLayout")[1]
    TouchAction(driver).long_press(el).perform()
    time.sleep(1)

    el = driver.find_element_by_accessibility_id("More options")
    el.click()
    time.sleep(1)

    el = driver.find_elements_by_class_name("android.widget.LinearLayout")[5]
    el.click()
    time.sleep(1)

    driver.press_keycode(8)

    el = driver.find_element_by_id("android:id/button1")
    el.click()
    time.sleep(1)

def fun4(driver):
    # test case5: 文件复制粘贴
    el = driver.find_elements_by_class_name("android.widget.RelativeLayout")[1]
    TouchAction(driver).long_press(el).perform()
    time.sleep(1)

    el = driver.find_element_by_accessibility_id("More options")
    el.click()
    time.sleep(1)

    el = driver.find_elements_by_class_name("android.widget.LinearLayout")[3]
    el.click()
    time.sleep(1)

    el = driver.find_elements_by_class_name("android.widget.RelativeLayout")[0]
    el.click()
    time.sleep(1)

    el = driver.find_element_by_accessibility_id("More options")
    el.click()
    time.sleep(1)

    el = driver.find_elements_by_class_name("android.widget.LinearLayout")[3]
    el.click()
    time.sleep(3)

def fun5(driver):
    # test case6: 文件删除
    el = driver.find_elements_by_class_name("android.widget.RelativeLayout")[1]
    # TouchAction(driver).long_press(el).perform()
    el.tap_hold()
    time.sleep(1)

    el = driver.find_element_by_accessibility_id("Delete")
    el.click()
    time.sleep(1)

    el = driver.find_element_by_id("android:id/button1")
    el.click()
    time.sleep(3)

def run(driver):
    #fun0(driver)
    fun1(driver)
    fun2(driver)
    #driver.quit()
