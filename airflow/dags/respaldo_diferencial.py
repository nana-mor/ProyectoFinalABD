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
    dag_id='respaldo_diferencial',
    default_args=default_args,
    schedule_interval='0 * * * *',
    catchup=False,
    tags=['datos', 'banco']
) as dag:

    backup_task = BashOperator(
        task_id="backup_pg",
        
        bash_command="""
        export PGPASSWORD="1234"
        psql -h postgres -U dani -d financial -c "\copy (SELECT * FROM trans WHERE date::DATE >= '2025-11-15') TO '/var/lib/postgresql/backups/diferencial/tabla_diff_{{ ds }}.csv' WITH CSV HEADER"
        """,
    )

