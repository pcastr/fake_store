import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List

import requests
from models import Cart, Categories, Product, User
from pydantic import ValidationError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class DataExtractor:
    BASE_API_URL = "https://fakestoreapi.com"

    @staticmethod
    def fetch_data(endpoint: str) -> List[dict]:
        logging.info(f"Buscando dados de: {endpoint}")
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            logging.info("Dados recebidos com sucesso.")
            return response.json()
        except requests.HTTPError as http_err:
            logging.error(f"Erro HTTP ao buscar dados: {http_err}")
            raise
        except requests.RequestException as e:
            logging.error(f"Erro ao buscar dados: {e}")
            raise

    @staticmethod
    def validate_data(data: List[dict], data_type: str) -> List[dict]:
        validated_data = []
        if data_type == "categories":
            if isinstance(data, list):
                try:
                    validated_item = Categories(category=data)
                    validated_data.append(validated_item.model_dump())
                except ValidationError as e:
                    logging.warning(f"Erro de validação: {e}")
        else:
            for item in data:
                try:
                    if data_type == "products":
                        validated_item = Product(**item)
                    elif data_type == "users":
                        validated_item = User(**item)
                    elif data_type == "carts":
                        validated_item = Cart(**item)

                    validated_data.append(validated_item.model_dump())
                except ValidationError as e:
                    logging.warning(
                        f"Erro de validação para o item {item}: {e}"
                    )

        logging.info(f"{len(validated_data)} dados validados com sucesso.")
        return validated_data

    @staticmethod
    def serialize_data(data: List[dict]) -> List[Dict[str, Any]]:
        def convert_datetime(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(
                f"Object of type {type(obj)} is not JSON serializable"
            )

        return [
            {
                k: convert_datetime(v) if isinstance(v, (datetime,)) else v
                for k, v in item.items()
            }
            for item in data
        ]

    @staticmethod
    def save_to_json(data: List[dict], endpoint: str):
        if not data:
            logging.info("Nenhum dado para salvar.")
            return

        current_date = datetime.now()
        folder_path = (
            f"data/raw/{current_date.year}/"
            f"{current_date.month:02}/{current_date.day:02}"
        )
        os.makedirs(folder_path, exist_ok=True)

        timestamp = current_date.strftime("%Y%m%d%H%M%S")
        filename = f"{folder_path}/{endpoint}_{timestamp}.json"

        serialized_data = DataExtractor.serialize_data(data)

        try:
            with open(filename, "w", encoding="utf-8") as json_file:
                json.dump(serialized_data, json_file, indent=4)
            logging.info(f"Dados salvos em: {filename}")
        except Exception as e:
            logging.error(f"Erro ao salvar os dados em JSON: {e}")

    @classmethod
    def run_data_extraction(cls, data_type: str):
        endpoint_map = {
            "products": f"{cls.BASE_API_URL}/products",
            "users": f"{cls.BASE_API_URL}/users",
            "carts": f"{cls.BASE_API_URL}/carts",
            "categories": f"{cls.BASE_API_URL}/products/categories",
        }
        endpoint = endpoint_map.get(data_type)
        if not endpoint:
            logging.error(f"Tipo de dados inválido: {data_type}")
            return

        try:
            data = cls.fetch_data(endpoint)
            validated_data = cls.validate_data(data, data_type)
            cls.save_to_json(validated_data, data_type)
        except (requests.RequestException, ValidationError) as e:
            logging.error(f"Ocorreu um erro na execução para {data_type}: {e}")
