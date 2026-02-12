import pendulum
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import Variable
from datetime import datetime
import requests
import os
from dotenv import load_dotenv
import json

# Carrega o .env
load_dotenv() 

# Salva as variaveis do .env
api_url = os.getenv("BASE_URL")
raw_path = os.getenv("RAW_PATH")

if not api_url:
    raise ValueError("BASE_URL não definida no .env")

if not raw_path:
    raise ValueError("RAW_PATH não definida no .env")


with DAG(
  dag_id = "extract_api_data",
  
  description = "Extract the data from the api",
  
  schedule = "@hourly",
  
  start_date = pendulum.datetime(2025, 1, 1, tz="UTC"),
  
  catchup = False,
  
  tags = ["extract", "extract_api"]
) as dag:
  #Funcao para checar se a API esta conectando
  def check_api():
    # manda uma requisicao para a api
    response = requests.get(api_url)
    
    if response.status_code == 200:
      print("API Disponivel")
    else:
      raise Exception("API Indisponivel")  
    
  # Função para criar a pasta raw caso não exista  
  def raw_data_save_folder():
    if not os.path.exists(raw_path):
      os.makedirs(raw_path)
      print("Folder Created!")
    else:
      print("Folde Already Exists!")
  
  def extract_product():
    # Pega o id do produto atual para comecar a pegar a partir do de id 1
    product_id = int(Variable.get("current_product_id", default="1"))
    
    # Endpoint acessado para extrair os dados
    url = f"{api_url}/{product_id}"
    
    # Manda a requisicao para a api para um produto especifico
    response = requests.get(url)
    
    # Gera um erro caso o produto não seja encontrado ou a api esteja com defeito
    if response.status_code != 200:
      raise Exception("Product not found")

    # Joga todos os dados do json em uma variavel data
    data = response.json()
    
    # Seleciona alguns campos do json
    select_data = {
      "id": data["id"],
      "title": data["title"],
      "description": data["description"],
      "category": data["category"],
      "price": data["price"],
      "rating": data["rating"],
      "stock": data["stock"],
      "tags": data["tags"],
      "weight": data["weight"],
      "dimensions": data["dimensions"]
    }
    
    # Define o caminho do arquivo
    file_path = f"{raw_path}/product_{product_id}.json"
    
    # with = garante que o arquivo seja fechado sozinho, mesmo se der erro
    # open = abre um arquivo
    # w = modo de escrita, sobreescreve ou cria se o arquivo não existir
    with open(file_path, "w") as f:
      # Pega os dados do dicionario select_data e tranforma tudo em json
      # f = arquivo que vai receber o json
      # indent=4 = formatacao do arquivo, melhor para a leitura
      json.dump(select_data, f, indent=4)
    
    print(f"Product {product_id} saved!")
    
    # Incrementa 1 no id do produto
    Variable.set("current_product_id", str(product_id + 1))    
  
  # Tasks
  task_check_api = PythonOperator(
    task_id = "check_api",
    python_callable = check_api,
  )
  
  task_create_folders = PythonOperator(
    task_id = "create_folders",
    python_callable = raw_data_save_folder,
  )
  
  task_extract_product = PythonOperator(
    task_id = "select_product",
    python_callable = extract_product,
  )
  
  task_check_api >> task_create_folders >> task_extract_product