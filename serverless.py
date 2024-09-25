import boto3
import os

REGION = 'ap-northeast-2'
bucket_name = 'piyush-serverless-bucket'

s3 = boto3.client('s3', region_name = REGION)

# function to create boto3
def create_bucket(bucket_name):
    try:
        res = s3.create_bucket(Bucket = bucket_name, CreateBucketConfiguration = {'LocationConstraint': REGION})
        print("Bucket created:", res)
        return res
    except Exception as e:
        print("Error creating bucket:", e)

create_bucket(bucket_name)

