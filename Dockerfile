# Start with the official Airflow image as the base
FROM apache/airflow:2.10.4

# Install Django and other dependencies
RUN pip install django==5.1.4
