__author__ = 'Jones'
# _*_ coding:utf-8 _*_
import os
import logging
from datetime import datetime
import threading
import readCongfig

localReadConfig = readCongfig.ReadConfig()


class Log:
    def __init__(self):
        global logPath, resultPath, proDir
        proDir = readCongfig.proDir
        resultPath = os.path.join(proDir, "result")
        # create result file if it doesn't exist
        if not os.path.exists(resultPath):
            os.mkdir(resultPath)
        # defined test result file name by localtime
        logPath = os.path.join(resultPath, str(datetime.now().strftime("%Y%m%d%H%M%S")))
        # create test result file if it doesn't exist
        if not os.path.exists(logPath):
            os.mkdir(logPath)
        # defined logger
        self.logger = logging.getLogger()
        # defined log level
        self.logger.setLevel(logging.INFO)

        # defined handler
        handler = logging.FileHandler(os.path.join(logPath, "output.log"))
        # defined formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # defined formatter
        handler.setFormatter(formatter)
        # add handler
        self.logger.addHandler(handler)

    def get_logger(self):
        """
        get logger
        :return:
        """
        return self.logger

    def build_start_line(self, case_no):
        """
        write start line
        :return:
        """
        self.logger.info("---------" + case_no + "START---------")

    def bulid_end_line(self, case_no):
        """
        write end line
        :param case_no:
        :return:
        """
        self.logger.info("---------" + case_no + "END---------")

    def build_case_line(self, case_name, code, msg):
        """
        write test case line
        :param case_name:
        :param code:
        :param msg:
        :return:
        """
        self.logger.info(case_name+' - RequestCode:'+unicode(code)+' - Message:'+unicode(msg))

    def get_result_path(self):
        """
        get result file path
        :return:
        """
        return logPath

    def get_report_path(self):
        """
        get report file path
        :return:
        """
        report_path = os.path.join(logPath, "report.html")
        return report_path

    def write_result(self, result):
        """
        :param result:
        :return:
        """
        result_path = os.path.join(logPath, "report.txt")
        fb = open(result_path, "wb")
        try:
            fb.write(result)
        except IOError as ex:
            logger.error(str(ex))

    # def output(self):
    #     self.logger.error('this is error message')
    #     self.logger.info('this is info message')
    #     self.logger.warn('this is warning message')
    #     self.logger.debug('this is debug message')


class MyLog:
    log = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_log():
        if MyLog.log is None:
            MyLog.mutex.acquire()
            MyLog.log = Log()
            MyLog.mutex.release()
        return MyLog.log

if __name__ == '__main__':
    log = MyLog.get_log()
    logger = log.get_logger()
    logger.error('this is error message')
    logger.warn('this is warn message')
