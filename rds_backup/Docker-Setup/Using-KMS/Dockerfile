FROM centos:7
RUN yum install epel-release -y 
RUN yum update -y && yum install python3 -y && yum install -y python3-pip && yum install -y python3-setuptools && yum install -y mysql 
RUN pip3 install oss2 && pip3 install sh
COPY rdsbackup_prod_KMS.py rdsdecrypt_prod_KMS.py /opt/
