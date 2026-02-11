import pendulum
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
import requests
import os
from dotenv import load_dotenv

# Carrega o .env
load_dotenv() 

# Salva as variaveis do .env
api_url = os.getenv("BASE_URL")
raw_path = os.getenv("RAW_PATH")

with DAG(
  dag_id = "extract_api_data",
  
  description = "Extract the data from the api",
  
  schedule_interval = "@hourly"
  
  start_date = datetime(2025, 1, 1),
  
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
    
  # Função para criar a pasta data caso não exista  
  def raw_data_save_folder():
    if not os.path.exists(raw_path):
      os.makedirs(raw_path)
      print("Folder Created!")
    else:
      print("Folde Already Exists!")
  
  def extract_product():
    print
    
    task3 = BashOperator(task_id="teste3", bash_command="sleep 5")

    