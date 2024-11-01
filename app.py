import sqlite3
from io import StringIO

import pandas as pd
import streamlit as st


# Função para carregar dados da tabela SQLite
def load_data_from_db(db_path, table_name):
    conn = sqlite3.connect(db_path)
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# Função para converter DataFrame para CSV
def convert_df_to_csv(df):
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False, encoding="utf-8")
    csv_buffer.seek(0)
    return csv_buffer.getvalue()


# Aplicativo Streamlit
def main():
    st.title("Visualização e Download da Tabela user_cart_insights")

    db_path = "data/gold/fake_store_gold.db"
    table_name = "user_cart_insights"

    # Carrega dados e exibe
    df = load_data_from_db(db_path, table_name)
    st.write("Tabela: user_cart_insights")
    st.dataframe(df)

    # Botão para download
    csv_data = convert_df_to_csv(df)
    st.download_button(
        label="Baixar CSV",
        data=csv_data,
        file_name="user_cart_insights.csv",
        mime="text/csv",
    )


if __name__ == "__main__":
    main()
