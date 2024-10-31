# Fake Store Data Pipeline

Este projeto de Engenharia de Dados realiza o processamento de dados da [Fake Store API](https://fakestoreapi.com/), convertendo-os para formatos utilizáveis e criando uma pipeline de dados robusta, automatizada e pronta para análise. O fluxo de trabalho abrange desde a ingestão de dados brutos até a visualização dos dados em dashboards interativos. O projeto é orquestrado com Apache Airflow e utiliza Docker para um ambiente isolado e consistente.

<p align="center">
    <img src="./assets/fluxo-geral.svg" />
</p>


## Objetivos do Projeto

- **Ingestão de Dados:** Consumir dados da Fake Store API e armazená-los de forma eficiente.
- **Transformação:** Processar os dados para extrair informações relevantes sobre os usuários e seus produtos no carrinho.
- **Persistência:** Armazenar os dados transformados em um formato otimizado para consultas futuras.
- **Automatização:** Implementar um fluxo de trabalho agendado usando Apache Airflow para a execução diária do pipeline.
- **Visualização:** Criar um web app utilizando Streamlit para visualização dos dados e geração de relatórios.

## Estrutura do Pipeline

1. `Camada Raw`: Nesta camada, os dados brutos são armazenados em arquivos `.parquet` provenientes da Fake Store API. A cada execução do pipeline, um novo arquivo é gerado, permitindo o armazenamento de um histórico de extrações.

2. `Camada Silver`: Os dados brutos são transformados e armazenados em um banco de dados SQLite. Uma modelagem de dados é criada para refletir as relações necessárias, permitindo consultas eficientes.

3. `Camada Gold`: Nesta camada, os dados são desnormalizados e organizados em tabelas otimizadas para análise.

4.`Visualização`: Um web app desenvolvido com Streamlit permite que os usuários visualizem os dados e façam download de relatórios em formato CSV. O aplicativo oferece gráficos interativos para análise das informações dos usuários e produtos

## Orquestração

A orquestração do pipeline é realizada através do Apache Airflow, que é executado em um ambiente Docker. O Airflow gerencia as tarefas de ingestão, transformação e persistência dos dados, garantindo que o processo seja executado diariamente de forma automatizada.

## Visualização

Um web app desenvolvido com Streamlit permite que os usuários visualizem os dados e façam download de relatórios em formato CSV. O aplicativo oferece gráficos interativos para análise das informações dos usuários e produtos.
