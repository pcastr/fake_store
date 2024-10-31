# Documentação da Camada Raw

## Visão Geral

A **Camada Raw** é a camada responsável por armazenar os dados brutos extraídos da API antes de qualquer transformação. Nesta camada, os dados são salvos diretamente em arquivos Parquet, de forma que mantêm sua estrutura original. O uso de Parquet nesta camada foi pensado para assegurar flexibilidade, performance e escalabilidade, considerando o volume crescente de dados gerado por um e-commerce.

## Estrutura de Armazenamento

Os dados da camada Raw são particionados por data de extração, em uma estrutura de diretórios que facilita a organização e o gerenciamento de múltiplas execuções. Essa organização facilita tanto o versionamento dos dados quanto o processo de ingestão incremental na camada Silver.

Exemplo de estrutura de diretórios:

```bash
raw_data/
└── 2024/
    └── 10/
        └── 30/
            ├── carts_20241030161720.parquet
            ├── products_20241030161706.parquet
            ├── users_20241030161714.parquet
```


## Justificativas para o Uso de Parquet

### 1. Formato Colunar
O Parquet é um formato colunar que permite um armazenamento mais eficiente e compactado, especialmente útil para dados de grande volume. Como o formato Parquet armazena os dados de forma colunar, é possível:
   - **Economizar espaço em disco:** O Parquet utiliza compressão eficiente nas colunas, reduzindo o tamanho dos arquivos e os custos de armazenamento.
   - **Melhorar a performance de leitura:** Como a leitura pode ser feita apenas nas colunas necessárias, consultas específicas se tornam mais rápidas e menos custosas.

### 2. Escalabilidade
O uso de arquivos Parquet permite que o pipeline de dados possa escalar de forma simples e eficiente:
   - **Processamento em lote:** É possível agrupar vários arquivos Parquet para leitura em uma única execução, o que facilita o processamento e a carga dos dados na camada Silver.
   - **Compatibilidade com tecnologias de Big Data:** Caso o volume de dados aumente, arquivos Parquet são facilmente integrados a soluções de Big Data (como Apache Spark), permitindo o processamento distribuído.

### 3. Manutenção de Dados Brutos
O armazenamento em Parquet possibilita que os dados brutos sejam mantidos para auditoria ou reprocessamento futuro:
   - **Reprodutibilidade:** Ter uma cópia dos dados brutos permite recriar etapas de processamento ou corrigir problemas na camada Silver sem depender de novas extrações da API.
   - **Histórico Completo:** O particionamento por data facilita a organização dos dados e permite o controle do histórico de execuções, essencial para auditoria e conformidade.

## Práticas de Manutenção e Limpeza

Como os dados em Parquet são armazenados em arquivos diários, será estabelecido um processo de limpeza e arquivamento. Arquivos mais antigos podem ser compactados ou movidos para um repositório de longo prazo, garantindo que o espaço de armazenamento ativo se mantenha otimizado.

## Resumo

A **Camada Raw** é estruturada para ser eficiente e escalável, garantindo que os dados brutos estejam disponíveis de forma compactada, organizada e pronta para o processamento diário na camada Silver.

A escolha do formato Parquet reflete a necessidade de balancear o armazenamento eficiente com o desempenho de leitura, criando uma base sólida para o fluxo de dados.

