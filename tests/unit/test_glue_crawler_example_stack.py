import aws_cdk as core
import aws_cdk.assertions as assertions

from glue_crawler_example.glue_crawler_example_stack import GlueCrawlerExampleStack

# example tests. To run these tests, uncomment this file along with the example
# resource in glue_crawler_example/glue_crawler_example_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = GlueCrawlerExampleStack(app, "glue-crawler-example")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
