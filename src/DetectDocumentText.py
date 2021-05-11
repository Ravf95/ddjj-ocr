from os import environ
from json import dumps
import boto3

environ["AWS_CONFIG_FILE"] = "../aws/config"
environ["AWS_SHARED_CREDENTIALS_FILE"] = "../aws/credentials"

def process_text_detection(bucket, document):    
    client = boto3.client('textract')

    response = client.detect_document_text(
        Document={'S3Object': {'Bucket': bucket, 'Name': document}})

    return response

def main():
    bucket = 'jpeg-container'
    document = 'ci.jpg'
    response = process_text_detection(bucket, document)

    with open("./block.json", "w") as f:
        f.write(dumps(response))
    
if __name__ == "__main__":
    main()
