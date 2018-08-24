# coding=utf-8
__author__ = 'Jones'
import unittest
from appium import webdriver
import time
import os


class LoginAndroidTest(unittest.TestCase):
    def setUp(self):
        print("Start Test...")
        desired_caps = {
            'platformName': 'Android',
            'deviceName': '127.0.0.1:62001',
            'platformVersion': '4.4.2',
            'appPackage': 'com.operations.winsky.operationalanaly',
            'appActivity': '.ui.activity.StartbootActivity',
            }
        self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)
        time.sleep(3)

    def tearDown(self):
        self.driver.quit()
        print("End Test...")

    def getSize(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return x, y

    def swipeLeft(self, t):
        l = self.getSize()
        x1 = int(l[0]*0.75)
        y1 = int(l[1]*0.5)
        x2 = int(l[0]*0.5)
        self.driver.swipe(x1, y1, x2, y1, t)

    def logCat(self):
        cmd_c = 'adb logcat -c'
        os.popen(cmd_c)
        for i in range(30):
            try:
                cmd_d = 'adb logcat -d | findstr codeString'
                value = os.popen(cmd_d).read()
                code = value.split(u'验证码')[1].split(',')[0]
                print(value)
                break
            except:
                pass
            time.sleep(1)
        else:
            raise ValueError
        return code

    def test_login(self):
        self.driver.find_element_by_id("com.operations.winsky.operationalanaly:id/login_zhanhao_et").clear()
        self.driver.find_element_by_id("com.operations.winsky.operationalanaly:id/login_zhanhao_et").send_keys("jiangyunsheng")
        self.driver.find_element_by_id("com.operations.winsky.operationalanaly:id/login_passworld_et").clear()
        self.driver.find_element_by_id("com.operations.winsky.operationalanaly:id/login_passworld_et").send_keys("yszh789")
        self.driver.find_element_by_class_name("android.widget.Button").click()
        time.sleep(2)

    def test_logout(self):
        self.driver.find_element_by_class_name()

if __name__ == '__main__':
    login = LoginAndroidTest()
    login.setUp()
    login.test_login()
    login.tearDown()
