import os
import time
import datetime
import oss2
import CustomEncDyc as enc
import base64
import sys
from shutil import rmtree

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
password_enc = os.getenv("PARAPHRASE")
password= str(base64.b64decode(password_enc))
password=password[2:]
password=password[:-1]

list1= os.system("mysql -h %s -u %s -p%s -e 'SHOW DATABASES' > list" % (db_config['host'],db_config['user'],key))
print("mysql -h %s -u %s -p%s -e 'SHOW DATABASES' > list" % (db_config['host'],db_config['user'],key))
myNames=[]
filters=['Database','mysql','sys','performance_schema','information_schema']
with open('list', 'r') as f:
    for line in f:
        myNames.append(line.strip())
print(myNames)
db_name=[]
for names in myNames:
    if names not in filters:
        db_name.append(names)
print(db_name)
AccessKeyId = os.getenv("USER_ACCESS_ID")
AccessKeyId= str(base64.b64decode(AccessKeyId))
AccessKeyId=AccessKeyId[2:]
AccessKeyId=AccessKeyId[:-1]
AccessKeySecret = os.getenv("USER_ACCESS_KEY")
AccessKeySecret= str(base64.b64decode(AccessKeySecret))
AccessKeySecret=AccessKeySecret[2:]
AccessKeySecret=AccessKeySecret[:-1]
auth = oss2. Auth(AccessKeyId, AccessKeySecret)
bucketEndpoint= os.getenv("OSS_ENDPOINT")
bucketEndpoint= str(base64.b64decode(bucketEndpoint))
bucketEndpoint=bucketEndpoint[2:]
bucketEndpoint=bucketEndpoint[:-1]
bucketName= os.getenv("OSS_BUCKET")
bucketName= str(base64.b64decode(bucketName))
bucketName=bucketName[2:]
bucketName=bucketName[:-1]
bucket = oss2. Bucket(auth,bucketEndpoint,bucketName)

 
# current date
date_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
 
"""
 Method body
"""
 
 
def create_file(path):
    """
         Create folder function
         :param path: create a file path
    :return:
    """
         # Remove the first space
    path = path.strip()
         # Remove tail \ symbol
    path = path.rstrip("\\")
 
         # Determine if the path exists
    if not os.path.exists(path):
                 #Create a directory if it does not exist
        os.makedirs(path)
        return True
    else:
                 # Do not create if the directory exists
        return False
 
 
def export_backup(address,id):
     # () "call mysqldump -h address -u username -p password database name to be backed up > generated file name"
     os.system("mysqldump -h%s -u%s -p%s %s --set-gtid-purged=OFF |gzip > %s" % (
      db_config['host'], db_config['user'],key,db_name[i], address))
 
 
def delete_zip(folder):
    """
         Delete file function
    """
    rmtree(folder)
    print("Removing " + folder + " from local system")

# Added function to get week of the month
def week_number_of_month(date_value):
     return (date_value.isocalendar()[1] - date_value.replace(day=1).isocalendar()[1] + 1)

 

if sys.argv[1] == 'hourly':
 
# Export database backup
    for i in range(len(db_name)):

        # folder address
        ts = time.gmtime()
        time_list=time.strftime("%Y-%m-%d %H:%M:%S", ts).split(" ")
        mkpath = "./%s/%s" % ('hourly', time_list[0])
        # backup file address
     
 
     
        create_file(mkpath+"/"+db_name[i])
        print(mkpath+"/"+db_name[i])
        print("folder creation completed")
        address = "%s/%s/%s/%s.sql.gz" % ('hourly',time_list[0],db_name[i],time_list[1])
     
        # backup database 
        export_backup(address,i) 
        filename = address
     
        enc.CustomEncDyc.encrypt(enc.CustomEncDyc.getKey(password), filename)
        print('Encryption Done.')
        bucket.put_object_from_file(address+'.enc', address+'.enc')
        print("Uploaded")
        print("Backup database completed: %s" % address)
     
        # Delete documents other than the number of days reserved
     
        print("Delete retention days beyond file completed: %s" % db_name[i])

        delete_zip(sys.argv[1])

    

elif sys.argv[1] == 'weekly':

    for i in range(len(db_name)):
 
        # folder address
        ts = time.gmtime()
        time_list=time.strftime("%Y-%m-%d-%H:%M:%S", ts)
        year=time.strftime("%Y-%m")
        date_given = datetime.datetime.today().date()
        week_number=week_number_of_month(date_given)
        week_folder = ('week-' + str(week_number))
        mkpath = "./%s/%s/%s"  % ('weekly',year,week_folder)
        # backup file address
     
 
     
        create_file(mkpath+"/"+db_name[i])
        print(mkpath+"/"+db_name[i])
        print("folder creation completed")
        address = "%s/%s/%s/%s/%s.sql.gz" % ('weekly',year,week_folder,db_name[i],time_list)
     
        # backup database 
        export_backup(address,i) 
        filename = address
     
        enc.CustomEncDyc.encrypt(enc.CustomEncDyc.getKey(password), filename)
        print('Encryption Done.')
        bucket.put_object_from_file(address+'.enc', address+'.enc')
        print("Uploaded")
        print("Backup database completed: %s" % address)
     
             # Delete documents other than the number of days reserved
     
        print("Delete retention days beyond file completed: %s" % db_name[i]) 

        delete_zip(sys.argv[1])

elif sys.argv[1] == 'monthly':

    for i in range(len(db_name)):
 
        # folder address
        ts = time.gmtime()
        time_list=time.strftime("%Y-%m-%d-%H:%M:%S", ts)
        year=time.strftime("%Y")
        month_name=time.strftime("%B")
        mkpath = "./%s/%s/%s" % ('monthly',year,month_name)
             # backup file address
     
 
     
        create_file(mkpath+"/"+db_name[i])
        print(mkpath+"/"+db_name[i])
        print("folder creation completed")
        address = "%s/%s/%s/%s/%s.sql.gz" % ('monthly',year,month_name,db_name[i],time_list)
     
              # backup database 
        export_backup(address,i) 
        filename = address
     
        enc.CustomEncDyc.encrypt(enc.CustomEncDyc.getKey(password), filename)
        print('Encryption Done.')
        bucket.put_object_from_file(address+'.enc', address+'.enc')
        print("Uploaded")
        print("Backup database completed: %s" % address)
     
          # Delete documents other than the number of days reserved
     
        print("Delete retention days beyond file completed: %s" % db_name[i])
        delete_zip('monthly')

else:        
        print("Please Give Valid Argument like hourly or weekly or monthly.")


