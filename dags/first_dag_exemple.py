import pendulum
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator

with DAG(
  # Forma como o arquivo vai ficar salvo localmente
  dag_id="Dag_de_Teste",
  # Descricao da Dag
  description="Primeira dag de teste para ver se o airflow esta integrado com o pyspark",
  # Agendamento, forma como vai ser disparada
  # None = a unica forma de disparar a dag é manualmente
  schedule=None,
  # Data de inicio da Dag
  start_date=pendulum.datetime(2026, 3, 5, tz="America/Sao_Paulo"),
  # Executa tarefas pendentes caso algo falhe no schedule
  catchup=False,
  # Forma de classificar as dags
  tags= ["teste", "primeira"]
) as dag:
  # task1 objeto python
  # BashOperator serve para executar comandos bash
  # Comandos Bash são como comandos do cmd
  # task_id é a forma como o airflow vai 
  # bash_command é o comando a ser executado
  task1 = BashOperator(task_id="teste1", bash_command="sleep 5")
  task2 = BashOperator(task_id="teste2", bash_command="sleep 5")
  task3 = BashOperator(task_id="teste3", bash_command="sleep 5")
  
  # Ordende execução das tarefas 
  task1 >> task2 >> task3
  
