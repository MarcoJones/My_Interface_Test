__author__ = 'Administrator'
import os
import codecs
import ConfigParser as configparser

global proDir
proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir, "config.ini")


class ReadConfig:

    def __init__(self):
        fd = open(configPath)
        data = fd.read()
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(configPath, "w")
            file.write(data)
            file.close()
        fd.close()

        self.cf = configparser.ConfigParser()
        self.cf.read(configPath)

    def get_email(self, name):
        value = self.cf.get("EMAIL", name)
        return value

    def get_db(self, name):
        value = self.cf.get("DATABASE", name)
        return value

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_url(self, name):
        value = self.cf.get("URL", name)
        return value

    def get_header(self, name):
        value = self.cf.get("HEADERS", name)
        return value

    def set_header(self, name, value):
        self.cf.set("HEADERS", name, value)
        with open(configPath, 'w+') as f:
            self.cf.write(f)

if __name__ == '__main__':
    rc = ReadConfig()
    print proDir
    print configPath
    print rc.get_email("mail_host")
    print rc.get_http("baseurl")
    #print rc.get_headers("token_V")
