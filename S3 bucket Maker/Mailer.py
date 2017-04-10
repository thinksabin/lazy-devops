

import datetime
import time
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP

class Mailer():
   
    smtp_server = ''
    smtp_username = ''
    smtp_password = ''
    smtp_port = '587'

    from_add = "noreply@example.com"

    def __init__(self, receiver, subject, body, filepath, filename):
        self.receiver = receiver
        self.subject = subject
        self.body = body
        self.filepath = filepath
        self.filename = filename
        self.msg = MIMEMultipart('alternative')


    def attach_attachment(self):
        part = MIMEApplication(open(self.filepath , "rb").read())
        part.add_header('Content-Disposition', 'attachment', filename=filename)
        self.msg.attach(part)

    def send_mail(self):
        self.msg['Subject'] = "Your S3 Details"
        self.msg['From'] = self.from_add
        self.msg['To'] = self.receiver
        # text = "Please find the attachment for the s3 bucket details"
        part1 = MIMEText(self.body, 'plain')
        self.msg.attach(part1)
        mail = smtplib.SMTP(host = self.smtp_server, port = self.smtp_port, timeout = 10)
        mail.set_debuglevel(10)
        mail.starttls()
        mail.ehlo()
        mail.login(self.smtp_username,self.smtp_password)
   
        mail.sendmail(self.from_add, self.receiver, self.msg.as_string())
        mail.quit()
