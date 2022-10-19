import os
from aws_cdk import (
    RemovalPolicy,
    Stack,
    aws_iam as iam,
    aws_s3 as s3,
    aws_s3_deployment as s3_deploy,
    aws_glue as glue,
)
from constructs import Construct

from . import data


class GlueCrawlerExperiment(Construct):

    def __init__(self, scope: Construct, construct_id: str, bucket: s3.IBucket,
                 role: iam.Role, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        if construct_id == 'JsonDataExample':
            dataset = data.JsonDataExample()
        elif construct_id == 'FlatAndOneCommonKey':
            dataset = data.FlatAndOneCommonKey()
        elif construct_id == 'DisjointKeys':
            dataset = data.DisjointKeys()
        elif construct_id == 'NonHiveDisjointKeys':
            dataset = data.NonHiveDisjointKeys()
        elif construct_id == 'OverlappingKeys':
            dataset = data.OverlappingKeys()
        else:
            assert False

        s3_deploy.BucketDeployment(self,
                                   "InputJsonBucketDeployment",
                                   destination_bucket=bucket,
                                   destination_key_prefix=f"{dataset.prefix}/",
                                   retain_on_delete=False,
                                   sources=dataset.sources)

        glue.CfnCrawler(
            self,
            "Crawler",
            role=role.role_name,
            targets=glue.CfnCrawler.TargetsProperty(s3_targets=[
                glue.CfnCrawler.S3TargetProperty(
                    path=f"s3://{bucket.bucket_name}/{dataset.prefix}/", )
            ], ),
            database_name=
            f"glue_crawler_experiment_{'_'.join(dataset.prefix.split('-'))}",
            tags={"glue-crawler-experiment": dataset.prefix},
        )


class GlueCrawlerExampleStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self,
                           "InputJsonBucket",
                           removal_policy=RemovalPolicy.DESTROY,
                           auto_delete_objects=True)

        role = iam.Role(
            self,
            "CrawlerRole",
            assumed_by=iam.ServicePrincipal("glue.amazonaws.com"),
        )

        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSGlueServiceRole"))
        role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                resources=[f"{bucket.bucket_arn}/*"],
                actions=["s3:GetObject", "s3:PutObject", "s3:ListBucket"],
            ))

        GlueCrawlerExperiment(self, "DisjointKeys", bucket, role)
        GlueCrawlerExperiment(self, "NonHiveDisjointKeys", bucket, role)
        GlueCrawlerExperiment(self, "OverlappingKeys", bucket, role)
        GlueCrawlerExperiment(self, "JsonDataExample", bucket, role)
        GlueCrawlerExperiment(self, "FlatAndOneCommonKey", bucket, role)
