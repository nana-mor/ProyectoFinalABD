CREATE USER airflow WITH PASSWORD 'airflow';
CREATE DATABASE db_airflow OWNER airflow;
GRANT ALL PRIVILEGES ON DATABASE db_airflow TO airflow;