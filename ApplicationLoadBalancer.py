import boto3

REGION = 'ap-northeast-2'
VPC_ID = 'vpc-0f22c13329dc40837'

ec2 = boto3.client('ec2', region_name=REGION)  # Use client instead of resource for describe_subnets
elbv2 = boto3.client('elbv2', region_name=REGION)

def get_subnet_ids():
    response = ec2.describe_subnets(
        Filters=[
            {'Name': 'vpc-id', 'Values': [VPC_ID]},  # Filter by VPC ID
            {'Name': 'availability-zone', 'Values': ['ap-northeast-2a', 'ap-northeast-2b']}  # Corrected quote
        ]
    )
    
    subnet_ids = [subnet['SubnetId'] for subnet in response['Subnets']]
    
    if len(subnet_ids) < 2:
        raise ValueError("At least two subnets are required in the specified availability zones.")
    
    return subnet_ids

subnet_ids = get_subnet_ids()
print("Subnet IDs:", subnet_ids)

# Creating security groups
def create_security_group():
    response = ec2.create_security_group(
        GroupName='PiyushALBSecurityGroup',
        Description='Security group for Piyush ALB',
        VpcId=VPC_ID  # Added a comma here
    )
    security_group_id = response['GroupId']

    ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 80,
                'ToPort': 80,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]  # Corrected 'cidrIp' to 'CidrIp'
            }
        ]
    )
    return security_group_id

# Attach target group
def create_target_group():
    response = elbv2.create_target_group(
        Name='PiyushTargetGroup',
        Protocol='HTTP',
        Port=80,
        VpcId=VPC_ID,  # Removed quotes from VPC_ID to use the variable
        HealthCheckProtocol='HTTP',
        HealthCheckPath='/',
        HealthCheckIntervalSeconds=30,
        HealthCheckTimeoutSeconds=5,
        HealthyThresholdCount=5,  # Corrected 'Thresold' to 'Threshold'
        UnhealthyThresholdCount=2  # Corrected 'Thresold' to 'Threshold'
    )
    return response['TargetGroups'][0]['TargetGroupArn']  # Corrected 'reponse' to 'response'

# Creating Load balancer
def create_load_balancer(subnet_ids, security_group_id):
    response = elbv2.create_load_balancer(
        Name='PiyushALB',  # Added a name for the load balancer
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
    load_balancer_arn = create_load_balancer(subnet_ids, security_group_id)  # Corrected to include security_group_id
    print("Load Balancer created with ARN:", load_balancer_arn)
