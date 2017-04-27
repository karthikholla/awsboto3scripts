import boto3
#def lambda_handler(event, context):
ec2 = boto3.resource('ec2')
cw = boto3.client('cloudwatch')
sns = 'arn:aws:sns:us-west-1:970612677544:epimetheans'
vpc = ec2.Vpc('vpc-81bb4fe4')
instance_iterator = vpc.instances.all()
for instance in instance_iterator:
    for tag in instance.tags:
        if tag['Key'] == 'Environment' and tag['Value'] == 'production':
            #print('Found instance id: ' + str(instance.id))
            response = cw.put_metric_alarm(
            AlarmName="Status Check Failed for " + str(instance.id) + " / " + str(instance.private_ip_address),
            AlarmDescription='Status Check Failed (Instance & System) for 5 Minutes',
            ActionsEnabled=True,
            AlarmActions=[sns],
            MetricName='StatusCheckFailed',
            Namespace='AWS/EC2',
            Statistic='Average',
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': str(instance.id)
                },
            ],
            Period=60,
            EvaluationPeriods=5,
            Threshold=1.0,
            ComparisonOperator='GreaterThanOrEqualToThreshold'
            )
