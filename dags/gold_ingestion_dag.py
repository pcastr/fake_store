from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor

from fake_store.gold_data_extract import GoldDataExtract
from fake_store.gold_database import GoldDatabase
from fake_store.gold_insights_ingestion import GoldDataInserter

# Configuração da DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2024, 11, 1),
    "catchup": False,
}


def data_ingestion():
    silver_db_path = "data/silver/fake_store.db"
    gold_db_path = "data/gold/fake_store_gold.db"

    inserter = GoldDataInserter(silver_db_path, gold_db_path)
    inserter.insert_user_cart_insights()


def data_extract():
    db_exporter = GoldDataExtract("data/gold/fake_store_gold.db")
    db_exporter.export_to_csv(
        "user_cart_insights", "data/marts/user_cart_insights.csv"
    )


with DAG(
    "gold_ingestion_dag",
    default_args=default_args,
    description="DAG para ingerir dados na camada gold ",
    schedule_interval="@daily",
) as dag:
    wait_for_data_extraction = ExternalTaskSensor(
        task_id="wait_for_silver_igestion",
        external_dag_id="silver_ingestion_dag",
        external_task_id=None,
        timeout=600,
        poke_interval=30,
        mode="poke",
    )

    ingest_gold_data_task = PythonOperator(
        task_id="ingest_gold_data_to_database", python_callable=data_ingestion
    )

    data_extract_to_csv_task = PythonOperator(
        task_id="data_gold_extract_to_csv", python_callable=data_extract
    )

    (
        wait_for_data_extraction
        >> ingest_gold_data_task
        >> data_extract_to_csv_task
    )
