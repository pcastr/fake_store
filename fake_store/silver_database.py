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

    def __init__(self, db_path="data/silver", db_name="fake_store.db"):
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
        self.cursor.executescript("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        );

        CREATE TABLE IF NOT EXISTS geolocation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lat TEXT NOT NULL,
            long TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS addresses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            street TEXT NOT NULL,
            number INTEGER NOT NULL,
            zipcode TEXT NOT NULL,
            geolocation_id INTEGER NOT NULL,
            FOREIGN KEY (geolocation_id) REFERENCES geolocation(id)
        );

        CREATE TABLE IF NOT EXISTS names (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            name_id INTEGER NOT NULL,
            address_id INTEGER NOT NULL,
            phone TEXT NOT NULL,
            FOREIGN KEY (name_id) REFERENCES names(id),
            FOREIGN KEY (address_id) REFERENCES addresses(id)
        );

        CREATE TABLE IF NOT EXISTS carts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS cart_products (
            cart_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            PRIMARY KEY (cart_id, product_id),
            FOREIGN KEY (cart_id) REFERENCES carts(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
        """)
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
    db_manager = DatabaseSilver(db_path="data/silver", db_name="fake_store.db")
    db_manager.initialize_database()
    db_manager.close()
