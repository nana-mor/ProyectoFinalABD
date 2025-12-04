from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 11, 23),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='respaldo_completo',
    default_args=default_args,
    schedule_interval='0 * * * *',
    catchup=False,
    tags=['datos', 'banco']
) as dag:

    backup_task = BashOperator(
        task_id="backup_pg",
        
        bash_command="""
        export PGPASSWORD="1234"
        pg_dump -h postgres -U dani -d financial \
            > /var/lib/postgresql/backups/completo/{{ ds }}_dump.dump
        """,
    )  

