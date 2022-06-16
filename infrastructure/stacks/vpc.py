from typing import Optional
from aws_cdk import (
    Stack,
    Environment,
    aws_ec2 as ec2,
)
from constructs import Construct

# Availability Zone
MAX_AZS = 3

class VpcStack(Stack):
    def __init__(
            self,
            scope: Construct,
            id: str,
            account: str,
            region: str,
            use_default: bool,  # Use default VPC or create a new one.
        ) -> None:
        super().__init__(
            scope,
            id=id,
            description='Stack that holds the VPCs.',
            env=Environment(account=account, region=region),
        )

        if use_default:
            self.vpc = ec2.Vpc.from_lookup(self, 'default-vpc', is_default= True)
        else:
            self.vpc = ec2.Vpc(self, f'{id}-vpc', max_azs=MAX_AZS)     
