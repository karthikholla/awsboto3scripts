import boto3
client = boto3.client('ec2')
in_use_groups = []
to_delete_groups = []
all_groups = [group['GroupName'] for group in client.describe_security_groups()['SecurityGroups']]
all_instances = client.describe_instances()

for instances in all_instances['Reservations']:
  for inst in instances['Instances']:
    for group in inst['SecurityGroups']:
      groupName = group['GroupName']
      if groupName not in in_use_groups:
        in_use_groups.append(groupName)

delete_candidates = [item for item in all_groups if item not in in_use_groups]
print(delete_candidates)
print("We will now delete security groups.")
for group in to_delete_groups:
    client.delete_security_group(GroupName = group)
print("We have deleted %d groups." % (len(to_delete_groups)))
