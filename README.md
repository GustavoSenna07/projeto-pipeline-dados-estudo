# Pipeline de Dados - DummyJSON API

## Contexto do Projeto

Este projeto foi desenvolvidp para aprender e familiarizar com as ferramentas basicas usadas no dia a dia.

O projeto demonstra:

- Orquestração de dags com Apache Airflow
- Processamento de dados com PySpark
- Extração de dados de API
- Containerização com Docker

---

# Objetivo

Construir um pipeline capaz de:

1. Verificar a disponibilidade de uma API externa.
2. Extrair dados de forma que seja 1 produto por execução.
3. Armazenar os dados brutos.
4. Transformar e estruturar os dados com PySpark.
5. Salvar os dados tratados em formato CSV.

API utilizada:
https://dummyjson.com/products

---

# Arquitetura do Pipeline

Fluxo geral:

DummyJSON API
↓
[Airflow - PythonOperator]
↓
RAW JSON 
↓
[Airflow - SparkSubmitOperator]
↓
CSV estruturado


---

# Estrutura do Projeto

/opt/airflow/
│
├── dags/
│ └── api_data_extract.py
│
├── scripts/
│ └── transform_data_pyspark.py
│
├── data/
│ ├── raw/
│ └── processed/
│
├── .env
│
├── .gitignore
├── docker-compose.yaml
└── Dockerfile


---

# Funcionamento do Pipeline

A cada execução da DAG:

1. Verifica se a API está disponível.
2. Obtém o ID atual do produto via Airflow Variable.
3. Extrai apenas 1 produto da API.
4. Salva o JSON bruto na camada RAW.
5. Executa o script PySpark via SparkSubmitOperator.
6. Seleciona apenas colunas relevantes.
7. Achata estruturas aninhadas (ex: dimensions).
8. Salva os dados em formato CSV estruturado.
9. Incrementa o ID para a próxima execução.

---

# Dados Brutos (Raw)

Armazena os dados exatamente como retornados pela API.

Formato:

data/raw/product_1.json
data/raw/product_2.json
...


Características:

- Dados não tratados
- Permite reprocessamento futuro
- Fonte de verdade do pipeline

---

# Dados Processados (processed)

Armazena dados em formato csv.

Formato:

data/processed/


Colunas selecionadas:

- id
- title
- description
- category
- price
- rating
- stock
- weight
- width
- height
- depth

Estruturas aninhadas (ex: dimensions) são achatadas para manter formato tabular adequado para CSV.

---

# ⚙️ Tecnologias Utilizadas

- Python 3.x
- Apache Airflow
- Apache Spark (PySpark)
- Docker
- DummyJSON API

---

# Decisões Arquiteturais

## 1- Extração Incremental

A extração ocorre produto por produto, utilizando uma Airflow Variable:

| Variable | Função |
|----------|--------|
| current_product_id | Controla qual produto será extraído |

Benefícios:

- Evita reprocessamento
- Permite controle de estado
- Simula ingestão contínua
- Facilita rastreabilidade

---

## 2- Separação de Responsabilidades

A DAG separa claramente:

- Extração (PythonOperator)
- Transformação (SparkSubmitOperator)

Isso melhora:

- Organização
- Manutenção
- Escalabilidade futura

---

## 3️- Uso do PySpark

O PySpark foi utilizado para:

- Processamento distribuído
- Seleção e transformação de colunas
- Tratamento de estruturas aninhadas
- Escrita estruturada em CSV

Mesmo sendo um volume pequeno (projeto de aprendizado), o uso do Spark demonstra capacidade de trabalhar com ferramentas de Big Data.

---

## 4️- Uso de CSV

O formato CSV foi escolhido para:

- Visualização simples
- Facilidade de leitura
- Integração com ferramentas básicas

Em ambientes de produção, recomenda-se o uso de:

- Parquet
- Delta Lake
- Banco de dados

---

# Execução

1. Subir os containers:

```bash
docker-compose up -d
Acessar a interface do Airflow.

Ativar a DAG dummyjson_full_pipeline.

Executar manualmente ou aguardar agendamento.