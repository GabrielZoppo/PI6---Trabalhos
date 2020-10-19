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
  
  ## Código python básico:
  ~~~Python
from typing import Any, Union
from time import strftime, localtime #biblioteca responsável em colocar os dados da data e hora do sistema em timestamp para ser usado no banco
import pymysql #biblioteca utilizada para comunicação entre python e mysql
import psutil #biblioteca responsável pela coleta de dados do sistema como cpu,memoria e disco
from pymysql.cursors import Cursor # importando cursor da biblioteca pymysql,este sendo necessário para execução dos comando mysql no python

#declarando as informações necessárias para a conexão com o banco de dados
conexao = pymysql.connect(
    host = 'localhost',
    user = 'root',
    passwd='',
    database = 'projetobancodados'
)
cursor = conexao.cursor()

# Leitura de CPU:
cpu_percent = psutil.cpu_percent(interval=1)
cpu_freq = psutil.cpu_freq(percpu=False)

#leitura de disco:
discoC = psutil.disk_usage('C://')
discoD = psutil.disk_usage('D://')

#leitura de memória:
mem = psutil.virtual_memory()

#leitura de data e hora:
datahora = strftime("%Y-%m-%d %H:%M:%S", localtime())

#tratamento dos dados para ser colocado no banco:
mem_used      = float(round(mem.used/1000000000,2))
mem_available = float(round(mem.available/1000000000,2))
discoC_used   = float(round(discoC.used/1000000000,2))
discoC_free   = float(round(discoC.free/1000000000,2))
discoD_used   = float(round(discoD.used/1000000000,2))
discoD_free   = float(round(discoD.free/1000000000,2))
cpu_p = float(cpu_percent)
cpu_f = float(round(cpu_freq.current,2))


#Imprimir todos os valores na tela:
print(strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print()

print("CPU:")
print("Porcentagem:", cpu_p,"%")
print("Frequência: ", cpu_f, "Mhz")
print()

print("Disco C:")
print("Usada : ", discoC_used, "GB")
print("Livre  : ", discoC_free, "GB")
print()

print("Disco D:")
print("Usada : ", discoD_used, "GB")
print("Livre : ", discoD_free, "GB")
print()

print("Memoria:")
print("Usada : ", mem_used, "GB")
print("Disponivel : ", mem_available, "GB")

#inserção dos dados no Banco de Dados
inserecpu = "insert into cpu(porcentagem, frequencia, data)values(%s, %s, %s)"
inseremem = "insert into memoria(memoria_usado, memoria_livre, data)values(%s, %s, %s)"
inseredis = "insert into disco(disco_C_usado, disco_C_livre, disco_D_usado, disco_D_livre, data)values(%s, %s, %s, %s,%s)"

valorcpu = (cpu_p, cpu_f, datahora)
valormem = (mem_used,mem_available , datahora)
valordis = (discoC_used, discoC_free, discoD_used,discoD_free, datahora)

cursor.execute(inserecpu, valorcpu)
cursor.execute(inseremem, valormem)
cursor.execute(inseredis, valordis)

#Atualizar o banco com os dados novos
conexao.commit()
  ~~~
