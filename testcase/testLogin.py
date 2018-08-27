__author__ = 'Jones'
# -*- coding: utf8 -*-
import unittest
import paramunittest
import readCongfig as readCongfig
from common.Log import MyLog as Log
from common import common as common
from common import configHttp as ConfigHttp
import requests
import re
import urllib

login_xls = common.get_xls("loginCase.xls", "login")
localReadConfig = readCongfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
info = {}


@paramunittest.parametrized(*login_xls)
class Login(unittest.TestCase):
    def setParameters(self, case_name, method, url, token, username, password, requestCode, msg):
        """
        set params
        :param case_name:
        :param method:
        :param token:
        :param username:
        :param password:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.username = str(username)
        self.password = str(password)
        self.code = str(requestCode)
        self.url = str(url)
        self.msg = unicode(msg)
        self.return_json = None
        self.info = 0

    def description(self):
        """
        test report description
        :return:
        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.logger.info(self.case_name+"_ready")

    def testLogin(self):
        """
        test body
        :return:
        """
        # set url

        configHttp.set_url(self.url)
        # print("set url:"+self.url)
        session = requests.session()
        # set header
        header = {"session": str(session)}
        configHttp.set_header(header)
        # set param
        data = {"username": self.username, "password": self.password}
        # print type(data)
        configHttp.set_data(data)
        # test interface
        self.return_json = configHttp.post()
        method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        self.logger.info("Request Method:"+method)
        cookies = self.return_json.cookies
        self.logger.info(cookies)
        self.logger.info(dict(cookies))
        # check result
        # print("Get Result:"+method)
        self.info = self.return_json.json()
        # print self.info
        self.checkResult()

    def tearDown(self):
        """
        :return:
        """
        try:
            info = dict(self.info)
            if self.result == 0:
                url2 = self.return_json.url
                sessionstr = re.findall(r"JSESSIONID=(.+\W)?", url2)
                if sessionstr != "":
                    strcookie = str(sessionstr)
                    cookie = strcookie[3:-3]
                    localReadConfig.set_header('cookie', "winsky.session.id="+cookie)
                    print cookie
                else:
                    self.logger.error("Cookie value is null!")
        except ValueError:
            self.logger.error("Get session value failed! ")
        self.log.build_case_line(self.case_name, info['requestCode'], info['msg'])

    def checkResult(self):
        """
        check test result
        :return:
        """
        self.info = self.return_json.json()
        common.show_return_message(self.return_json)
        self.result = self.info['requestCode']
        if self.code == self.result:
            username = common.get_value_from_return_json(self.info, 'data', 'loginName')
            self.logger.error(username)
            print username
            self.assertEqual(self.info['msg'], self.msg, 'Messages is not equal.')
            self.assertEqual(username, self.username, 'Username is not equal')
        elif self.result == 2:
            self.logger.info("Always Login!")
            # print("RequestCode:"+str(self.result))
            # print("RequestMsg:"+str(self.info['msg']))


if __name__ == '__main__':
    login = Login()
    name = login.username
    print name