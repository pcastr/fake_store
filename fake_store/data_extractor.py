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
    """
    Classe para extrair dados de uma API e salvar em arquivos JSON.

    Attributes:
        BASE_API_URL (str): URL base da API de dados.
    """

    BASE_API_URL = "https://fakestoreapi.com"

    @staticmethod
    def fetch_data(endpoint: str) -> List[dict]:
        """Busca dados da API correspondente ao endpoint especificado."""
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
        """Valida e transforma os dados usando Pydantic."""
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
        """Converte campos datetime em strings para serialização JSON."""

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
        """Salva os dados validados em um arquivo JSON."""
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

        # Serializa os dados antes de salvar
        serialized_data = DataExtractor.serialize_data(data)

        try:
            with open(filename, "w", encoding="utf-8") as json_file:
                json.dump(serialized_data, json_file, indent=4)
            logging.info(f"Dados salvos em: {filename}")
        except Exception as e:
            logging.error(f"Erro ao salvar os dados em JSON: {e}")

    def run_products(self):
        """Executa o fluxo de extração,
        validação e salvamento para produtos."""
        endpoint = f"{self.BASE_API_URL}/products"
        try:
            data = self.fetch_data(endpoint)
            validated_data = self.validate_data(data, "products")
            self.save_to_json(validated_data, "products")
        except (requests.RequestException, ValidationError) as e:
            logging.error(f"Ocorreu um erro na execução para produtos: {e}")

    def run_users(self):
        """Executa o fluxo de extração, validação e salvamento
        para usuários."""
        endpoint = f"{self.BASE_API_URL}/users"
        try:
            data = self.fetch_data(endpoint)
            validated_data = self.validate_data(data, "users")
            self.save_to_json(validated_data, "users")
        except (requests.RequestException, ValidationError) as e:
            logging.error(f"Ocorreu um erro na execução para usuários: {e}")

    def run_carts(self):
        """Executa o fluxo de extração,
        validação e salvamento para carrinhos."""
        endpoint = f"{self.BASE_API_URL}/carts"
        try:
            data = self.fetch_data(endpoint)
            validated_data = self.validate_data(data, "carts")
            self.save_to_json(validated_data, "carts")
        except (requests.RequestException, ValidationError) as e:
            logging.error(f"Ocorreu um erro na execução para carrinhos: {e}")

    def run_categories(self):
        """Executa o fluxo de extração,
        validação e salvamento para categorias."""
        endpoint = f"{self.BASE_API_URL}/products/categories"
        try:
            data = self.fetch_data(endpoint)
            validated_data = self.validate_data(data, "categories")
            self.save_to_json(validated_data, "categories")
        except (requests.RequestException, ValidationError) as e:
            logging.error(f"Ocorreu um erro na execução para categorias: {e}")


if __name__ == "__main__":
    data_type = input(
        "Digite o tipo de dados a extrair (products, users, "
        "carts, categories): "
    )

    extractor = DataExtractor()

    if data_type == "products":
        extractor.run_products()
    elif data_type == "users":
        extractor.run_users()
    elif data_type == "carts":
        extractor.run_carts()
    elif data_type == "categories":
        extractor.run_categories()
    else:
        logging.error(f"Tipo de dados inválido: {data_type}")
