__author__ = 'Jones'
# coding:utf-8
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import Header
from email.mime.text import MIMEText


mail_host = 'smtp.163.com'
mail_user = 'jiangyunshengv5@163.com'
mail_pass = 'ShanSeek877695'


sender = 'jiangyunshengv5@163.com'
receivers = ['jiangyunshengv5@163.com']

msgR = MIMEMultipart('related')
msgR['From'] = Header('Test Engineer',)
msgR['To'] = Header('Jones',)
subject = 'This is my first email!'
msgR['Subject'] = Header(subject, 'utf-8')

msgAlter = MIMEMultipart('alternative')
msgR.attach(msgAlter)

txt = MIMEText('Email Content:Film <Yours Name>Picture', 'plain', 'utf-8')
msgR.attach(txt)

image = open('timg.jpg', 'rb')
msgImage = MIMEImage(image.read())
image.close()
msgR.attach(msgImage)
try:
    smtp = smtplib.SMTP()
    smtp.connect(mail_host)
    smtp.login(mail_user, mail_pass)
    smtp.sendmail(sender, receivers, msgR.as_string())
    smtp.quit()
    print "Send email success!"
except smtplib.SMTPException:
    print "Send email failed!"