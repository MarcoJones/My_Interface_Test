__author__ = 'Jones'
# coding=utf-8
import os
from xlrd import open_workbook
from xml.etree import ElementTree as ET
from Log import MyLog as Log
import configHttp
import readCongfig
import requests
import json


localReadConfig = readCongfig.ReadConfig()
log = Log.get_log()
logger = log.get_logger()
localConfigHttp = configHttp.ConfigHttp()
proDir = readCongfig.proDir

caseNo = 0


def get_visitor_token():
    """
    create a token for visitor
    :return:
    """
    host = localReadConfig.get_http("BASEURL")
    response = requests.get(host + "#/login")
    info = response.json()
    token = info.get("info")
    logger.debug("Create token:%s" % (token))
    return token


def set_visitor_token_to_config():
    """
    set token that created for visitor to config
    :return:
    """
    token_v = get_visitor_token()
    localReadConfig.set_headers("TOKEN_V", token_v)


def get_value_from_return_json(json, name1, name2):
    """
    get value from return json
    :param json:
    :param name1:
    :param name2:
    :return:
    """
    info = json["info"]
    group = info[name1]
    value = group[name2]
    return value


def show_return_message(response):
    """
    show message details
    :param response:
    :return:
    """
    url = response.url
    msg = response.text
    print("Request address:"+url)
    print("Return number:"+json.dumps(json.loads(msg), ensure_ascii=False, sort_keys=True, indent=4))


def get_xls(xls_name, sheet_name):
    cls = []
    # get xls file's path
    xlspath = os.path.join(readCongfig.proDir, "testfile\\adminCase\\", xls_name)
    # open xls file
    files = open_workbook(xlspath)
    # get sheet by name
    sheet = files.sheet_by_name(sheet_name)
    # get one sheet's rows
    nrows = sheet.nrows
    for i in range(nrows):
        if sheet.row_values(i)[0] != u'case_name':
            cls.append(sheet.row_values(i))
    return cls

# get sql from xml
database = {}


def set_xml():
    if len(database) == 0:
        sql_path = os.path.join(readCongfig.proDir, "testFile", "SQL.xml")
        tree = ET.parse(sql_path)
        for db in tree.findall("database"):
            db_name = db.get("name")
            table = {}
            for tb in db.getchildren():
                table_name = tb.get("name")
                sql = {}
                for data in tb.getchaildren():
                    sql_id = data.get("id")
                    sql[sql_id] = data.text
                table[table_name] = sql
            database[db_name] = table


def get_xml_dict(database_name, table_name):
    set_xml()
    database_dict = database.get(database_name).get(table_name)
    return database_dict


def get_sql(database_name, table_name, sql_id):
    db = get_xml_dict(database_name, table_name)
    sql = db.get(sql_id)
    return sql


def get_url_from_xml(name):
    """
    By name get url from interfaceURL.xml
    :param name:
    :return:
    """
    url_list = []
    url_path = os.path.join(proDir, 'testFile', 'interfaceURL.xml')
    tree = ET.parse(url_path)
    for u in tree.findall('url'):
        url_name = u.get('name')
        if url_name == name:
            for c in u.getchildren():
                url_list.append(c.text)

    url = '/dist/'+'#'+'/'.join(url_list)
    return url

if __name__ == '__main__':
    case = get_xls("loginCase.xls", "login")
    print case[0][2]



