import boto3

region_list = ['eu-west-1', 'eu-central-1', 'us-east-1', 'us-west-1', 'us-west-2', 'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1', 'sa-east-1']
#def lambda_handler(event, context):
for region in region_list:
    ec2 = boto3.resource('ec2', region_name=region)
    sns = boto3.resource('sns')
    platform_endpoint = sns.PlatformEndpoint('arn:aws:sns:us-east-1:691693565742:Karthik_SNS_Test')
    volumes = ec2.volumes.all()
    tagreport = "The Following Volumes have no Tags: \n"
    x = 0
    for vol in volumes:
        if not vol.tags:
            tagreport = tagreport + "- " + str(vol.id) + " - " + str(vol.availability_zone) + "\n"
            x= x + 1
    if x == 0:
        print("Nothing to Report")
    else:
        response = platform_endpoint.publish(
        Message=tagreport,
        Subject='Volumes with No Tags - IaaS Account - All Regions: ',
        MessageStructure='string',)
        print(tagreport)