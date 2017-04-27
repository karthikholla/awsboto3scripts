#Script to check whether CloudTrail is ENABLED or not across all the regions
import boto3
region_list = ['eu-west-1', 'eu-central-1', 'us-east-1', 'us-west-1', 'us-west-2', 'ap-southeast-1', 'ap-southeast-2',
               'ap-northeast-1', 'sa-east-1']
#def lambda_handler(event, context):
for region in region_list:
    cloudtrail = boto3.client('cloudtrail',region_name=region)
    response = cloudtrail.describe_trails(includeShadowTrails=True)
    #print(str(response)+"\n")
    if len(response['trailList']):
        print("CloudTrail is ENABLED"+ " - " + str(region))
    else:
        print("CloudTrail is NOT ENABLED"+ " - " + str(region))