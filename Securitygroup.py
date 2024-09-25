VPC_ID = 'vpc-0f22c13329dc40837'

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
