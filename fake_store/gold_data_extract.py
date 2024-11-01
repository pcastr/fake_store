import csv
import os
import sqlite3


class DatabaseExporter:
    def __init__(self, db_path):
        """
        Inicializa a conexão com o banco de dados SQLite.

        :param db_path: Caminho para o arquivo do banco de dados SQLite.
        """
        self.db_path = db_path

    def export_to_csv(self, table_name, csv_path):
        """
        Exporta os dados de uma tabela SQLite para um arquivo CSV.

        :param table_name: Nome da tabela a ser exportada.
        :param csv_path: Caminho para o arquivo CSV de saída.
        """
        output_dir = os.path.dirname(csv_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            column_names = [
                description[0] for description in cursor.description
            ]

            with open(
                csv_path, mode="w", newline="", encoding="utf-8"
            ) as file:
                writer = csv.writer(file)
                writer.writerow(column_names)
                writer.writerows(rows)

            print(f"Dados exportados com sucesso para {csv_path}")

        except sqlite3.Error as e:
            print(f"Erro ao exportar dados: {e}")

        finally:
            conn.close()


# Exemplo de uso:
db_exporter = DatabaseExporter("data/gold/fake_store_gold.db")
db_exporter.export_to_csv(
    "user_cart_insights", "data/marts/user_cart_insights.csv"
)
