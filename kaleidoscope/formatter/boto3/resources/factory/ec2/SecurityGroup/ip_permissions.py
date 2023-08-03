#- TODO - get the partial defined at the end of this module to be able to be defined in
#-        configuration files, including references to kwargs

import functools

def _format_ip_permissions(ip_permissions, source, ec2_rs):
    """
    Description:
        formats the ip_permissions, ip_permissions_egress attributes of boto3 resource
        SecurityGroup objects
    Input:
        ip_permissions: the ip_permissions we are rendering
        source: source object whose ip_permissions* attrs this method is rendering
        ec2_rs: a dict whose values are the boto3 ec2 resource objects to use to lookup info
            these should use the region name as the dictionary key
    Output:
        list of lines of text to use as the attribute rendering
    """
    import cush
    #- create the table of EC2 implementors to access AWS when we render
    c = cush.CushApplication('default')
    ec2_rs = c._ns.get_leaf_nodes(".implementor.boto3.aws.ec2.resource")
    ec2_rs_t = { ec2_r.meta.client.meta.region_name: ec2_r for ec2_r in ec2_rs }

    output = list()
    for rule in ip_permissions:
        output.append('Protocol: {}'.format(rule['IpProtocol']))
        if 'FromPort' in rule.keys():
            output.append('Ports: {}..{}'.format(rule['FromPort'], rule['ToPort']))
        output.append('IpRanges:')
        if 'IpRanges' in rule.keys() and rule['IpRanges']:
            for ip_range in rule['IpRanges']:
                output.append('    {}'.format(ip_range['CidrIp']))
        if 'Ipv6Ranges' in rule.keys() and rule['Ipv6Ranges']:
            for ipv6_range in rule['Ipv6Ranges']:
                output.append('    {}'.format(ipv6_range))
        if 'UserIdGroupPairs' in rule.keys() and rule['UserIdGroupPairs']:
            for pair in rule['UserIdGroupPairs']:
                if pair['GroupId'] == source.group_id\
                    and pair['UserId'] == source.owner_id:

                    output.append('Security Group Id: self')

                else:
                    #- the SG referenced isn't this one, but lets get a name
                    region = source.meta.client.meta.region_name
                    referenced_sg = ec2_rs[region].security_groups.filter(GroupIds=pair['GroupId'])

                    output.append('Security Group Id: {} | UserId: {}'.format(pair['GroupId'], pair['UserId']))

        output.append('---------')
    return output

ec2_rs_t = dict()
format_ip_permissions = functools.partial(_format_ip_permissions, ec2_rs=ec2_rs_t)
