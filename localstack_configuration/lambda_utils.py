from services_utils import get_client


def deploy_lambda(function_name):
    """
    Deploying lambda form .zip

    Also works with lambda layers!
    """

    with open(f'{function_name}.zip', 'rb') as f:
        zipped_code = f.read()
    get_client('lambda').create_function(
        FunctionName=function_name,
        Runtime='python3.8',
        Role='role',
        Handler=function_name + '.handler',
        Code={'ZipFile': zipped_code},
        Timeout=200,
        Environment={
            "Variables": {
                "STAGE": "TESTING"
            }
        }
    )


def create_s3_trigger():
    """Creating s3 trigger"""

    get_client("s3").put_bucket_notification_configuration(Bucket='data-bucket', NotificationConfiguration={
        "LambdaFunctionConfigurations": [
            {
                "Id": "s3eventtggerslambda",
                "LambdaFunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:s3_lambda",
                "Events": ["s3:ObjectCreated:*"]
            }
        ]
    })


def create_sqs_trigger():
    """Creating sqs trigger"""

    get_client('lambda').create_event_source_mapping(
        EventSourceArn='arn:aws:sqs:us-east-1:000000000000:queue',
        FunctionName='sqs_lambda',
        Enabled=True,

    )


