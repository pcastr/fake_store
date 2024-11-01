import logging
import os
import sqlite3

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class GoldDataInserter:
    def __init__(self, silver_db: str, gold_db: str):
        """
        Inicializa a classe GoldDataInserter.

        :param silver_db: Caminho para o banco de dados silver.
        :param gold_db: Caminho para o banco de dados gold.
        """
        self.silver_db = silver_db
        self.gold_db = gold_db
        self._create_gold_database()

    def _create_gold_database(self):
        """Cria o banco de dados gold se não existir."""
        if not os.path.exists(self.gold_db):
            logging.info(f"Criando o banco de dados: {self.gold_db}")
            conn = sqlite3.connect(self.gold_db)
            conn.close()

    def _connect_silver(self):
        """Estabelece uma conexão com o banco de dados silver."""
        return sqlite3.connect(self.silver_db)

    def _connect_gold(self):
        """Estabelece uma conexão com o banco de dados gold."""
        return sqlite3.connect(self.gold_db)

    def insert_user_cart_insights(self):
        """
        Insere ou atualiza os insights do carrinho de compras dos usuários
        no banco de dados gold a partir do banco de dados silver.
        """
        with (
            self._connect_silver() as silver_conn,
            self._connect_gold() as gold_conn,
        ):
            silver_cursor = silver_conn.cursor()
            gold_cursor = gold_conn.cursor()

            user_insights_query = """
            SELECT
                u.id AS user_id,
                COALESCE(COUNT(cp.product_id), 0) AS total_products,
                COALESCE(c.name, 'sem compra') AS most_frequent_category,
                COALESCE(MAX(ca.date), '0000-00-00 00:00:00')
                    AS most_recent_cart_date
            FROM users u
            LEFT JOIN carts ca ON u.id = ca.user_id
            LEFT JOIN cart_products cp ON ca.id = cp.cart_id
            LEFT JOIN products p ON cp.product_id = p.id
            LEFT JOIN categories c ON p.category_id = c.id
            GROUP BY u.id
            ORDER BY u.id;
            """

            silver_cursor.execute(user_insights_query)
            user_insights = silver_cursor.fetchall()

            insert_query = """
            INSERT INTO user_cart_insights
            (user_id, total_products, most_frequent_category,
            most_recent_cart_date)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                total_products = excluded.total_products,
                most_frequent_category = excluded.most_frequent_category,
                most_recent_cart_date = excluded.most_recent_cart_date;
            """

            gold_cursor.executemany(insert_query, user_insights)
            gold_conn.commit()
            logging.info("Dados de user_cart_insights inseridos com sucesso.")


if __name__ == "__main__":
    base_dir = "data/raw"
    silver_db_path = "data/silver/fake_store.db"
    gold_db_path = "data/gold/fake_store_gold.db"

    inserter = GoldDataInserter(silver_db_path, gold_db_path)
    inserter.insert_user_cart_insights()
