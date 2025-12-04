FROM apache/airflow:2.9.1

USER root

# --- meter snippet aquí ---
RUN apt-get update && \
    apt-get install -y wget gnupg lsb-release apt-transport-https && \
    wget -qO - https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --batch --yes --dearmor -o /usr/share/keyrings/postgres.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/postgres.gpg] http://apt.postgresql.org/pub/repos/apt bookworm-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
    apt-get update && \
    apt-get install -y postgresql-client-18 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# --------------------------

USER airflow