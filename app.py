#!/usr/bin/env python3
import os

import aws_cdk as cdk

from glue_crawler_example.glue_crawler_example_stack import GlueCrawlerExampleStack


app = cdk.App()
GlueCrawlerExampleStack(app, "GlueCrawlerExampleStack", prefix="data")
GlueCrawlerExampleStack(app, "GlueCrawlerExampleStackNonHive", prefix="non-hive")

app.synth()
