from typing import Optional
from aws_cdk import (
    Stack,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_route53 as route53,
    aws_certificatemanager as certificatemanager,
)
from constructs import Construct


class ApiServiceStack(Stack):
    def __init__(
            self,
            scope: Construct,
            id: str,
            enviroment_variables: dict,
            hosted_zone: route53.IHostedZone,
            domain_name: str,
            certificate: certificatemanager.Certificate,
            container_name: str,
            cluster: ecs.Cluster,
            image: ecs.ContainerImage,              # container image
            cpu: Optional[int] = None,
            memory_limit_mib: Optional[int] = None  # memory_limit_mib
        ) -> None:
        super().__init__(
            scope=scope,
            id=id,
            description='ECS Fargate service with autoscaling and a LB accesible from internet.'
        )

        # Container name should not have to have '.'
        container_name = container_name.replace('.', '_')

        ecs_patterns.ApplicationLoadBalancedFargateService(self,
            id=f'api-service',
            cluster=cluster,            # Required               
            desired_count=1,            # Default is 1
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=image,
                environment=enviroment_variables,
                container_name=container_name,
            ),
            domain_name=domain_name,
            domain_zone=hosted_zone,
            certificate=certificate,
            cpu=cpu,                            # Default is 256
            memory_limit_mib=memory_limit_mib,  # Default 512
            redirect_http=True,
            # In order to solve this: https://stackoverflow.com/questions/67301268/aws-fargate-resourceinitializationerror-unable-to-pull-secrets-or-registry-auth
            # I'll put this:
            assign_public_ip=True,
            public_load_balancer=True,
        )
