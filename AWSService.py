__author__ = 'gambit'


from IdentityAccessManagement import IdentityAccessManagement
from Mailer import Mailer
from FileCreator import FileCreator

# ec2_name = raw_input("Enter your instance name: ")
bucket_name = raw_input("Enter Your Bucket Name: ")
s3_user = raw_input("Enter The S3 Username: ")


iam = IdentityAccessManagement()

status = iam.create_s3_bucket(bucket_name)
if status is False:
    print "Bucket cannot be created or it already exists"
else:
    iam.create_user(s3_user)

user_info = iam.access_key(s3_user)

created_user = user_info[0]
created_access_key = user_info[1]
created_secret_key = user_info[2]

iam.attach_policy(s3_user, bucket_name)

filepath = FileCreator.create_s3_file(bucket_name, created_user, created_access_key, created_secret_key)

body = "Hello there.."
mailer = Mailer("rkapali@lftechnology.com", "Your bucket details", body, filepath, "s3details.txt")
mailer.attach_attachment()
mailer.send_mail()

print "S3 Bucket: %s" % bucket_name
print "S3 Username: %s" % created_user
print "Access Key Id: %s" % created_access_key
print "Aws Secret Access Key: %s" % created_secret_key