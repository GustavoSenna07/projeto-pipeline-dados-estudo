from dotenv import load_dotenv
from pyspark.sql import SparkSession
import os
import json
import sys
from pyspark.sql.functions import col

load_dotenv()

raw_path = os.getenv("RAW_PATH")
processed_path = os.getenv("PROCESSED_PATH")

if not processed_path:
    raise ValueError("PROCESSED_PATH não definida no .env")
  
if not raw_path:
    raise ValueError("RAW_PATH não definida no .env")
  
product_id = sys.argv[1]
  
# SparkSession = Ponto de entrada além da criação de Data frames e permite consultas SQL
# builder = é um padrão de construção, diz que vai configurar antes de criar a sessao
# .appName define o nome da sessao
spark = SparkSession.builder \
  .appName("Process JSON Product") \
  .getOrCreate()

# Pega o arquivo de acordo com o id do produto
input_path = f"{raw_path}/product_{product_id}.json"

# Le o aquivo json e salva na variavel
data = spark.read.json(input_path)

# Seleciona alguns dados
data_selected = data.select(
  col("id"),
  col("title"),
  col("description"),
  col("category"),
  col("price"),
  col("rating"),
  col("stock"),
  col("tags"),
  col("weight"),
  col("dimensions.width").alias("width"),
  col("dimensions.height").alias("height"),
  col("dimensions.depth").alias("depth")
)

# Cria a pasta se não existir  
if not os.path.exists(processed_path):
  os.makedirs(processed_path)
  
# coalesce = gera particoes, definindo 1 gera apenas uma
# mode = define o comportamento se o destino ja existir
# append = adiciona novos dados
# header, true = escreve o nome das colunas na primeira linha
# .csv(processed_path) = define o formato de saida e o destino
data_selected.coalesce(1).write \
  .mode("append") \
  .option("header", True) \
  .csv(processed_path)
    
# para o pyspark
spark.stop()
  

