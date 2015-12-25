__author__ = 'gambit'


import datetime
import time
import smtplib
import os

class FileCreator():

    @classmethod
    def create_s3_file(cls, bucket_name, s3_user, access_key, secret_key):
        filename = bucket_name + "_" + s3_user + ".txt"
        header = "###### YOUR S3 BUCKET DETAILS ######"

        f = open(filename, 'a')
        f.write(header + "\n" + "\n" + "\n")

        bucket = "S3 Bucket: %s" % bucket_name
        username = "S3 Username: %s" % s3_user
        access_key_id = "Access Key Id: %s" % access_key
        aws_secret_access_key = "Aws Secret Access Key: %s" % secret_key

        # #Write S3 details to file

        f.write(bucket + "\n" + "\n")
        f.write(username + "\n" + "\n")
        f.write(access_key_id + "\n" + "\n")
        f.write(aws_secret_access_key + "\n" + "\n")
        f.close()

        filepath = os.getcwd()+"/"+filename
        return filepath