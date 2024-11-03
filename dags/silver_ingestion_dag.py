from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor

from fake_store.find_recent_data import FindRecentData
from fake_store.silver_carts_ingestion import (
    CartIngestion,
)
from fake_store.silver_categories_ingestion import CategoryIngestion
from fake_store.silver_database import DatabaseSilver
from fake_store.silver_products_ingestion import ProductIngestion
from fake_store.silver_user_ingestion import UserIngestion

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


def ingest_categories_data():
    base_dir = "data/raw"
    data_ingestion = FindRecentData(base_dir)

    categories_recent_file = data_ingestion.buscar_categories(
        data_ingestion.obter_dia_recentes_path(
            data_ingestion.obter_ano_recentes(),
            data_ingestion.obter_mes_recentes(
                data_ingestion.obter_ano_recentes()
            ),
        )
    )
    db_path = "data/silver/fake_store.db"
    ingestion = CategoryIngestion(db_path, categories_recent_file)
    ingestion.insert_categories()


def ingest_products_data():
    db_path = "data/silver/fake_store.db"
    base_dir = "data/raw"
    data_ingestion = FindRecentData(base_dir)

    products_recent_file = data_ingestion.buscar_products(
        data_ingestion.obter_dia_recentes_path(
            data_ingestion.obter_ano_recentes(),
            data_ingestion.obter_mes_recentes(
                data_ingestion.obter_ano_recentes()
            ),
        )
    )
    product_ingestion = ProductIngestion(db_path, products_recent_file)
    product_ingestion.insert_products()
    product_ingestion.close()


def ingest_user_data():
    base_dir = "data/raw"
    data_ingestion = FindRecentData(base_dir)
    users_recent_file = data_ingestion.buscar_users(
        data_ingestion.obter_dia_recentes_path(
            data_ingestion.obter_ano_recentes(),
            data_ingestion.obter_mes_recentes(
                data_ingestion.obter_ano_recentes()
            ),
        )
    )
    db_path = "data/silver/fake_store.db"

    user_ingestion = UserIngestion(db_path, users_recent_file)
    user_ingestion.ingest_data()


with DAG(
    "silver_ingestion_dag",
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

    ingest_categories_task = PythonOperator(
        task_id="ingest_categories_data",
        python_callable=ingest_categories_data,
    )

    ingest_products_task = PythonOperator(
        task_id="ingest_products_data",
        python_callable=ingest_products_data,
    )

    ingest_cart_data_task = PythonOperator(
        task_id="ingest_cart_data",
        python_callable=ingest_cart_data,
    )

    ingest_user_data_task = PythonOperator(
        taks_id="ingest_user_data",
        python_callable=ingest_user_data,
    )

    (
        wait_for_data_extraction
        >> ingest_categories_task
        >> ingest_products_data
        >> ingest_cart_data_task
        >> ingest_user_data_task
    )
