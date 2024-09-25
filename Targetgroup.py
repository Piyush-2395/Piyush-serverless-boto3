import boto3
REGION = 'ap-northeast-2'
VPC_ID = 'vpc-0f22c13329dc40837'

ec2 = boto3.resource('ec2', region_name = REGION)
elbv2 = boto3.client('elbv2', region_name = REGION)

def create_target_group():
    response = elbv2.create_target_group(
        Name='PiyushTargetGroup',
        Protocol = 'HTTP',
        Port=80,
        VpcId = 'VPC_ID',
        HealthCheckProtocol = 'HTTP',
        HealthCheckPath = '/',
        HealthCheckIntervalSeconds= 30,
        HealthCheckTimeoutSeconds= 5,
        HealthyThresoldCount=5,
        UnhealthyThresoldCount =2
        
    )
    return reponse ['TargetGroups'][0]['TargetGroupArn']
