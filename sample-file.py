#!/usr/bin/env python3

import shortuuid
import boto3
from botocore.exceptions import ClientError
import string
import random
import os

def upload_this(fileid):
    s3 = boto3.client('s3')
    bucket = 's3-linecount'
    try:
        response = s3.upload_file(fileid, bucket, fileid)
        print("Upload complete:",fileid)
    except ClientError as e:
        print("Error!:", e)
        return False
    return True
    
def random_file():
    fileid = shortuuid.uuid()
    f = open(fileid,"w+")
    lines = random.randint(1200,3000)
    letters = string.ascii_letters
    for i in range(lines):
        f.write(''.join(random.choice(letters) for i in range(10)))
        f.write('\n')
    f.close()
    upload_this(fileid)
    z = os.remove(fileid)

if __name__ == '__main__':
    random_file()
