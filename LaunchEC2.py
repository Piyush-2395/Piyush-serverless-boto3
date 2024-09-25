import boto3

REGION = 'ap-northeast-2'
KEY_NAME = 'Piyush_key'  # Make sure this key pair exists in your AWS region

ec2 = boto3.resource('ec2', region_name=REGION)

def create_ec2_instance():
    instance = ec2.create_instances(
        ImageId='ami-05d2438ca66594916',  # Make sure this AMI ID is valid in your region
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        KeyName=KEY_NAME,  # Use the variable without quotes
        TagSpecifications=[
            { 
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': 'PiyushWebServer'}]
            }
        ],
        UserData='''#!/bin/bash
                    sudo apt update -y
                    sudo apt install nginx -y
                    service nginx start
                    mkdir -p /var/www/uploads
                '''
    )
    instance[0].wait_until_running()
    instance[0].reload()
    print("EC2 instance created:", instance[0].id)
    return instance[0]

create_ec2_instance()
