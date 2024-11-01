import json
import logging
import sqlite3

from fake_store.find_recent_data import FindRecentData

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class CategoryIngestion:
    def __init__(self, db_path: str, json_path: str):
        """
        Inicializa a conexão com o banco de dados e o caminho do arquivo JSON.
        :param db_path: Caminho do banco de dados SQLite.
        :param json_path: Caminho do arquivo JSON com as categorias.
        """
        self.db_path = db_path
        self.json_path = json_path

    def _connect_db(self):
        """Estabelece a conexão com o banco de dados."""
        try:
            conn = sqlite3.connect(self.db_path)
            logging.info("Conexão com o banco de dados estabelecida.")
            return conn
        except sqlite3.Error as e:
            logging.error(f"Erro ao conectar ao banco de dados: {e}")
            return None

    def load_json(self):
        """Carrega as categorias do arquivo JSON."""
        try:
            with open(self.json_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            logging.info("Conteúdo do JSON carregado com sucesso.")
            if isinstance(data, list) and data:
                # Verifica se a primeira entrada contém a chave 'category'
                if "category" in data[0]:
                    return data[0]["category"]
                else:
                    logging.warning(
                        "A chave 'category' não encontrada na entrada JSON."
                    )
            else:
                logging.warning(
                    "O JSON não contém uma lista válida ou está vazio."
                )
                return []

        except json.JSONDecodeError as e:
            logging.error(f"Erro ao decodificar o JSON: {e}")
            return []
        except FileNotFoundError:
            logging.error(f"Arquivo JSON não encontrado: {self.json_path}")
            return []

    def insert_categories(self):
        """Insere as categorias na tabela `categories`."""
        categories = self.load_json()

        if not categories:
            logging.warning("Nenhuma categoria encontrada para inserção.")
            return

        conn = self._connect_db()
        if conn is None:
            logging.error(
                "Conexão com o banco de dados não estabelecida."
                // "Abortando inserção."
            )
            return

        cursor = conn.cursor()

        for category in categories:
            try:
                cursor.execute(
                    "INSERT INTO categories (name) VALUES (?) "
                    "ON CONFLICT(name) DO NOTHING",
                    (category,),
                )
                logging.info(f"Categoria '{category}' inserida com sucesso.")
            except sqlite3.IntegrityError as e:
                logging.error(f"Erro ao inserir a categoria '{category}': {e}")

        conn.commit()
        conn.close()
        logging.info("Todas as categorias foram processadas e inseridas.")


# Exemplo de uso
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
    ingestion = CategoryIngestion(db_path, categories_recent_file)
    ingestion.insert_categories()
