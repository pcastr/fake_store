import logging
import os
import sqlite3

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DatabaseSilver:
    """
    Gerencia a conexão e inicialização do banco de dados.
    """

    def __init__(self, db_path="data/gold", db_name="fake_store_gold.db"):
        """
        Inicializa o gerenciador de banco de dados.

        Args:
            db_path (str): Caminho do diretório onde o arquivo do
                           banco de dados será salvo.
            db_name (str): Nome do arquivo do banco de dados.
        """
        self.db_path = db_path
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        """Conecta ao banco de dados."""
        self.conn = sqlite3.connect(os.path.join(self.db_path, self.db_name))
        self.cursor = self.conn.cursor()
        logging.info("Conexão estabelecida com o banco de dados.")

    def create_tables(self):
        """Cria as tabelas no banco de dados se ainda não foram criadas."""
        self.cursor.executescript(
            """
        CREATE TABLE IF NOT EXISTS user_cart_insights (
            user_id INTEGER PRIMARY KEY,
            total_products INTEGER NOT NULL DEFAULT 0,
            most_frequent_category TEXT NOT NULL DEFAULT 'sem compra',
            most_recent_cart_date TEXT NOT NULL DEFAULT '0000-00-00 00:00:00',
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        """
        )
        self.conn.commit()
        logging.info("Tabelas criadas ou já existem no banco de dados.")

    def initialize_database(self):
        """
        Inicializa o banco de dados verificando se o arquivo já existe.
        Se o arquivo não existir, cria as tabelas.
        """
        full_db_path = os.path.join(self.db_path, self.db_name)
        if not os.path.isfile(full_db_path):
            logging.info(
                f"Criando o banco de dados {self.db_name} em {self.db_path}..."
            )
            self.connect()
            self.create_tables()
            logging.info("Banco de dados criado com sucesso.")
        else:
            logging.info(f"Conectando ao banco de dados {full_db_path}.")
            self.connect()

    def close(self):
        """Fecha a conexão com o banco de dados."""
        if self.conn:
            self.conn.close()
            logging.info("Conexão com o banco de dados fechada.")


# Exemplo de uso
if __name__ == "__main__":
    db_manager = DatabaseSilver(
        db_path="data/gold", db_name="fake_store_gold.db"
    )
    db_manager.initialize_database()
    db_manager.close()
