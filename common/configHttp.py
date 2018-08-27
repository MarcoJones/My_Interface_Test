# coding=utf-8
from urllib3.exceptions import TimeoutError
import readCongfig as RC
import requests
import os
import json
from Log import MyLog as Log

rc = RC.ReadConfig()


class ConfigHttp:
    def __init__(self):
        global host, port, timeout
        host = rc.get_http('baseurl')
        port = rc.get_http('port')
        timeout = int(rc.get_http('timeout'))
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.url = None
        self.header = {}
        self.params = {}
        self.data = {}
        self.file = {}
        self.status = 0

    def set_url(self, url):
        """
        set url
        :param url:
        :return:
        """
        self.url = host+":" + port+url

    def set_header(self, header):
        """
        set header
        :param header:
        :return:
        """
        self.header = header

    def set_params(self, params):
        """
        set params
        :param params:
        :return:
        """
        self.params = params

    def set_data(self, data):
        """
        set data
        :param data:
        :return:
        """
        self.data = data

    def set_file(self, file_name):
        """
        set files
        :param file_name:
        :return:
        """
        # file_path = os.path.join(RC.proDir, file_name)
        # return file_path
        if file_name != '':
            file_path = os.path.join(RC.proDir, file_name)
            self.file = {'file': open(file_path, 'rb')}
        if file_name == '' or file_name is None:
            self.status = 1

    def post(self):
        try:
            response = requests.post(self.url, data=self.data, timeout=timeout, headers=self.header)
            return response
        except TimeoutError:
            self.logger.error("Timer Out!")
            return None

    def get(self):
        try:
            response = requests.get(self.url, params=self.params, headers=self.header)
            return response
        except TimeoutError:
            self.logger.error("Timer Out!")
            return None

if __name__ == '__main__':
    Ch = ConfigHttp()
    Ch.set_url("/admin/login.do")
    data = {'username': 'jiangyunsheng', 'password': 'yszh789'}
    Ch.set_data(data)
    header = rc.get_header("winsky.session.id")
    Ch.set_header(header)
    timeout = 0.5
    response = Ch.post()
    info = json.loads(response.content)
    print info["msg"]