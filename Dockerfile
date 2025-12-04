FROM python:3.10-slim
USER root
RUN pip install apache-airflow
RUN pip install apache-airflow-providers-postgres 
