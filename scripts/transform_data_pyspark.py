from dotenv import load_dotenv
from pyspark.sql import SparkSession
import os
import json
import sys
from pyspark.sql.functions import col
from pyspark.sql.functions import concat_ws

load_dotenv()

raw_path = os.getenv("RAW_PATH")
processed_path = os.getenv("PROCESSED_PATH")

print("RAW_PATH:", raw_path)
print("PROCESSED_PATH:", processed_path)


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

try:
    data = spark.read.option("multiline", "true").json(input_path)
except Exception as e:
    print(f"Erro ao ler JSON: {e}")
    spark.stop()
    sys.exit(1)

# Seleciona alguns dados
data_selected = data.select(
  col("id"),
  col("title"),
  col("description"),
  col("category"),
  col("price"),
  col("rating"),
  col("stock"),
  concat_ws(",", col("tags")).alias("tags"),
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
  .option("delimiter", ";") \
  .csv(processed_path)

# para o pyspark
spark.stop()
  

