import os
import boto3
from botocore.exceptions import ClientError
from chalice import Chalice

app = Chalice(app_name='s3-linecount')
app.debug = True

S3_BUCKET = os.environ.get('BUCKET_NAME')

# capture data into dynamo
dynamodb = boto3.resource('dynamodb')
TABLE = os.environ.get('TABLE')
def insert_item(fileid, count):
    table = dynamodb.Table(TABLE)
    try:
        response = table.put_item(
           Item={
                'fileid': fileid,
                'lines': count
            }
        )
    except ClientError as e:
        print("Error!:", e)  

# grab the bucket and key and line count for each file
@app.on_s3_event(bucket=S3_BUCKET, events=['s3:ObjectCreated:*'])
def s3_handler(event):
    app.log.debug("Received event for bucket: %s, key: %s",event.bucket, event.key)
    cd = os.chdir('/tmp')
    bucket = event.bucket
    fileid = event.key
    s3 = boto3.client('s3')
    try:
        s3.download_file(bucket, fileid, fileid)
    except ClientError as e:
        print("Error!:", e)
    count = len(open(fileid).readlines())
    print(count)
    insert_item(fileid, count)

