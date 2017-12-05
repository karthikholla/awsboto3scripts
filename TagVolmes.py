# This script finds EC2 instances and append tags on attached EBS volumes to match across all regions

import boto3
region_list = ['eu-west-1', 'eu-central-1', 'us-east-1', 'us-west-1', 'us-west-2', 'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1', 'sa-east-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-south-1']
def lambda_handler(event, context):
    for region in region_list:
        print ('REGION:', region)
        ec2 = boto3.resource('ec2', region)
        for instance in ec2.instances.all():
            if not instance.tags:
                print(instance.id + " has no tags")
            else:
                try:
                    ec2tags = [tag['Value'] for tag in instance.tags if tag['Key'] == 'Name' or tag['Key'] == 'name' ][0]
                except IndexError:
                    print("IndexError: list index out of range " + instance.id)
                    break
                for volume in instance.volumes.all():
                    for vol in volume.attachments:
                        if str(vol['Device']) == '/dev/sda1' or str(vol['Device']) == '/dev/xvda':
                            if not volume.tags:
                                volume.create_tags(DryRun=False, Tags=[{'Key': 'Name','Value': str(ec2tags) + "-root"},])
                                print("*****Created***** " + volume.id)
                            else:
                                print("Already exists " + volume.id)
                        else:
                            print("Cannot create tags for Non-root device " + volume.id)
