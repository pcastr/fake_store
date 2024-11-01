# Extração de Dados para a "Camada raw"

<p align="center">
    <img src="./assets/fluxo-geral.svg" alt="Fluxo geral" />
</p>


A primeira etapa é a extração dos dados da [Fake Store API](https://fakestoreapi.com/). Os dados são salvos no formato original fornecido pela API (`.json`), em uma estrutura de arquivos local que simula uma "camada raw" em uma arquitetura de dados. Cada extração diária gera novos arquivos organizados por data, possibilitando um controle de versão dos dados extraídos:

```bash
raw_data/
└── 2024/
    └── 10/
        └── 30/
            ├── carts_20241030161720.json
            ├── products_20241030161706.json
            ├── users_20241030161714.json
```

### Vantagens deste Método

1. **Rastreamento de Histórico**: A organização por data permite manter um histórico detalhado de extrações, facilitando auditorias e análises temporais, essenciais para entender tendências e identificar mudanças no comportamento do usuário.

2. **Preservação do Estado Original**: Manter os dados no formato `.json`, como extraído, preserva o estado original da informação. Isso permite análise histórica mesmo que a API mude, sem perda de estrutura dos dados.

3. **Disponibilidade de Dados Brutos**: A camada raw serve como uma fonte fiel de dados brutos que pode ser processada novamente, garantindo uma camada inicial de persistência sem transformações.

### Por que Utilizar o Formato `.json`

O `.json` é flexível, amplamente suportado e permite o armazenamento de dados estruturados (objetos aninhados, listas) de forma clara, facilitando o uso em ferramentas de processamento de dados e linguagens de programação.

### Melhorias para Cenários de Grande Porte

Para um e-commerce de grande porte que coleta dados diariamente, o `.json` pode se tornar ineficiente a longo prazo devido ao armazenamento pesado e baixa eficiência em consultas. Em vez disso, recomenda-se o uso de um formato colunar, como **Parquet** ou **ORC**, que oferecem compressão nativa e são otimizados para grandes volumes de dados.

#### Recomendações para Escalabilidade e Eficiência

1. **Agrupamento Periódico**: Consolidar dados em intervalos maiores, como semanal ou mensalmente, simplifica a organização e reduz o número de arquivos.

2. **Uso de Formatos Colunares**: Formatos como Parquet ou ORC são ideais para armazenar grandes volumes de dados, melhorando a performance de leitura e reduzindo os custos de armazenamento.

3. **Data Lakes: Utilizar data lakes (ex: AWS S3, Google Cloud Storage) permite o armazenamento incremental e particionado dos dados, melhorando a escalabilidade e a velocidade das consultas.

#### Vantagens dos Formatos Colunares

- **Economia de Armazenamento**: Parquet e ORC comprimem dados de forma nativa, otimizando o espaço em disco.
- **Consultas Mais Rápidas**: Esses formatos são otimizados para consultas em colunas específicas, acelerando o processamento e reduzindo a quantidade de dados lida.
- **Integração com Ferramentas de Big Data**: Amplamente compatíveis com plataformas como Spark, Hive , Bigquery e Redshift, esses formatos permitem análises avançadas e escaláveis.

Essas adaptações tornam o fluxo de dados mais eficiente, escalável e sustentável para atender as demandas de um e-commerce de grande porte.

