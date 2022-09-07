from aws_cdk.aws_s3_deployment import Source


def json_data_example():
    return [
            Source.json_data('/year=2022/month=08/01.json', { "id": "20220801" })
    ]


def flat_and_one_common_key():
    return [
            Source.json_data(f'/{i}.json', { "id": str(i), f"key{i}": str(i) })
            for i in range(0, 30)
    ]
