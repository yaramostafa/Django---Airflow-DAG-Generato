import os
import random
from django.core.management.base import BaseCommand
from simulator.models import Simulator
import pytz

DAGS_DIR = "D:/airflow/dags"  

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        simulators = Simulator.objects.all()
        for simulator in simulators:
            dag_file = os.path.join(DAGS_DIR, f"simulator_{simulator.id}.py")
            with open(dag_file, 'w') as f:
                f.write(self.generate_dag_content(simulator))
        self.stdout.write(self.style.SUCCESS("DAGs generated successfully!"))

    def generate_dag_content(self, simulator): 
        start_date = simulator.start_date
        # datetime is in UTC
        if start_date.tzinfo is None:
            start_date = start_date.replace(tzinfo=pytz.utc)
        else:
            start_date = start_date.astimezone(pytz.utc)

        print(f"Simulator ID: {simulator.id}, Start Date (UTC): {start_date}")
        # Generate a random value for each simulator
        random_value = random.randint(1, 100) 

        return f"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta, datetime
import requests

def send_kpi_value_to_django():
    kpi_id = {simulator.kpi_id}  
    value = {random_value}  # Random value for this simulator
    url = 'http://host.docker.internal:8080/calculate-kpi/'  # Django Calc API endpoint
    data = {{
        'kpi_id': kpi_id,
        'value': value
    }}
    response = requests.post(url, json=data)
    print(f"Response: {{response.json()}}")

default_args = {{
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': '{simulator.start_date}',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}}

dag = DAG(
    dag_id='simulator_{simulator.id}',
    default_args=default_args,
    schedule_interval='{simulator.interval}',
    catchup=False
)

task = PythonOperator(
    task_id='send_kpi_value_to_django',
    python_callable=send_kpi_value_to_django,
    dag=dag,
)
"""