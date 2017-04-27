import boto3
import logging
from datetime import *

logger = logging.getLogger()
logger.setLevel(logging.WARNING)

region_list = ['eu-west-1', 'eu-central-1', 'us-east-1', 'us-west-1', 'us-west-2', 'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1', 'sa-east-1']
#def lambda_handler(event, context):
for region in region_list:
    ec2 = boto3.resource('ec2', region_name=region)
    sns = boto3.resource('sns')
    platform_endpoint = sns.PlatformEndpoint('arn:aws:sns:us-east-1:691693565742:Karthik_SNS_Test')
    today = datetime.now().date()
    volumes = ec2.volumes.all()
    missingReport = "The Following Volumes are not attached to any instances: \n"
    x = 0
    for vol in volumes:
        if vol.state == "available":
            missingReport = missingReport + "- " + str(vol.id) + " - (GiG) " + str(vol.size) + " -  " + str(vol.create_time) + " -  " + str(vol.availability_zone) + " -  " + str(vol.volume_type) + "\n"
            x= x + 1
    if x == 0:
        print("Nothing to Report")
    else:
        response = platform_endpoint.publish(
        Message=missingReport,
        Subject='EBS Volumes that are Not-In-Use: ' + str(today),
        MessageStructure='string',)
        print(missingReport)
