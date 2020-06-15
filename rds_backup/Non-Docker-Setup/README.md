## Backup Utility for Non-Docker Setup##

------------
### Ease for taking automated Aliyun RDS Encrypted Backup and Pushing to OSS using Grandfather-father-son Strategy ###
Grandfather-father-son backup is a common rotation scheme for backup media, in which there are three or more backup cycles, such as daily, weekly and monthly.


### Provide Configuration properties in base64 ecrypted format in database.config file as below
[database_config]
endpoint = cm0tNmdqaXA0c3NkMjA0cDA4MGxjby5teXNxbC5hcC1zb3V0aC0xLnJkcy5hbGl5dW5jcy5jb20=
username = cm9vdA==
password = SGVsbG8xMjMq

[oss_config]
accessid = TFRBSU1sTFZMcHFUYUM5eQ==
accesskey = M1g3eEJnRjgzRmJGbllLamRpbldtOU9qcUFDM2dr
endpoint = b3NzLWFwLXNvdXRoLTEuYWxpeXVuY3MuY29t
bucketname = YnVja2V0MzU1

[enc_config]
paraphrase = YXNkZg==

##### How to take backup
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




