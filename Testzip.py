__author__ = 'Jones'
import zipfile
import readCongfig
import os
from common.Log import MyLog
import glob


log = MyLog.get_log()
logger = log.get_logger()

report_path = log.get_result_path()
zip_path = os.path.join(readCongfig.proDir, 'result', 'test.zip')
# set zip file
try:
    files = glob.glob(report_path)
    f = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
    for file in files:
        f.write(file, os.path.basename(file))
        logger.info(os.path.basename(file))
        # , '/report/'+os.path.basename(file)
    f.close()
except Exception as ex:
    print(ex)