import logging
import os
from datetime import datetime
from enum import Enum

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class FileType(Enum):
    CARTS = "carts"
    PRODUCTS = "products"
    USERS = "users"
    CATEGORIES = "categories"


class FindRecentData:
    def __init__(self, base_dir):
        """
        Inicializa a classe FindRecentData com o diretório base onde os dados
        estão armazenados, organizado por ano, mês e dia.

        Parameters:
            base_dir (str): Caminho para o diretório base contendo os arquivos.
        """
        self.base_dir = base_dir
        logging.info(f"Iniciando DataIngestion com base_dir: {self.base_dir}")

    def buscar_arquivos_recentes(self):
        """
        Busca os arquivos mais recentes para cada tipo de dado
        (carts, products, users, categories)
        com base na estrutura de diretórios de ano,mês e dia.

        returns:
            tuple: Caminhos para os arquivos mais recentes de cada tipo,
                    ou None se não existirem arquivos para um tipo específico.
        """
        ano_recentes = self.obter_ano_recentes()
        if ano_recentes is None:
            logging.warning("Nenhum ano encontrado.")
            return self._get_empty_results()

        mes_recentes = self.obter_mes_recentes(ano_recentes)
        if mes_recentes is None:
            logging.warning(
                f"Nenhum mês encontrado para o ano {ano_recentes}."
            )
            return self._get_empty_results()

        dia_recentes_path = self.obter_dia_recentes_path(
            ano_recentes, mes_recentes
        )
        if dia_recentes_path is None:
            logging.warning(
                f"""Nenhum dia encontrado para o mês
                {mes_recentes} do ano {ano_recentes}."""
            )
            return self._get_empty_results()

        return (
            self.buscar_carts(dia_recentes_path),
            self.buscar_products(dia_recentes_path),
            self.buscar_users(dia_recentes_path),
            self.buscar_categories(dia_recentes_path),
        )

    def buscar_carts(self, dia_recentes_path):
        """
        Busca o arquivo mais recente do tipo 'carts' no diretório especificado.

        parameters:
            dia_recentes_path (str): Caminho para o diretório
                                     do dia mais recente.

        returns:
            str: Caminho do arquivo mais recente de 'carts',
                 ou None se não encontrado.
        """
        return self.buscar_arquivo_por_tipo(dia_recentes_path, FileType.CARTS)

    def buscar_products(self, dia_recentes_path):
        """
        Busca o arquivo mais recente do tipo 'products'
        no diretório especificado.

        parameters:
            dia_recentes_path (str): Caminho para o diretório do dia mais recente.

        returns:
            str: Caminho do arquivo mais recente de 'products',
                 ou None se não encontrado.
        """
        return self.buscar_arquivo_por_tipo(
            dia_recentes_path, FileType.PRODUCTS
        )

    def buscar_users(self, dia_recentes_path):
        """
        Busca o arquivo mais recente do tipo 'users' no diretório especificado.

        parameters:
            dia_recentes_path (str): Caminho para o diretório
                                        do dia mais recente.

        returns:
            str: Caminho do arquivo mais recente de 'users',
                 ou None se não encontrado.
        """
        return self.buscar_arquivo_por_tipo(dia_recentes_path, FileType.USERS)

    def buscar_categories(self, dia_recentes_path):
        """
        Busca o arquivo mais recente do tipo 'categories' no diretório
        especificado.

        parameters:
            dia_recentes_path (str): Caminho para o diretório
                                     do dia mais recente.

        returns:
            str: Caminho do arquivo mais recente de
                 'categories', ou None se não encontrado.
        """
        return self.buscar_arquivo_por_tipo(
            dia_recentes_path, FileType.CATEGORIES
        )

    def buscar_arquivo_por_tipo(self, dia_recentes_path, tipo):
        """
        Encontra o arquivo mais recente de um tipo
        específico no diretório fornecido.

        parameters:
            dia_recentes_path (str): Caminho para o diretório
                                     do dia mais recente.
            tipo (FileType): Tipo do arquivo a ser buscado
            (carts, products, users, categories).

        returns:
            str: Caminho para o arquivo mais recente do
                 tipo especificado, ou None se não encontrado.
        """
        arquivos = [
            arquivo
            for arquivo in os.listdir(dia_recentes_path)
            if arquivo.endswith(".json") and tipo.value in arquivo
        ]

        if not arquivos:
            logging.warning(
                f"Nenhum arquivo encontrado para o tipo {tipo.value}."
            )
            return None

        arquivos.sort(key=self.extraindo_data_arquivo)
        arquivo_recente = arquivos[-1]
        logging.info(
            f"Arquivo recente encontrado para {tipo.value}: {arquivo_recente}"
        )
        return os.path.join(dia_recentes_path, arquivo_recente)

    def obter_ano_recentes(self):
        """
        Obtém o ano mais recente no diretório base,
        considerando que os subdiretórios
        representam os anos em formato numérico.

        parameters:
            str: Ano mais recente como string,
                 ou None se nenhum diretório de ano for encontrado.
        """
        anos = [
            d
            for d in os.listdir(self.base_dir)
            if os.path.isdir(os.path.join(self.base_dir, d))
        ]
        ano_recentes = max(anos, key=int) if anos else None
        logging.info(f"Ano mais recente encontrado: {ano_recentes}")
        return ano_recentes

    def obter_mes_recentes(self, ano):
        """
        Obtém o mês mais recente para o ano fornecido no diretório base.

        parameters:
            ano (str): Ano para o qual o mês mais recente será buscado.

        returns:
            str: Mês mais recente como string,
                 ou None se nenhum mês for encontrado.
        """
        mes_dir = os.path.join(self.base_dir, ano)
        meses = [
            d
            for d in os.listdir(mes_dir)
            if os.path.isdir(os.path.join(mes_dir, d))
        ]
        mes_recentes = max(meses, key=int) if meses else None
        logging.info(
            f"Mês mais recente encontrado para o ano {ano}: {mes_recentes}"
        )
        return mes_recentes

    def obter_dia_recentes_path(self, ano, mes):
        """
        Obtém o caminho do dia mais recente para um dado ano e mês.

        parameters:
            ano (str): Ano do diretório.
            mes (str): Mês do diretório.

        returns:
            str: Caminho completo para o
                 diretório do dia mais recente, ou None se não encontrado.
        """
        dia_dir = os.path.join(self.base_dir, ano, mes)
        dias = [
            d
            for d in os.listdir(dia_dir)
            if os.path.isdir(os.path.join(dia_dir, d))
        ]
        if not dias:
            logging.warning(
                f"Nenhum dia encontrado para o mês {mes} do ano {ano}."
            )
            return None
        dia_recentes = max(dias, key=int)
        dia_recentes_path = os.path.join(dia_dir, dia_recentes)
        logging.info(
            f"""Dia mais recente encontrado: {dia_recentes}
            com caminho: {dia_recentes_path}"""
        )
        return dia_recentes_path

    @staticmethod
    def extraindo_data_arquivo(arquivo):
        """
        Extrai e converte a data do nome do arquivo para comparação.

        parameters:
            arquivo (str): Nome do arquivo com data no formato '%Y%m%d%H%M%S'.

        returns:
            datetime: Objeto datetime representando a data extraída.
        """
        data_str = arquivo.split("_")[1].split(".")[0]
        return datetime.strptime(data_str, "%Y%m%d%H%M%S")

    @staticmethod
    def _get_empty_results():
        """
        Retorna uma tupla de resultados vazios,
        indicando ausência de arquivos recentes.

        parameters:
            tuple: Uma tupla com None para cada tipo de arquivo
                   (carts, products, users, categories).
        """
        return (None,) * len(FileType)


# Exemplo de uso
base_dir = "data/raw"
data_ingestion = FindRecentData(base_dir)
(
    carts_recent_file,
    products_recent_file,
    users_recent_file,
    categories_recent_file,
) = data_ingestion.buscar_arquivos_recentes()

print("Caminho do arquivo carts recente:", carts_recent_file)
print("Caminho do arquivo products recente:", products_recent_file)
print("Caminho do arquivo users recente:", users_recent_file)
print("Caminho do arquivo categories recente:", categories_recent_file)
