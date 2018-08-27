__author__ = 'Jones'
# coding:utf-8
import unittest
import paramunittest
from common.Log import MyLog
from common.configHttp import ConfigHttp
from common import common
from readCongfig import ReadConfig
import requests

localReadconfig = ReadConfig()
msg_list_xls = common.get_xls("msgList.xls", "msglist")
configHttp = ConfigHttp()


@paramunittest.parametrized(*msg_list_xls)
class TestMsgList(unittest.TestCase):
    def __init__(self, case_name, method, url, startTime, endTime, status, evaluate, stakeGroupId, pageNum, pageSize, requestCode, msg):
        """
        Set test data
        :param case_name:
        :param method:
        :param url:
        :param startTime:
        :param endTime:
        :param status:
        :param evaluate:
        :param stakeGroupId:
        :param pageNum:
        :param pageSize:
        :param requestCode:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.url = str(url)
        self.startTime = str(startTime)
        self.endTime = str(endTime)
        self.status = int(status)
        self.evaluate = str(evaluate)
        self.stakeGroupId = str(stakeGroupId)
        self.pageNum = int(pageNum)
        self.pageSize = int(pageSize)
        self.requestCode = int(requestCode)
        self.msg = str(msg)
        self.return_json = None
        self.info = None

    def setUp(self):
        """
        setUp
        :return:
        """
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        self.logger.info(self.case_name+"_Ready")

    def description(self):
        """
        description
        :return:
        """
        self.case_name

    def test_msg_list(self):
        """
        Test body
        :return:
        """
        try:
            configHttp.set_url(self.url)
            session = requests.session()
            headers = {"session": str(session)}
            configHttp.set_header(headers)
            data = {"pageNum": self.pageNum,
                    "pagesize": self.pageSize,
                    "startTime": self.startTime,
                    "endTime": self.endTime,
                    "status": self.status,
                    "evaluate": self.evaluate,
                    "stakeGroup": self.stakeGroupId}
            configHttp.set_data(data)
            self.return_json = configHttp.post()
            cookies = self.return_json.cookies
            self.logger.info(dict(cookies))
            self.info = self.return_json.json()
            print self.info
        except Exception as ex:
            print ex

if __name__ == '__main__':
    TestMsgList.test_msg_list()
