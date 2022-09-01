import os
from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_s3 as s3,
    aws_s3_deployment as s3_deploy,
    aws_glue as glue,
)
from constructs import Construct

class GlueCrawlerExperiment(Construct):

    def __init__(self, scope: Construct, construct_id: str, prefix: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self, "GlueCrawlerExperimentJsonBucket")

        s3_deploy.BucketDeployment(self, "GlueCrawlerExperimentBucketDeploy",
                destination_bucket=bucket,
                destination_key_prefix=f"{prefix}/",
                sources=[s3_deploy.Source.asset(os.path.join(os.path.dirname(__file__), prefix))]
        )

        role = iam.Role(self, "GlueCrawlerExperimentRole",
                assumed_by=iam.ServicePrincipal("glue.amazonaws.com"),
        )

        role.add_managed_policy(
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSGlueServiceRole")
        )
        role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=[f"{bucket.bucket_arn}/*"],
            actions=["s3:GetObject", "s3:PutObject", "s3:ListBucket"],
            )
        )

        crawler = glue.CfnCrawler(self, construct_id,
                role=role.role_name,
                targets=glue.CfnCrawler.TargetsProperty(
                    s3_targets=[glue.CfnCrawler.S3TargetProperty(
                        path=f"s3://{bucket.bucket_name}/{prefix}/",
                        )
                    ],
                ),
                database_name=f"glue_crawler_experiment_{'_'.join(prefix.split('-'))}",
                tags={"glue-crawler-experiment": prefix},
        )


class GlueCrawlerExampleStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        GlueCrawlerExperiment(self, "Data", "data")
        GlueCrawlerExperiment(self, "NonHive", "non-hive")
        GlueCrawlerExperiment(self, "NonEmptyCommon", "non-empty-common")
