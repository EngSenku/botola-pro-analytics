from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging

default_args = {
    "owner": "data-team",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": False,
}

with DAG(
    dag_id="botola_bi_daily",
    default_args=default_args,
    description="Full Botola Pro BI pipeline",
    schedule_interval="0 6 * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["botola", "football", "bi"],
) as dag:

    ingest_apifootball = BashOperator(
        task_id="ingest_apifootball",
        bash_command="cd /opt/airflow && python ingestion/extract_apifootball.py",
    )

    ingest_sportsdb = BashOperator(
        task_id="ingest_sportsdb",
        bash_command="cd /opt/airflow && python ingestion/extract_sportsdb.py",
    )

    ingest_transfermarkt = BashOperator(
        task_id="ingest_transfermarkt",
        bash_command="cd /opt/airflow && python ingestion/extract_transfermarkt.py",
    )

    ingest_wikipedia = BashOperator(
        task_id="ingest_wikipedia",
        bash_command="cd /opt/airflow && python ingestion/extract_wikipedia.py",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/airflow/transform && dbt run --profiles-dir .",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/airflow/transform && dbt test --profiles-dir .",
    )

    dbt_docs = BashOperator(
        task_id="dbt_docs_generate",
        bash_command="cd /opt/airflow/transform && dbt docs generate --profiles-dir .",
    )

    # parallel ingestion → dbt run → dbt test → docs
    [ingest_apifootball, ingest_sportsdb,
     ingest_transfermarkt, ingest_wikipedia] >> dbt_run >> dbt_test >> dbt_docs
