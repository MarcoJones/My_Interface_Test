__author__ = 'Jones'
import common
import configHttp
import readCongfig as RC
import re
from Log import MyLog
import json

localConfigHttp = configHttp.ConfigHttp()
localReadConfig = RC.ReadConfig()
localLogin_xls = common.get_xls("loginCase.xls", "login")
address = str(localLogin_xls[0][2])
log = MyLog.get_log()
logger = log.get_logger()


def setCookies():
    localConfigHttp.set_url(address)
    username = localLogin_xls[0][4]
    password = localLogin_xls[0][5]
    data = {"username": username, "password": password}

    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    localConfigHttp.set_header(header)
    localConfigHttp.set_data(dict(data))
    response = localConfigHttp.post()
    sessionstr = re.findall(r"JSESSIONID=(.+\W)?", response.url)
    Status = response.content
    statusCode = json.loads(Status)['requestCode']
    if statusCode == 0:
        strcookie = str(sessionstr)
        cookie = strcookie[3:-3]
        if cookie != "":
            localReadConfig.set_header('cookie', "winsky.session.id="+cookie)
            return cookie
        else:
            print "Cookie value is null!"
    elif statusCode == 1:
        print("Login Failed!")
    elif statusCode == 2:
        print 'The account has been logged in!'


def logout():
    logout_url = "/admin/logout.do"
    localConfigHttp.set_url(logout_url)
    cookie = localReadConfig.get_header("cookie")
    header = {'Cookie': cookie, 'ContentType': 'text/html;charset=utf-8'}
    localConfigHttp.set_header(header)
    try:
        response = localConfigHttp.get()
        content = response.content
        status = response.status_code
    except Exception as ex:
        print ex
    if (status < 300) and (status >= 200):
        localReadConfig.set_header("cookie", "")
        return status, content
    else:
        print("LogOut Failed!")
        return status

if __name__ == '__main__':
    response = setCookies()
    print response