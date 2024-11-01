from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from fake_store.data_extractor import (
    DataExtractor,
)

# Configuração da DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2024, 11, 1),
    "catchup": False,
}


# Função para executar a extração para cada tipo de dado
def extract_data(data_type: str):
    DataExtractor.run_data_extraction(data_type)


# Definição da DAG
with DAG(
    "data_extraction_dag",
    default_args=default_args,
    description="DAG para extrair e salvar dados de uma API externa",
    schedule_interval="0 12 * * *",  # Executa diariamente ao meio-dia
) as dag:
    # Tarefas para cada tipo de dado
    extract_products = PythonOperator(
        task_id="extract_products",
        python_callable=extract_data,
        op_args=["products"],
    )

    extract_users = PythonOperator(
        task_id="extract_users",
        python_callable=extract_data,
        op_args=["users"],
    )

    extract_carts = PythonOperator(
        task_id="extract_carts",
        python_callable=extract_data,
        op_args=["carts"],
    )

    extract_categories = PythonOperator(
        task_id="extract_categories",
        python_callable=extract_data,
        op_args=["categories"],
    )

    # Definindo a ordem de execução (paralelamente)
    [extract_products, extract_users, extract_carts, extract_categories]
