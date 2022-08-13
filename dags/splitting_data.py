import glob
import os
from datetime import datetime, timedelta
import pandas as pd

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


def split_data(**kwargs):
    """Splitting data by month via pandas"""

    files = glob.glob('/usr/local/airflow/data/raw_data/*.csv')
    if files:
        data = pd.read_csv(files[0], delimiter=',', date_parser='departure')
        os.remove(files[0])
        data['departure'] = pd.to_datetime(data['departure'])
        d = data.groupby(pd.Grouper(key='departure', freq='M'))
        for x, group in d:
            if not group.empty:
                group.to_csv(f'/usr/local/airflow/data/split_data/{x.month}-{x.year}.txt')


dag = DAG("splitting_dag", default_args=default_args, schedule_interval="*/30 * * * *", catchup=False)

t0 = PythonOperator(task_id='splitting_task', python_callable=split_data, dag=dag)

t0




