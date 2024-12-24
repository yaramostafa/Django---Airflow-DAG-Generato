
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta, datetime
import requests

def send_kpi_value_to_django():
    kpi_id = 2  
    value = 84  # Random value for this simulator
    url = 'http://host.docker.internal:8080/calculate-kpi/'  # Django Calc API endpoint
    data = {
        'kpi_id': kpi_id,
        'value': value
    }
    response = requests.post(url, json=data)
    print(f"Response: {response.json()}")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': '2024-12-23 22:31:32+00:00',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='simulator_6',
    default_args=default_args,
    schedule_interval='@once',
    catchup=False
)

task = PythonOperator(
    task_id='send_kpi_value_to_django',
    python_callable=send_kpi_value_to_django,
    dag=dag,
)
