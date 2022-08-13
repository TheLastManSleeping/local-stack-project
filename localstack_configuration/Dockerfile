FROM python:3.8

WORKDIR /usr/app

COPY lambda_utils.py ./
COPY services_utils.py ./
COPY run_scripts.py ./
COPY lambda/s3_lambda.zip ./
COPY lambda/sqs_lambda.zip ./
RUN pip install boto3

CMD ["python", "./run_scripts.py"]