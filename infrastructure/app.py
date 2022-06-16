#!/usr/bin/env python3
import os
import uuid

import aws_cdk as cdk
from aws_cdk import (
    aws_ecs as ecs,
)
from aws_cdk.aws_secretsmanager import ISecret
from stacks.cluster import ClusterStack, ON_DEMAND

from stacks.api import ApiServiceStack
from stacks.domain import DomainStack
from stacks.vpc import VpcStack

from dotenv import dotenv_values


# Random string in order to have a unique container name.
# If you usa an container name that already exists, the stack will be get stuck in UPDATE_IN_PROGRESS status. ¬_¬
# I think.
RANDOM_STRING = uuid.uuid4().hex[:6]

# =========
# CONSTANTS
# =========

# CDK
CDK_DEFAULT_ACCOUNT = os.environ.get("CDK_DEFAULT_ACCOUNT")
CDK_DEFAULT_REGION = os.environ.get("CDK_DEFAULT_REGION")
assert CDK_DEFAULT_ACCOUNT
assert CDK_DEFAULT_REGION

# Print advise about region
print('We are using CDK_DEFAULT_REGION = ', CDK_DEFAULT_REGION, '. Default VPC will use this region.')

# Domain configuration
DOMAIN_OF_HOSTED_ZONE = 'agusavior.tk'
EXISTING_HOSTED_ZONE_ID = 'Z07771553F2GOV3IGFSSE'   # Put this in None if you want to create one. Else, go to AWS console and get the value.
EXISTING_HOSTED_ZONE_NAME = DOMAIN_OF_HOSTED_ZONE   # Put this in None if you want to create one.
PRODUCTION_PMS_API_SUB_DOMAIN = f'pms.api.{DOMAIN_OF_HOSTED_ZONE}'
SUB_DOMAIN_LIST = [
    PRODUCTION_PMS_API_SUB_DOMAIN,
]

def define_stacks(app: cdk.App):
    # =============
    # Domains Stack
    # =============
    domains_stack = DomainStack(
        app,
        domain_of_hosted_zone=DOMAIN_OF_HOSTED_ZONE,
        sub_domain_list=SUB_DOMAIN_LIST,
        existing_hosted_zone_id=EXISTING_HOSTED_ZONE_ID,
        existing_hosted_zone_name=EXISTING_HOSTED_ZONE_NAME,
    )

    # =========
    # VPC Stack
    # =========
    vpc_stack = VpcStack(
        app,
        id='vpc',
        use_default=True,
        account=CDK_DEFAULT_ACCOUNT,
        region=CDK_DEFAULT_REGION,
    )

    # ============
    # ECS Cluster
    # ============
    cluster_stack = ClusterStack(
        app,
        id='cluster',
        instances=[
            ('t3.micro', None),
        ],
        capacity_providers=[],
        vpc=vpc_stack.vpc,
    )

    # ===========
    # Fargate API
    # ===========
    container_image = ecs.ContainerImage.from_asset(
        directory='../api',
        file='Dockerfile',
    )
    container_name = f'api-{RANDOM_STRING}'
    # TODO: Use secrets!
    enviroment_variables = dict() # dotenv_values('../api/.env')
    ApiServiceStack(
        app,
        id=f'pms-api',     # The name of the Cloudformation stack.
        cluster=cluster_stack.cluster,
        image=container_image,
        hosted_zone=domains_stack.hosted_zone,
        domain_name=PRODUCTION_PMS_API_SUB_DOMAIN,
        certificate=domains_stack.get_certificate_of(PRODUCTION_PMS_API_SUB_DOMAIN),
        enviroment_variables=enviroment_variables,
        container_name=container_name,
        cpu=512,
        memory_limit_mib=1024,
    )

# =======
# CDK APP
# =======
app = cdk.App()
define_stacks(app)
app.synth()
