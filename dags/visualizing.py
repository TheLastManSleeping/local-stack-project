import glob
import os
from datetime import datetime, timedelta

import boto3
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from matplotlib import pyplot as plt

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


def visualize(**kwargs):
    dynamodb = boto3.resource("dynamodb",
                              endpoint_url='http://ls:4583',
                              aws_access_key_id='dummy',
                              aws_secret_access_key='dummy',
                              region_name='us-east-1',
                              )
    titles = ['distance (m)', 'duration (sec.)', 'avg_speed (km/h)', 'Air temperature (degC)']
    data_names = ['daily_data', 'monthly_data']
    for data_name in data_names:
        table = dynamodb.Table(data_name)
        data = table.scan()
        for title in titles:
            groups = []
            counts = []
            for item in data['Items']:
                groups.append(item['id'])
                counts.append(float(item['myAttributes'][title]))
            new_title = " ".join(title.split()[:-1])
            plt.title(new_title)
            plt.bar(groups, counts, edgecolor="k", linewidth=2)
            plt.savefig('/usr/local/airflow/data/visualized_data/' + new_title + '-' + data_name + '.png')


dag = DAG("visualising_dag", default_args=default_args, schedule_interval="*/30 * * * *", catchup=False)

t0 = PythonOperator(task_id='visualizing_task', python_callable=visualize, dag=dag)

t0
