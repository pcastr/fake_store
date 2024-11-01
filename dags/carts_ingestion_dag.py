from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor

from fake_store.cart_ingestion import (
    CartIngestion,
)
from fake_store.find_recent_data import FindRecentData

# Configuração da DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2024, 11, 1),
    "catchup": False,
}


def ingest_cart_data():
    base_dir = "data/raw"
    data_ingestion = FindRecentData(base_dir)

    carts_recent_file = data_ingestion.buscar_carts(
        data_ingestion.obter_dia_recentes_path(
            data_ingestion.obter_ano_recentes(),
            data_ingestion.obter_mes_recentes(
                data_ingestion.obter_ano_recentes()
            ),
        )
    )
    db_path = "data/silver/fake_store.db"

    cart_ingestion = CartIngestion(db_path, carts_recent_file)
    cart_ingestion.ingest_data()


with DAG(
    "cart_ingestion_dag",
    default_args=default_args,
    description="DAG para ingerir dados de carrinhos no banco de dados SQLite",
    schedule_interval="@daily",
) as dag:
    wait_for_data_extraction = ExternalTaskSensor(
        task_id="wait_for_data_extraction",
        external_dag_id="data_extractor_dag",
        external_task_id=None,
        timeout=600,
        poke_interval=30,
        mode="poke",
    )

    ingest_cart_data_task = PythonOperator(
        task_id="ingest_cart_data",
        python_callable=ingest_cart_data,
    )

    wait_for_data_extraction >> ingest_cart_data_task
