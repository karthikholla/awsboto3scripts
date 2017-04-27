import boto3
from datetime import datetime
import json

region_list = ['eu-west-1', 'eu-central-1', 'us-east-1', 'us-west-1', 'us-west-2', 'ap-southeast-1', 'ap-southeast-2',
               'ap-northeast-1', 'sa-east-1']
#def lambda_handler(event, context):
for region in region_list:
    ec2 = boto3.resource('ec2', region_name=region)
    sns = boto3.resource('sns')
    platform_endpoint = sns.PlatformEndpoint('arn:aws:sns:us-east-1:691693565742:Karthik_SNS_Test')
    result = " The Following SG's are opened to Public(0.0.0.0/0) on Port 22 & 3389 \n"
    x = 0
    for sg in ec2.security_groups.iterator():
        #print(sg.id)
        #print(sg.ip_permissions)
        for rule in sg.ip_permissions:
            #from_port = rule.get('FromPort')
            if (rule.get('FromPort') == 22) or (rule.get('FromPort') == 3389):
                for ip_range in rule.get('IpRanges'):
                    if ip_range.get('CidrIp') == '0.0.0.0/0':
                        result = result + " - " + str(sg.group_name) + " - " + str(sg.group_id) + " - " + str(sg.vpc_id) + "\n"
                        x= x + 1
    for cloudtrail in boto3.client('cloudtrail', region_name=region).lookup_events() ['Events']:
        for resource in cloudtrail['Resources']:
            if resource['ResourceType'] == 'AWS::EC2::SecurityGroup':
                result2 = (resource['ResourceName'])
if(result == result2):
    print("breached")
