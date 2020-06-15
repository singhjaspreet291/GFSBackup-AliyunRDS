## Backup Utility for Docker/Container Setup##

------------
### Ease for taking automated Aliyun RDS Encrypted Backup and Pushing to OSS using Grandfather-father-son Strategy ###
Grandfather-father-son backup is a common rotation scheme for backup media, in which there are three or more backup cycles, such as daily, weekly and monthly.

##### Build the docker image with below command
docker build -t <image_name>:<version> .

### Provide Configuration properties in base64 ecrypted format during runtime of docker as environment variables###
docker run -itd  -e RDS_ENDPOINT="bm9vbnN0YWdlLssXMxLm15c3FsLmR1YmFpLnJkcy5hbGl5dW5jcy5jb20=" -e RDS_USERNAME="cm9vdA==" -e RDS_PASSWORD="VHM3YlY1adexeaVJ3VkRWQldxeHB2ZUc=" -e USER_ACCESS_ID="TFRBSTRGd2hvxeSFVzVmZxMTY4RDRLelZk" -e USER_ACCESS_KEY="OGRlUnYza0dERGxwaWsxwwTkpqWUh1a211cldCQUZO" -e OSS_ENDPOINT="b3NzLW1lLWVxw6hc3QtMS5hbGl5dW5jcy5jb20=" -e OSS_BUCKET="bXlzcWxwwtcmRzYmFja3VwLW5vb25zdGFnZS1zMQ==" -e PARAPHRASE="U3gqxwWjhd" <image_name>:<version>

##### Parameter blocks in Script###
1. Database Configuration (database_config)
1.  Object Storage Service (oss_config)
1.  Encryption Paraphrase (paraphrase)

##### How to take backup###
python3 rdsbackup_common.py hourly
or
python3 rdsbackup_common.py weekly
or
python3 rdsbackup_common.py monthly

##### How to restore dump###
python3 Decrypt.py


## Note: This script will create the directory structure as below and user has to run the script using cronjob for hourly, monthly & weekly basis.
1. hourly --> 2019-11-06 --> DB_NAME --> hourly.sql.gz.enc file
2. weekly --> Nov-19 --> Week Number --> DB_NAME --> date.sql.gz.enc file
3. monthly --> 2019 --> November --> DB_NAME --> date..sql.gz.enc file




