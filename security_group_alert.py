import boto3

ec2 = boto3.client('ec2')
sns = boto3.resource('sns')

def email_service(email_title, email_body):
    platform_endpoint = sns.PlatformEndpoint('arn:aws:sns:us-west-2:XXXX:XXXX')
    response = platform_endpoint.publish(
    Message=email_body,
    Subject=email_title,
    MessageStructure='string',)
    # print(email_body)


def alert_security_group_by_source():
    alert_sources = ['0.0.0.0/0']
    allowed_security_group = []
    allowed_ports = []
    alert_security_group(alert_sources, allowed_security_group, allowed_ports)


def alert_security_group(alert_sources, allowed_security_group, allowed_ports):
    email_title = "Urgent: Security rules with inbound source of " + str(alert_sources) + " detected "
    email_body = "Below are the Security rules with inbound source of " + str(alert_sources) + " detected: " + "\n" + "\n" + "\n"
    groupfound = 0
    security_group_list = ec2.describe_security_groups()
    for security_group in security_group_list['SecurityGroups']:
        for ip_rule in security_group['IpPermissions']:
            try:
                for ip_range in ip_rule['IpRanges']:
                    if (ip_range['CidrIp'] in alert_sources and security_group[
                        'GroupId'] not in allowed_security_group and str(ip_rule['FromPort']) not in allowed_ports):
                        groupfound = 1
                        email_body += "Group Id: " + security_group['GroupId'] + " ||  " +  "Group Name: " + security_group['GroupName'] + " ||  " + "Port Range: " + str(
                            ip_rule['FromPort']) + "\n"
            except Exception as e:
                e

    if (groupfound == 1):
        email_service(email_title, email_body)


# if __name__ == "__main__":
#     alert_security_group_by_source()

def lambda_handler(json_input, context):
    alert_security_group_by_source()
