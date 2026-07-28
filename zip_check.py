import boto3
import json
import hashlib
import os
import logging
import sys

print("Script name:", sys.argv[0])
print("Arguments:", sys.argv[:1])

if(len(sys.argv)!=4):
	print("Total arguments:", len(sys.argv))
	sys.exit(1)

logging.getLogger('boto').setLevel(logging.INFO)

s3 = boto3.client('s3')

def check_file(boto3_s3,s3_bucket,s3_path,local_path):
    try:
        file_hash=hashlib.md5(open(local_path,'rb').read()).hexdigest()
    except IOError as e:
        print("An error occurred:", e)
        return False
    s3 = boto3_s3
    response = s3.head_object(
        Bucket=s3_bucket,
        Key=s3_path
    )
    #print(response["ETag"][1:-1])
    print(response['Metadata']['md5'])
    print(file_hash)
    if response['Metadata']['md5']==file_hash:
        return True
    else:
        return False

def download_file(s3,s3_bucket,s3_path,local_path):
    s3.download_file(s3_bucket, s3_path, local_path)

def get_clip(s3,s3_bucket,s3_path,local_path):
    check=check_file(s3,s3_bucket,s3_path,local_path)
    if not check:
        download_file(s3,s3_bucket,s3_path,local_path)
        sys.exit(4)

s3_bucket=sys.argv[1]
s3_path=sys.argv[2]
local_path=sys.argv[3]

get_clip(s3,s3_bucket,s3_path,local_path)
