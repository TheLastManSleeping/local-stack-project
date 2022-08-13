from services_utils import create_table, get_client, get_resource
from lambda_utils import deploy_lambda, create_s3_trigger, create_sqs_trigger

# creating s3 bucket and lambda with trigger
get_client("s3").create_bucket(Bucket='data-bucket')
deploy_lambda('s3_lambda')
create_s3_trigger()

# creating sqs queue and lambda layers with trigger
get_resource('sqs').create_queue(QueueName='queue')
deploy_lambda('sqs_lambda')
create_sqs_trigger()

# creating dynamodb tables
create_table('raw_data', "N")
create_table('daily_data', "S")
create_table('monthly_data', "S")
