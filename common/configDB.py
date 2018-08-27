from requests import ConnectionError

__author__ = 'Jones'
# _*_ coding:utf-8 _*_
import readCongfig
from Log import MyLog
import pymysql

localReadConfig = readCongfig.ReadConfig()


class MyDB:
    global host, username, password, port, database, config
    host = localReadConfig.get_db("host")
    username = localReadConfig.get_db("username")
    password = localReadConfig.get_db("password")
    port = localReadConfig.get_db("port")
    database = localReadConfig.get_db("database")
    config = {
        'host': str(host),
        'user': username,
        'passwd': password,
        'port': int(port),
        'db': database
    }

    def __init__(self):
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        self.db = None
        self.cursor = None

    def connectDB(self):
        try:
            self.db = pymysql.connect(**config)
            self.cursor = self.db.cursor()
            print("Connect DB successfully!")
        except ConnectionError as ex:
            self.logger.error(str(ex))

    def executeSQL(self, sql, params=None):
        self.connectDB()
        self.cursor.execute(sql, params)
        self.db.commit()
        return self.cursor

    def get_all(self, cursor):
        value = cursor.fetchall()
        return value

    def get_one(self, cursor):
        value = cursor.fetchone()
        if value > 0:
            return value
        else:
            return None

    def closeDB(self):
        if self.db != None:
            self.db.close()
            print("Database closed!")


if __name__ == '__main__':
    Group = "1EAE9A643A824D2F992CD39661ED058E"
    sql = "SELECT * FROM cloud_stakegroup_netmode WHERE stakeGroup='1EAE9A643A824D2F992CD39661ED058E'"
    cursor = MyDB().executeSQL(sql,)
    value = MyDB().get_all(cursor)
    print value
    MyDB().closeDB()


#