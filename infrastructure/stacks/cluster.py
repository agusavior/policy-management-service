from typing import List, Optional, Tuple
from aws_cdk import (
    Stack,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling,
    Duration,
)
from constructs import Construct

ON_DEMAND = None

class ClusterStack(Stack):
    def __init__(
            self,
            scope: Construct,
            id: str,
            vpc: ec2.IVpc,                                             # vpc
            instances: List[Tuple[str, Optional[str]]],                # instance types, for instance [('c5.12xlarge', ON_DEMAND), ('c5.9xlarge', '0.13'), ... ]
            capacity_providers: List[Tuple[str, Optional[str], int]],  # list of ('c5.12xlarge', spot_price, max_capacity)
        ) -> None:
        super().__init__(
            scope=scope,
            id=id,
            description='ECS Cluster.'
        )

        self.cluster = ecs.Cluster(self, f'cluster', vpc=vpc)
        
        self.capacity_providers = []
        index = 0
        for instance_type, spot_price, max_capacity in capacity_providers:
            auto_scaling_group = autoscaling.AutoScalingGroup(
                self,
                id=f'asg{index}',
                vpc=vpc,
                instance_type=ec2.InstanceType(instance_type_identifier=instance_type),
                machine_image=ecs.EcsOptimizedImage.amazon_linux2(),
                min_capacity=1,
                max_capacity=max_capacity,
                spot_price=spot_price,
                cooldown=Duration.minutes(5),
            )

            capacity_provider = ecs.AsgCapacityProvider(self,
                f'asg-capacity-provider{index}',
                auto_scaling_group=auto_scaling_group,
                capacity_provider_name=f'asg-capacity-provider{index}',
                # https://github.com/aws/aws-cdk/issues/14732
                enable_managed_termination_protection=False,
            )
            self.cluster.add_asg_capacity_provider(capacity_provider)

            self.capacity_providers.append(capacity_provider)

            index += 1

        for index, instance in enumerate(instances):
            instance_type_id, spot_price = instance
            instance_type = ec2.InstanceType(instance_type_identifier=instance_type_id)
            # Each 'add_capacity' creates an AutoScalingGroup
            self.cluster.add_capacity(f'capacity{index}',
                instance_type=instance_type,
                spot_price=spot_price,
                max_capacity=3, # of the AutoScalingGroup created
            )
