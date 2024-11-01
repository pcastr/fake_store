import json
import logging
import sqlite3

from fake_store.find_recent_data import FindRecentData

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class UserIngestion:
    """Classe para ingerir usuários em um banco de dados SQLite."""

    def __init__(self, db_path, json_path):
        """Inicializa a classe com o caminho do banco e do arquivo JSON.

        Args:
            db_path (str): Caminho do arquivo de banco de dados SQLite.
            json_path (str): Caminho do arquivo JSON com dados dos usuários.
        """
        self.db_path = db_path
        self.json_path = json_path
        self.users_data = []

    def load_data(self):
        """Carrega os dados dos usuários a partir do arquivo JSON."""
        with open(self.json_path, "r", encoding="utf-8") as file:
            self.users_data = json.load(file)

    @classmethod
    def insert_geolocation(cls, cursor, geolocation):
        """Insere a geolocalização no banco de dados.

        Args:
            cursor: O cursor do banco de dados.
            geolocation (dict): Dados de geolocalização.

        Returns:
            int: ID da geolocalização inserida.
        """
        cursor.execute(
            "INSERT INTO geolocation (lat, long) VALUES (?, ?)",
            (geolocation["lat"], geolocation["long"]),
        )
        return cursor.lastrowid

    @classmethod
    def insert_address(cls, cursor, address_data):
        """Insere o endereço no banco de dados.

        Args:
            cursor: O cursor do banco de dados.
            address_data (dict): Dados do endereço.

        Returns:
            int: ID do endereço inserido.
        """
        cursor.execute(
            "INSERT INTO addresses "
            "(city, street, number, zipcode, geolocation_id) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                address_data["city"],
                address_data["street"],
                address_data["number"],
                address_data["zipcode"],
                address_data["geolocation_id"],
            ),
        )
        return cursor.lastrowid

    @classmethod
    def insert_name(cls, cursor, name_data):
        """Insere o nome no banco de dados.

        Args:
            cursor: O cursor do banco de dados.
            name_data (dict): Dados do nome.

        Returns:
            int: ID do nome inserido.
        """
        cursor.execute(
            "INSERT INTO names (firstname, lastname) VALUES (?, ?)",
            (name_data["firstname"], name_data["lastname"]),
        )
        return cursor.lastrowid

    @classmethod
    def insert_user(cls, cursor, user_data):
        """Insere o usuário no banco de dados.

        Args:
            cursor: O cursor do banco de dados.
            user_data (dict): Dados do usuário.
        """
        cursor.execute(
            "INSERT INTO users"
            "(email, username, password, name_id, address_id, phone) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                user_data["email"],
                user_data["username"],
                user_data["password"],
                user_data["name_id"],
                user_data["address_id"],
                user_data["phone"],
            ),
        )
        logging.info(
            f"Usuário '{user_data['username']}' inserido com sucesso."
        )

    def ingest_data(self):
        """Realiza a ingestão de dados dos usuários no banco de dados."""
        self.load_data()
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        try:
            for user in self.users_data:
                cursor.execute(
                    "SELECT id FROM users WHERE email = ?", (user["email"],)
                )
                if cursor.fetchone() is not None:
                    logging.warning(
                        f"Usuário '{user['email']}' já existe no banco."
                    )
                    continue

                geolocation_id = self.insert_geolocation(
                    cursor, user["address"]["geolocation"]
                )

                address_data = user["address"]
                address_data["geolocation_id"] = geolocation_id
                address_id = self.insert_address(cursor, address_data)

                name_id = self.insert_name(cursor, user["name"])

                user_data = {
                    "email": user["email"],
                    "username": user["username"],
                    "password": user["password"],
                    "name_id": name_id,
                    "address_id": address_id,
                    "phone": user["phone"],
                }
                self.insert_user(cursor, user_data)

            connection.commit()
        except sqlite3.Error as e:
            connection.rollback()
            logging.error("Erro ao inserir dados: %s", e)
        finally:
            connection.close()


if __name__ == "__main__":
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
