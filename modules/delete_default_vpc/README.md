"""
delete_default_vpc.py

Finds the default VPC in us-east-1 and deletes:
- Internet Gateways
- Subnets
- Non-default Security Groups
- Non-main Route Tables
- Network ACL entries & associations
- Finally, the VPC itself

Usage:
  pip install boto3
  export AWS_PROFILE=…
  export AWS_DEFAULT_REGION=us-east-1
  python delete_default_vpc.py
"""