# _*_ coding:utf-8 _*_
__author__ = 'Jones'
from common import common
import unittest
import paramunittest
import sys
reload(sys)
from common.configDB import MyDB
from common import configHttp as ConfigHttp
from common.Log import MyLog as Log
import readCongfig
import random
sys.setdefaultencoding('utf-8')

addNetMode_xls = common.get_xls("netMode.xls", "addNetMode")
configHttp = ConfigHttp.ConfigHttp()
localReadConfig = readCongfig.ReadConfig()
info = {}


@paramunittest.parametrized(*addNetMode_xls)
class AddNetMode(unittest.TestCase):
    def setParameters(self, case_name, method, url, token, stakeGroup, stakeId, companyName, companyId, payType, payCycle, validDate, requestCode, msg):
        """
        set parameters
        :param case_name:
        :param method:
        :param url:
        :param stakeGroup:
        :param stakeId:
        :param payType:
        :param payCycle:
        :param validDate:
        :param requestCode:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.url = str(url)
        self.stakeGroup = str(stakeGroup)
        self.stakeId = str(stakeId)
        self.payType = int(payType)
        self.payCycle = int(payCycle)
        self.validDate = str(validDate)
        self.requestCode = int(requestCode)
        self.token = int(token)
        self.msg = msg
        self.account = random.randint(1000000, 9999999)
        self.cardNo = random.randint(1000000, 9999999)
        self.comOperator = random.choice(['Mobile', 'Unicom', 'Telecom'])
        self.netType = 1
        self.companyId = str(companyId)
        self.companyName = companyName

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

    def testAddNetMode(self):
        """
        test body
        :return:
        """
        configHttp.set_url(self.url)
        session = localReadConfig.get_header("cookie")
        header = {"Cookie": str(session), "Content-Type": "application/x-www-form-urlencoded"}
        configHttp.set_header(dict(header))
        data1 = {"account": self.account, "cardNo": self.cardNo, "comOperator": self.comOperator, "netType": self.netType, "payCycle": self.payCycle, "payType": self.payType,
                "stakeGroup": self.stakeGroup, "stakeId": self.stakeId, "companyId": self.companyId, "companyName": self.companyName, "validDate": self.validDate}
        data = dict(data1)
        # print data
        self.logger.info(data)
        configHttp.set_data(data)
        self.return_json = configHttp.post()
        self.logger.info("RequestStatus:"+str(self.return_json.status_code))
        try:
            self.info = self.return_json.text
            print self.info
            self.logger.info("ResponseData:"+self.info)
        except Exception as ex:
            print ex
        print session
        self.checkResult()

    def tearDown(self):
        pass

    def checkResult(self):
        self.info = dict(self.return_json.json())
        requestCode = self.info['requestCode']
        if requestCode == 0:
            account = self.account
            sql = "SELECT account AS account, cardNo AS cardNo,netType AS netType,stakeGroup AS stakeId \
            FROM cloud_stakegroup_netmode \
            WHERE account = %s"
            cursor = MyDB().executeSQL(sql, account)
            val = MyDB().get_all(cursor)
            if self.assertEqual(val[0][0], str(self.account)):
                print(val)
                self.logger.info("Add netMode Successfully!")
                print "Add netMode Successfully!"
        else:
            print "Add netMode failed!"
        MyDB().closeDB()

    def test(self):
        pass

if __name__ == '__main__':
    netMode = AddNetMode()
    netMode.testAddNetMode()