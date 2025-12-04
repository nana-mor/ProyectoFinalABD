from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from datetime import timedelta
import random
# Obtener el id de la transacción
def get_trans_id(cur):
    query = "SELECT MAX(trans_id) from trans" # Verificar el id válido anterior
    cur.execute(query)
    trans_id = cur.fetchone()[0] +1 # Utilizar el id siguiente inmediato
    return trans_id

def get_account_id(cur): # Inserar a partir de un valor de cuenta que ya existe
    
    get_max_account_id = '''select max(account_id) 
    from trans;''' 

    while True:
        cur.execute(get_max_account_id)
        max = cur.fetchone()
        account_id = random.randint(1, max[0])

        query = "select * from trans where account_id = %s;"
        cur.execute(query, (account_id,))

        if cur.fetchall(): # Si tiene registros la devuelve
            return account_id

def get_date():
    return "2025-11-19"

def get_type():
    type_list = ["PRIJEM","VYBER","VYDAJ"]
    type = random.choice(type_list)
    return type

def get_operation():
    operation_list = ["PREVOD NA UCET","PREVOD Z UCTU","VKLAD","VYBER","VYBER KARTOU", None]
    operation = random.choice(operation_list)
    return operation

def get_amount():
    amount = random.randint(0, 10_000)
    return amount

def get_balance():
    balance = random.randint(-6000, 50_000)
    return balance

def get_k_symbol():
    symbol_list = ["",
    "DUCHOD",
    "POJISTNE",
    "SANKC. UROK",
    "SIPO",
    "SLUZBY",
    "UROK",
    "UVER",
    None]
    k_symbol = random.choice(symbol_list)
    return k_symbol

def get_bank():
    bank_list = [
        "AB",
        "CD",
        "EF",
        "GH",
        "IJ",
        "KL",
        "MN",
        "OP",
        "QR",
        "ST",
        "UV",
        "WX",
        "YZ",
        None
    ]
    bank = random.choice(bank_list)
    return bank

def get_account(cur, account_id):
    query_account = '''select max(account) from trans where account_id = %s;'''
    cur.execute(query_account, (account_id,))
    account = cur.fetchone()
    return account[0]

def insert_values(**kwargs):
    conn_id = kwargs.get('postgres_conn_id') 

    if not conn_id:
        raise ValueError("El ID de conexión (postgres_conn_id) no fue proporcionado en op_kwargs.")
        
    hook = PostgresHook(postgres_conn_id=conn_id)
    try:
        with hook.get_conn() as conn:
            with conn.cursor() as cur:
        
                for _ in range (10):
                    
                    trans_id = get_trans_id(cur)
                    account_id = get_account_id(cur)
                    date = get_date()
                    trans_type = get_type()
                    operation = get_operation()
                    amount = get_amount()
                    balance = get_balance()
                    k_symbol = get_k_symbol()
                    bank = get_bank()
                    account = get_account(cur, account_id)

                    query_insert = '''insert into trans (trans_id, account_id, date, type, operation, amount, balance, k_symbol, bank, account) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''    
                    cur.execute(query_insert,(
                        trans_id,
                        account_id,
                        date,
                        trans_type,
                        operation,
                        amount,
                        balance,
                        k_symbol,
                        bank,
                        account
                        ))
                
                conn.commit()

    except Exception as e:
        if 'conn' in locals() and conn:
            conn.rollback() 
        raise e

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 11, 23),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='generador_transacciones_aleatorias',
    default_args=default_args,
    schedule_interval='*/10 * * * *',
    catchup=False,
    tags=['datos', 'banco']
) as dag:
    

    insert_task = PythonOperator(
        task_id='insertar_10_transacciones',
        python_callable=insert_values, 
        op_kwargs={'postgres_conn_id': 'postgres_financial'} 
    )

