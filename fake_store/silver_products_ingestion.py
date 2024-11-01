import json
import logging
import sqlite3

from find_recent_data import FindRecentData

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class ProductIngestion:
    """Classe para ingerir produtos em um banco de dados SQLite."""

    def __init__(self, db_file, json_file):
        """Inicializa a classe com o caminho do banco de dados
        e do arquivo JSON.

        Args:
            db_file (str): Caminho do arquivo de banco de dados SQLite.
            json_file (str): Caminho do arquivo JSON com dados dos produtos.
        """
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.json_file = json_file

    @staticmethod
    def fetch_products_from_file(file_path):
        """Carrega produtos de um arquivo JSON.

        Args:
            file_path (str): Caminho do arquivo JSON com dados dos produtos.

        Returns:
            list: Lista de produtos carregados do arquivo JSON.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def fetch_categories(self):
        """Recupera todas as categorias do banco de dados.

        Returns:
            dict: Um dicionário com o nome da
            categoria como chave e seu ID como valor.
        """
        self.cursor.execute("SELECT id, name FROM categories")
        return {name: id for id, name in self.cursor.fetchall()}

    def insert_products(self):
        """Insere produtos no banco de dados, evitando duplicatas."""
        categories = self.fetch_categories()
        products = self.fetch_products_from_file(self.json_file)

        for product in products:
            title = product["title"]
            price = product["price"]
            description = product["description"]
            category_name = product["category"]

            category_id = categories.get(category_name)
            if category_id is not None:
                self.cursor.execute(
                    """
                        SELECT id FROM products
                            WHERE title = ? AND category_id = ?
                    """,
                    (title, category_id),
                )
                existing_product = self.cursor.fetchone()

                if existing_product is None:
                    self.cursor.execute(
                        """
                        INSERT INTO products
                            (title, price, description, category_id)
                            VALUES (?, ?, ?, ?)
                        """,
                        (title, price, description, category_id),
                    )
                    logging.info(f"Produto '{title}' inserido com sucesso.")
                else:
                    logging.info(
                        f"Produto '{title}' já existe no banco de dados."
                    )
            else:
                logging.warning(
                    f"""Categoria '{category_name}'
                    não encontrada para o produto '{title}'."""
                )

        self.connection.commit()

    def close(self):
        """Fecha a conexão com o banco de dados."""
        self.connection.close()


if __name__ == "__main__":
    db_path = "data/silver/fake_store.db"
    base_dir = "data/raw"
    data_ingestion = FindRecentData(base_dir)
    (
        carts_recent_file,
        products_recent_file,
        users_recent_file,
        categories_recent_file,
    ) = data_ingestion.buscar_arquivos_recentes()
    product_ingestion = ProductIngestion(db_path, products_recent_file)
    product_ingestion.insert_products()
    product_ingestion.close()
