__author__ = 'Administrator'
# _*_ coding:utf-8 _*_

import unittest
import os
from common.Log import MyLog as Log
import readCongfig
# import HTMLTestRunner
from common import HTMLTestRunnerCN
from common.configEmail import MyEmail


localReadConfig = readCongfig.ReadConfig()


class AllTest():
    def __init__(self):
        global log, logger, resultPath
        log = Log.get_log()
        logger = log.get_logger()
        resultPath = log.get_report_path()
        # on_off = localReadConfig.get_email("on_off")
        self.caseListFile = os.path.join(readCongfig.proDir, "caselist.txt")
        self.caseFile = os.path.join(readCongfig.proDir, "testcase")
        self.caselist = []

    def set_case_list(self):
        """
        set case list
        :return:
        """
        fb = open(self.caseListFile)
        for value in fb.readlines():
            data = str(value)
            if data != '' and not data.startswith("#"):
                self.caselist.append(data.replace("\n", ""))
            # print value
        fb.close()

    def set_case_suite(self):
        """
        set case suite
        :return:
        """
        self.set_case_list()
        test_suite = unittest.TestSuite()
        suite_module = []

        for case in self.caselist:
            case_name = case
            # print case_name+'.py'
            discover = unittest.defaultTestLoader.discover(self.caseFile, pattern=case_name+'.py', top_level_dir=None)
            suite_module.append(discover)

        if len(suite_module) > 0:

            for suite in suite_module:
                for test_name in suite:
                    test_suite.addTest(test_name)
        else:
            return None
        return test_suite

    def run(self):
        """
        run test
        :return:
        """
        global fp
        try:
            fp = open(resultPath, 'wb')
            suite = self.set_case_suite()
            if suite is not None:
                logger.info("*********TEST START***********")
                runner = HTMLTestRunnerCN.HTMLTestRunner(stream=fp, title="Test Report", description="Test Description")
                runner.run(suite)
            else:
                logger.info("Have no case to test")
        except Exception as ex:
            logger.error(str(ex))

        finally:
            MyEmail.get_email()
            logger.info("**********TEST ENDING***********")
            fp.close()


if __name__ == '__main__':
    obj = AllTest()
    obj.run()
