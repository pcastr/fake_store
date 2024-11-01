import json
import logging
import sqlite3
from datetime import datetime

from fake_store.find_recent_data import FindRecentData

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def format_date(date_str):
    """Formata a string de data para o formato compatível com o banco.

    Args:
        date_str (str): String de data em formato ISO.

    Returns:
        str: Data formatada no formato 'YYYY-MM-DD HH:MM:SS'.
    """
    return datetime.fromisoformat(date_str).strftime("%Y-%m-%d %H:%M:%S")


class CartIngestion:
    """Classe para ingerir dados de carrinhos de compras em um banco SQLite."""

    def __init__(self, db_path, json_path):
        """Inicializa a classe com o caminho do banco e do arquivo JSON.

        Args:
            db_path (str): Caminho do banco de dados SQLite.
            json_path (str): Caminho do arquivo JSON com dados de carrinhos.
        """
        self.db_path = db_path
        self.json_path = json_path

    def load_data(self):
        """Carrega dados do arquivo JSON."""
        try:
            with open(self.json_path, "r", encoding="utf-8") as file:
                self.carts_data = json.load(file)
            logging.info("Dados dos carrinhos carregados com sucesso.")
        except FileNotFoundError:
            logging.error(f"Arquivo JSON não encontrado: {self.json_path}")
            self.carts_data = []
        except json.JSONDecodeError as e:
            logging.error(f"Erro ao decodificar JSON: {e}")
            self.carts_data = []

    @classmethod
    def insert_cart(cls, cursor, cart_data):
        """Insere um carrinho no banco de dados, ignorando se já existir.

        Args:
            cursor (sqlite3.Cursor): Cursor da conexão SQLite.
            cart_data (dict): Dados do carrinho a ser inserido.

        Returns:
            int: ID do carrinho inserido ou existente.
        """
        cursor.execute(
            "INSERT OR IGNORE INTO carts (id, user_id, date) VALUES (?, ?, ?)",
            (cart_data["id"], cart_data["userId"], cart_data["date"]),
        )
        logging.info(f"Carrinho {cart_data['id']} inserido ou já existente.")
        return cart_data["id"]

    @classmethod
    def insert_cart_product(cls, cursor, cart_id, product_data):
        """Insere um produto associado a um carrinho no banco de dados.

        Args:
            cursor (sqlite3.Cursor): Cursor da conexão SQLite.
            cart_id (int): ID do carrinho ao qual o produto pertence.
            product_data (dict): Dados do produto a ser inserido.
        """
        cursor.execute(
            "INSERT OR IGNORE INTO cart_products"
            "(cart_id, product_id, quantity) "
            "VALUES (?, ?, ?)",
            (cart_id, product_data["productId"], product_data["quantity"]),
        )
        logging.info(
            f"""Produto {product_data["productId"]}
                inserido no carrinho {cart_id}."""
        )

    def ingest_data(self):
        """Injeta os dados dos carrinhos no banco de dados."""
        self.load_data()

        # Usar gerenciador de contexto para a conexão
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            try:
                for cart in self.carts_data:
                    # Inserindo o carrinho
                    cart_date = format_date(cart["date"])
                    cart_id = self.insert_cart(
                        cursor,
                        {
                            "id": cart["id"],
                            "userId": cart["userId"],
                            "date": cart_date,
                        },
                    )

                    # Inserindo os produtos relacionados ao carrinho
                    for product in cart["products"]:
                        self.insert_cart_product(cursor, cart_id, product)

                logging.info("Todos os dados dos carrinhos foram processados.")
            except sqlite3.Error as e:
                logging.error("Erro ao inserir dados no banco de dados: %s", e)


if __name__ == "__main__":
    base_dir = "data/raw"
    data_ingestion = FindRecentData(base_dir)
    (
        carts_recent_file,
        products_recent_file,
        users_recent_file,
        categories_recent_file,
    ) = data_ingestion.buscar_arquivos_recentes()
    db_path = "data/silver/fake_store.db"

    cart_ingestion = CartIngestion(db_path, carts_recent_file)
    cart_ingestion.ingest_data()
