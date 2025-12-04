from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from time import sleep




default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 11, 23),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='respaldo_incremental',
    default_args=default_args,
    schedule_interval='0 19 * * *',
    catchup=False,
    tags=['datos', 'banco']
) as dag:

    backup_task = BashOperator(
        task_id="backup_task",
        bash_command="""
        export PGPASSWORD="1234"
        pg_basebackup -h postgres \
                      -U dani \
                      -D /var/lib/postgresql/backups/incremental/wal/base_backup_$(date +%Y%m%d_%H%M%S) \
                      -F tar \
                      -z \
                      -P \
                      -X stream
        """,
    )

    switch_wal = PostgresOperator(
        task_id="switch_wal",
        postgres_conn_id='postgres_financial',
        sql="SELECT pg_switch_wal();",
    )


    end_worflow = DummyOperator(
        task_id="end_worflow",
    )


switch_wal >> backup_task >> end_worflow  