# **Localstack project**
_No pain, no gain_

## Introduction

Localstack project is intended to process raw data from [here](https://www.kaggle.com/geometrein/helsinki-city-bikes) and load data to different localstack services.


## Structure

Project is presented by docker-compose app and contains of three containers:

**localstack** - just localstack, yep.

**localstack conf** - container for creating different localstack services like sqs queue, dynamodb tables, etc. Contains ziped code for sqs and s3 lambdas.

**airflow** - just airflow container with java and additional folder for data. Later it will be pushed to dokerhub.
airflow gets 3 additional volumes via docker-compose: 

_data_ - here you can place data for processing.

_requirements_ - requirements for code in dags.

_dags_ - dags, yea. For now, there are 3 dags: 

`splitting_data` - dag for splitting raw data

`s3 `- dag for processing data via pyspark and dumping all data to s3.

`visualizing`- dag for building plots from data in dynamodb.


## How to ...

Project starts with a single `docker compose up` command 

Then you can manage your dags on `localhost:8080`

You can put raw files to `data/raw_data` before booting project or directly to airflow container to `/usr/local/airflow/data/raw_data` after booting 

Right now you can find plots in airflow container at `/usr/local/airflow/data/visualized_data`