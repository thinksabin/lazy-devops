__author__ = 'gambit'
import boto
from boto.iam.connection import IAMConnection
from boto.s3.key import Key
import datetime
import time
import smtplib
import os


class IdentityAccessManagement():
    admin_access_key = "AKIAJHURBM3YVB5TORAA"
    admin_secret_key = "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"

    def create_user(self, s3_user):
        connect = IAMConnection(self.admin_access_key, self.admin_secret_key)
        user = connect.get_all_users()

        users = user['list_users_response']['list_users_result']['users']

        for user in users:
            if s3_user in user['user_name']:
                return False

        connect.create_user(s3_user)
        return True

    def access_key(self, s3_user):
        connect = IAMConnection(self.admin_access_key, self.admin_secret_key)
        key = connect.create_access_key(s3_user)
        access_key = key['create_access_key_response'][u'create_access_key_result'][u'access_key'][u'access_key_id']
        secret_key = key['create_access_key_response'][u'create_access_key_result'][u'access_key'][u'secret_access_key']

        return s3_user, access_key, secret_key

    def attach_policy(self, S3_User, bucket_name):
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

        print policy
        # # Attach Policy to acces s3 bucket
        connect = IAMConnection(self.admin_access_key, self.admin_secret_key)
        connect.put_user_policy(S3_User, bucket_name, policy)

    def create_s3_bucket(self, bucket_name):
        s3 = boto.connect_s3(self.admin_access_key, self.admin_secret_key)

        all_bucket = s3.get_all_buckets()
        for bucket in all_bucket:
            name = bucket.name
            if bucket_name not in name:
                s3.create_bucket(bucket_name)
                return True
            else:
                return False

