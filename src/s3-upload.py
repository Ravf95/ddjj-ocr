import boto3
from os import environ

environ["AWS_CONFIG_FILE"] = "../aws/config"
environ["AWS_SHARED_CREDENTIALS_FILE"] = "../aws/credentials"

s3 = boto3.resource('s3')
data = open('./ci.jpg', 'rb')
s3.Bucket('jpeg-container').put_object(Key='ci.jpg', Body=data)
