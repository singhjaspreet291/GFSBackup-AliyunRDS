import os
import time
import datetime
import oss2
import base64
import time
import sys
import pdb
from sh import gunzip
from shutil import rmtree
from oss2.crypto import AliKMSProvider


ts = time.gmtime()
print(time.strftime("%Y-%m-%d %H:%M:%S", ts))
 
ignore = ['.DS_Store']
hostEndpoint = os.getenv("RDS_ENDPOINT")
hostEndpoint= str(base64.b64decode(hostEndpoint))
hostEndpoint=hostEndpoint[2:]
hostEndpoint=hostEndpoint[:-1]
user= os.getenv("RDS_USERNAME")
user= str(base64.b64decode(user))
user=user[2:]
user=user[:-1]

db_config = {
    'host': hostEndpoint,
    'user': user,
    'pwd': "",
}
password_db= os.getenv("RDS_PASSWORD")
key= str(base64.b64decode(password_db))
key=key[2:]
key=key[:-1]

kms_id = os.getenv("KMS_ID")
KmsKey= str(base64.b64decode(kms_id))
KmsKey=KmsKey[2:]
KmsKey=KmsKey[:-1]

kms_region = os.getenv("KMS_REGION")
KmsRegion= str(base64.b64decode(kms_region))
KmsRegion=KmsRegion[2:]
KmsRegion=KmsRegion[:-1]

AccessKeyId = os.getenv("ALIYUN_ACCESS_ID")
AccessKeyId= str(base64.b64decode(AccessKeyId))
AccessKeyId=AccessKeyId[2:]
AccessKeyId=AccessKeyId[:-1]

AccessKeySecret = os.getenv("AlIYUN_ACCESS_KEY")
AccessKeySecret= str(base64.b64decode(AccessKeySecret))
AccessKeySecret=AccessKeySecret[2:]
AccessKeySecret=AccessKeySecret[:-1]

auth = oss2.Auth(AccessKeyId, AccessKeySecret)

bucketEndpoint= os.getenv("BUCKET_ENDPOINT")
bucketEndpoint= str(base64.b64decode(bucketEndpoint))
bucketEndpoint=bucketEndpoint[2:]
bucketEndpoint=bucketEndpoint[:-1]

bucketName= os.getenv("BUCKET_NAME")
bucketName= str(base64.b64decode(bucketName))
bucketName=bucketName[2:]
bucketName=bucketName[:-1]

DbName= os.getenv("DB_NAME")

# KMS method to encrypt the data. This method only applies to scenarios where objects are uploaded or downloaded entirely.
bucket = oss2.CryptoBucket(auth,bucketEndpoint, bucketName,crypto_provider=AliKMSProvider(AccessKeyId, AccessKeySecret, KmsRegion, KmsKey))

# Input path
address = (sys.argv[1])

if os.path.exists("dump.sql.gz"):
# Deleting dump.sql.gz file if present
    os.remove("dump.sql.gz")
    print("Existing dump.sql.gz file Removed!")
else:
# create empty file 
    open("dump.sql.gz","w+")
  
# Download an object to a local file.
bucket.get_object_to_file(address, 'dump.sql.gz')
print("MySQL dump downloaded from OSS & Decrypted and stored in dump.sql.gz file!")

if os.path.exists("dump.sql"):
    os.remove("dump.sql")
    print("Existing dump.sql file Removed!")
    gunzip('dump.sql.gz')
    print("Extracted dump.sql.gz to dump.sql")
    
else:
   gunzip('dump.sql.gz')
   print("Extracted dump.sql.gz to dump.sql")

#Result=os.system("mysql -h %s -u %s -p%s -e 'SHOW DATABASES' | grep %s" % (db_config['host'],db_config['user'],key,DbName))

#if Result == DbName:
#   os.system("mysql -h %s -u %s -p%s %s < dump.sql" % (db_config['host'],db_config['user'],key,DbName))
#   print("Database Restoration done!")

#else:
os.system("mysql -h %s -u %s -p%s -e 'CREATE DATABASE IF NOT EXISTS %s'" % (db_config['host'],db_config['user'],key,DbName))
os.system("mysql -h %s -u %s -p%s %s < dump.sql" % (db_config['host'],db_config['user'],key,DbName))
print("Database Restoration Done Successfully!")
