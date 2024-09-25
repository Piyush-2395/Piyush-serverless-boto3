import boto3

REGION = 'ap-northeast-2'
VPC_ID = 'vpc-0f22c13329dc40837'

ec2 = boto3.client('ec2', region_name=REGION)
elbv2 = boto3.client('elbv2', region_name=REGION)

def get_subnet_ids():
    response = ec2.describe_subnets(
        Filters=[
            {'Name': 'vpc-id', 'Values': [VPC_ID]},
            {'Name': 'availability-zone', 'Values': ['ap-northeast-2a', 'ap-northeast-2b']}
        ]
    )
    
    subnet_ids = [subnet['SubnetId'] for subnet in response['Subnets']]
    
    if len(subnet_ids) < 2:
        raise ValueError("At least two subnets are required in the specified availability zones.")
    
    return subnet_ids

def create_security_group():
    # Check if the security group already exists
    try:
        existing_groups = ec2.describe_security_groups(
            Filters=[
                {'Name': 'group-name', 'Values': ['PiyushALBSecurityGroup']},
                {'Name': 'vpc-id', 'Values': [VPC_ID]}
            ]
        )
        if existing_groups['SecurityGroups']:
            print("Security group already exists, using the existing one.")
            return existing_groups['SecurityGroups'][0]['GroupId']
    except Exception as e:
        print("Error checking existing security groups:", e)

    # Create new security group if it doesn't exist
    response = ec2.create_security_group(
        GroupName='PiyushALBSecurityGroup',
        Description='Security group for Piyush ALB',
        VpcId=VPC_ID
    )
    security_group_id = response['GroupId']

    ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            }
        ]
    )
    return security_group_id

def create_target_group():
    response = elbv2.create_target_group(
        Name='PiyushTargetGroup',
        Protocol='HTTP',
        Port=80,
        VpcId=VPC_ID,
        HealthCheckProtocol='HTTP',
        HealthCheckPath='/',
        HealthCheckIntervalSeconds=30,
        HealthCheckTimeoutSeconds=5,
        HealthyThresholdCount=5,
        UnhealthyThresholdCount=2
    )
    return response['TargetGroups'][0]['TargetGroupArn']

def create_load_balancer(subnet_ids, security_group_id):
    response = elbv2.create_load_balancer(
        Name='PiyushALB',
        Subnets=subnet_ids,
        SecurityGroups=[security_group_id],
        Scheme='internet-facing',
        Tags=[{'Key': 'Name', 'Value': 'PiyushLoadBalancer'}],
        Type='application',
        IpAddressType='ipv4'
    )
    return response['LoadBalancers'][0]['LoadBalancerArn']

if __name__ == "__main__":
    subnet_ids = get_subnet_ids()
    security_group_id = create_security_group()
    load_balancer_arn = create_load_balancer(subnet_ids, security_group_id)
    print("Load Balancer created with ARN:", load_balancer_arn)
