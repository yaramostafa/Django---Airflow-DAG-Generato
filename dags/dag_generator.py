from airflow.decorators import dag, task
from datetime import timedelta, datetime
import requests
import pytz
import random
import os
import sys
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simulator_project.settings")
sys.path.append('D:/airflow/simulator_project')
django.setup()

# Fetch all simulator data
def get_simulator_data():
    """
    This function fetches simulator data from the database.
    """
    from simulator.models import Simulator  
    simulators = Simulator.objects.all()  
    return simulators


# This function dynamically creates the DAGs
def create_dag(simulator):
    default_args = {
        "owner": "airflow",
        "depends_on_past": False,
        "start_date": simulator.start_date.astimezone(pytz.utc) if simulator.start_date else datetime(2025, 1, 1),
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    }

    @dag(
        dag_id=f"simulator_{simulator.id}",
        default_args=default_args,
        schedule=simulator.interval, 
        catchup=False,
    )
    def simulator_dag():
        @task()
        def send_kpi_value_to_django():
            """
            This function simulates sending a random KPI value to a Django endpoint.
            """
            kpi_id = simulator.kpi_id
            value = random.randint(1, 100) 
            url = "http://host.docker.internal:8080/calculate-kpi/" 
            data = {"kpi_id": kpi_id, "value": value}
            response = requests.post(url, json=data)
            print(f"Response: {response.json()}")

        send_kpi_value_to_django()

    return simulator_dag()


# Dynamically register all DAGs based on data fetched from the Django ORM
try:
    simulators = get_simulator_data()
    for simulator in simulators:
        globals()[f"simulator_{simulator.id}"] = create_dag(simulator)
except Exception as e:
    print(f"Failed to load simulator DAGs: {e}")
