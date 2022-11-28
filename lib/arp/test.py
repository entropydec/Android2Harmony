# -*- coding:utf8 -*-
import time
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
# appium 配置信息

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '11.0'
desired_caps['deviceName'] = 'Pixel 2 API 30'
desired_caps['noReset'] = True
desired_caps["unicodeKeyboard"] = True
desired_caps["resetKeyboard"] = True
desired_caps['appPackage'] = 'com.example.helloworld'
desired_caps['appActivity'] = 'com.example.helloworld.MainActivity'

def run(driver):
    time.sleep(3)
    el1 = driver.find_element_by_id("com.example.helloworld:id/Jump")
    el1.click()

if __name__ == '__main__':
    from executor.appium_driver.AppiumScriptDriver import AppiumScriptDriver
    # driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    driver = AppiumScriptDriver.build(desired_caps)
    driver.close_app()
    driver.save_result('../result')