#!/usr/bin/env python3

import boto3, botocore

ec2    = boto3.resource('ec2')
client = boto3.client('ec2')

def get_default_vpc():
    vpcs = list(ec2.vpcs.filter(Filters=[{'Name':'is-default','Values':['true']}]))
    return vpcs[0] if vpcs else None

def detach_and_delete_igws(vpc):
    for igw in vpc.internet_gateways.all():
        vpc.detach_internet_gateway(InternetGatewayId=igw.id)
        igw.delete()

def delete_subnets(vpc):
    for subnet in vpc.subnets.all():
        subnet.delete()

def delete_non_default_sgs(vpc):
    for sg in vpc.security_groups.all():
        if sg.group_name != 'default':
            try: sg.delete()
            except botocore.exceptions.ClientError: pass

def delete_non_main_route_tables(vpc):
    for rt in vpc.route_tables.all():
        if any(not a.get('Main') for a in rt.associations_attribute):
            try: rt.delete()
            except botocore.exceptions.ClientError: pass

def delete_network_acls(vpc):
    for acl in vpc.network_acls.all():
        if not acl.is_default:
            acl.delete()

def main():
    vpc = get_default_vpc()
    if not vpc:
        print("No default VPC found.")
        return
    print(f"Deleting default VPC {vpc.id}…")
    detach_and_delete_igws(vpc)
    delete_subnets(vpc)
    delete_non_default_sgs(vpc)
    delete_non_main_route_tables(vpc)
    delete_network_acls(vpc)
    client.delete_vpc(VpcId=vpc.id)
    print("Done.")
    
if __name__ == '__main__':
    main()

chmod +x delete_default_vpc.py
