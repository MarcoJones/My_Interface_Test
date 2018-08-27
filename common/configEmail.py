__author__ = 'Jones'
# coding:utf-8

import os
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
from Log import MyLog
import readCongfig
import zipfile
import glob

localReadConfig = readCongfig.ReadConfig()


class Email:
    def __init__(self):
        global host, user, passwd, port, sender, title
        host = localReadConfig.get_email("mail_host")
        user = localReadConfig.get_email("mail_user")
        passwd = localReadConfig.get_email("mail_pass")
        sender = localReadConfig.get_email("sender")
        port = localReadConfig.get_email("mail_port")
        title = localReadConfig.get_email("subject")

        # get receiver list
        self.value = localReadConfig.get_email("receivers")
        self.receiver = []
        for n in str(self.value).split('/'):
            self.receiver.append(n)

        # defined email subject
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.subject = "Interface test report" + " " + date

        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        self.msg = MIMEMultipart('related')

    def config_header(self):
        """
        set email header include subject,sender,receiver
        :return:
        """
        self.msg['subject'] = self.subject
        self.msg['From'] = sender
        self.msg['To'] = ";".join(self.receiver)

    def config_content(self):
        """
        set email content
        :return:
        """
        fp = open(os.path.join(readCongfig.proDir, 'testfile', 'emailStyle.txt'))
        content = fp.read()
        fp.close()
        content_plain = MIMEText(content, 'html', 'utf-8')
        self.msg.attach(content_plain)

    def config_image(self):
        """
        set email picture
        :return:
        """
        # Add picture in email content
        image1_path = os.path.join(readCongfig.proDir, 'testfile', '1.jpg')
        fp1 = open(image1_path, 'rb')
        msgImage1 = MIMEImage(fp1.read())
        msgImage1.add_header('Content-ID', '<image1>')
        self.msg.attach(msgImage1)

        image2_path = os.path.join(readCongfig.proDir, 'testfile', '2.png')
        fp2 = open(image2_path, 'rb')
        msgImage2 = MIMEImage(fp2.read())
        msgImage2.add_header('Content-ID', '<image2>')
        self.msg.attach(msgImage2)

    def config_file(self):
        """
        config email file
        :return:
        """
        if self.check_file():
            try:
                report_path = self.log.get_result_path()
                zip_path = os.path.join(readCongfig.proDir, 'result', 'test.zip')
                self.logger.info("report path:"+report_path)
                # set zip file
                files = glob.glob(report_path+'\*')
                self.logger.info(files)
                f = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
                for file in files:
                    self.logger.info(os.path.basename(file))
                    f.write(file, '/report/'+os.path.basename(file))
                f.close()
            except Exception as ex:
                print(ex)
            # Add zip file in email
            report_path = open(zip_path, 'rb').read()
            email_file = MIMEText(report_path, "base64", "utf-8")
            email_file['Content-Type'] = 'application/octet-stream'
            email_file['Content-Disposition'] = 'attachment; filename="test.zip"'
            self.msg.attach(email_file)

    def check_file(self):
        """
        check report file is exist
        :return:
        """
        report_path = self.log.get_result_path()
        if os.path.isdir(report_path) and not os.stat(report_path) == 0:
            return True
        else:
            return False

    def test(self):
        return host, user, passwd, sender, title, port, self.value

    def send_email(self):
        """
        send email
        :return:
        """
        self.config_header()
        self.config_content()
        self.config_file()
        try:
            smtp = smtplib.SMTP()
            smtp.connect(host)
            smtp.login(user, passwd)
            smtp.sendmail(sender, self.receiver, self.msg.as_string())
            smtp.quit()
            self.logger.info("This is my first email test report.")
        except Exception as ex:
            self.logger.error(str(ex))


class MyEmail:
    email = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_email():
        if MyEmail.email is None:
            MyEmail.mutex.acquire()
            MyEmail.email = Email()
            MyEmail.mutex.release()
        return MyEmail.email.send_email()

if __name__ == '__main__':
    email = MyEmail.get_email()