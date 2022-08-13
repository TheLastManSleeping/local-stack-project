import glob
import os
from datetime import datetime, timedelta

import boto3
from pyspark.sql import SparkSession
import pyspark.sql.functions as ps
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2015, 6, 1),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "provide_context": True,
}


def get_path(**kwargs):
    """
    Getting file and changing it to .csv

    Changing file to .csv helps to prevent processing file more than once
    """

    file = glob.glob('/usr/local/airflow/data/split_data/*.txt')[0]
    new_file = os.path.splitext(file)[0] + ".csv"
    os.rename(file, new_file)
    ti = kwargs["ti"]
    ti.xcom_push("path", new_file)


def load_data(**kwargs):
    """Loading files to s3"""
    file = kwargs["ti"].xcom_pull(task_ids="process_data", key="processed_path")
    if file is None:
        file = kwargs["ti"].xcom_pull(task_ids="path_task", key="path")
    print(file)
    s3 = boto3.client("s3",
                      endpoint_url='http://ls:4583',
                      aws_access_key_id='dummy',
                      aws_secret_access_key='dummy',
                      region_name='us-east-1',
                      )
    s3.upload_file(
        Filename=file,
        Bucket="data-bucket",
        Key=os.path.basename(file),
    )


def process_data(**kwargs):
    """
    Processing files with pyspark

    This function reads csv, processes and merges data and saves it to .txt.
    In the end, it passes path to .txt file to xcom.
    """

    file = kwargs["ti"].xcom_pull(task_ids="path_task", key="path")
    spark = SparkSession.builder.appName("task").getOrCreate()
    data = spark.read.csv(file, header=True)
    departure_data = data.groupBy("departure_name").agg(ps.count("*").alias("departured"))
    return_data = data.groupBy("return_name").agg(ps.count("*").alias("returned"))
    processed_data = departure_data.join(return_data, departure_data.departure_name == return_data.return_name, 'inner')
    new_file = f'/usr/local/airflow/data/processed_data/{os.path.splitext(os.path.basename(file))[0]}.txt'
    processed_data.select(ps.col("departure_name").alias("station"), 'departured', 'returned')\
        .toPandas().to_csv(new_file)
    ti = kwargs["ti"]
    ti.xcom_push("processed_path", new_file)
    print(new_file)
    file = kwargs["ti"].xcom_pull(task_ids="process_data", key="processed_path")
    print(file)


dag = DAG("s3_dag", default_args=default_args, schedule_interval="*/30 * * * *", catchup=False)

t0 = PythonOperator(task_id='path_task', python_callable=get_path, dag=dag)
t1 = PythonOperator(task_id='load_raw_data', python_callable=load_data, dag=dag)
t2 = PythonOperator(task_id='process_data', python_callable=process_data, dag=dag)
t3 = PythonOperator(task_id='load_processed_data', python_callable=load_data, dag=dag)

t0 >> t1 >> t2 >> t3
