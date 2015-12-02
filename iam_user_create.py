__author__ = 'gambit'
import credentials
import boto
from boto.iam.connection import IAMConnection
from boto.s3.key import Key
import datetime
import time
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP

bucket_name = raw_input("Enter Your Bucket Name: ")
S3_User = raw_input("Enter The S3 Username: ")
password = raw_input("Enter Your Email Password")

class IAM_actions(object):

    def createUser(aws_access_key_id,aws_secret_access_key):
        connect = IAMConnection(aws_access_key_id, aws_secret_access_key)
        user = connect.get_all_users()
        # # print user
        users = user['list_users_response']['list_users_result']['users']

        for user1 in users:
        #     print user1
            try:
                if S3_User not in user1['user_name']:
                    new_user = connect.create_user(S3_User)
                    print new_user
                break
            except:
               print " User Already Exist"
               break


    def attachPolicy(self):
        policy = '''{
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": [
                        "s3:ListAllMyBuckets"
                    ],
                    "Effect": "Allow",
                    "Resource": "arn:aws:s3:::*"
                },
                {
                    "Action": "s3:*",
                    "Effect": "Allow",
                    "Resource": [
                        "arn:aws:s3:::%s*",
                        "arn:aws:s3:::%s*/*"
                    ]
                }
            ]
         }''' % (bucket_name, bucket_name)

        # # Attach Policy to acces s3 bucket

        connect.put_user_policy(S3_User, bucket_name, policy)
        key = connect.create_access_key(S3_User)

        # print key


        access_key = key['create_access_key_response'][u'create_access_key_result'][u'access_key'][u'access_key_id']
        secret_key = key['create_access_key_response'][u'create_access_key_result'][u'access_key'][u'secret_access_key']


        # # print access_key
        # # print secret_key

        bucket = "S3 Bucket: %s" % bucket_name
        Username = "S3 Username: %s" % S3_User
        access_key_id = "Acess Key Id: %s" % access_key
        aws_secret_access_key = "Aws Secret Acces Key: %s" % secret_key