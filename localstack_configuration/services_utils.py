import boto3


def get_client(service):
    """Creating clients"""

    return boto3.client(service,
                        endpoint_url='http://ls:4583',
                        aws_access_key_id='dummy',
                        aws_secret_access_key='dummy',
                        region_name='us-east-1',
                        )


def get_resource(service):
    """Creating resources"""
    return boto3.resource(service,
                          endpoint_url='http://ls:4583',
                          aws_access_key_id='dummy',
                          aws_secret_access_key='dummy',
                          region_name='us-east-1')


def create_table(table_name, attribute_type):
    """Creating dynamodb tables"""

    get_client("dynamodb").create_table(
        TableName=table_name,
        KeySchema=[
            {
                "AttributeName": "id",
                "KeyType": "HASH",
            },
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "id",
                "AttributeType": attribute_type,
            },
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 1,
            "WriteCapacityUnits": 1
        }
    )


