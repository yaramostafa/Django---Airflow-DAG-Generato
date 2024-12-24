import os
import sys
import django

# Set up the correct Django settings module path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simulator_project.settings")

# Add the project directory to the system path so Django can find the project
sys.path.append('D:/airflow/simulator_project')

# Initialize Django
django.setup()

# Import models from the simulator app
from simulator.models import Simulator

# Fetch all Simulator objects
simulators = Simulator.objects.all()
print(simulators)
