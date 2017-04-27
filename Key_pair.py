import boto3

region_list = ['eu-west-1', 'eu-central-1', 'us-east-1', 'us-west-1', 'us-west-2', 'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1', 'sa-east-1']
#def lambda_handler(event, context):
for region in region_list:
    ec2 = boto3.resource('ec2', region_name=region)
    print(id)
