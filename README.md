# Projeto Integrador IV 

## Métricas Escolhidas: 
 * Uso  de CPU 	
 * Uso de Mémoria 	
 * Uso de Disco

  ## Código para entrega parcial
  ~~~python
  # importação de bibliotecas
import time
from time import localtime, strftime
import psutil
import pymysql
from pymysql.cursors import Cursor

#Criando a conexão com o servidor
conexao = pymysql.connect(
    host = 'localhost',
    user = 'root',
    passwd='',
    database = 'trabalho'
)
cursor = conexao.cursor()
sleep = 59

while True:
    # Leitura dos sensores
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disco = psutil.disk_usage('/')

    try:

        # tratamento dos dados
        mem_used = float(round(mem.used / 1000000000, 2))
        disco_used = float(round(disco.used / 1000000000, 2))
        cpu = float(cpu)
        mem_used = float(mem_used)
        disco_used = float(disco_used)

        # Printa os valores enviados, data e status da conexão
        print("CPU %:", cpu, "%")
        print("Uso de Disco :", disco_used, "GB")
        print("Uso de memoria :", mem_used, "GB")
        print(strftime("%a, %d %b %Y %H:%M:%S", localtime()))

        #instruções  de inserção MYSQL
        insere = "insert into analise(cpu_percent, memory_use, disk_use)values(%s, %s, %s)"
        valor = (cpu, disco_used, mem_used)
        cursor.execute(insere, valor)
        conexao.commit()

    except:
        
        time.sleep(sleep)
  ~~~
