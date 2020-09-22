# Projeto Integrador IV 

## Métricas Escolhidas: 
 * Uso  de CPU 	
 * Uso de Mémoria 	
 * Uso de Disco

  ## Código para entrega parcial
  ~~~python
  #importando a biblioteca PyMySQL e psutil
from typing import Any, Union
from time import strftime, localtime
import pymysql
import psutil
#Criando a conexão com o servidor
from pymysql.cursors import Cursor

conexao = pymysql.connect(
    host = 'localhost',
    user = 'root',
    passwd='',
    database = 'trabalho'
)

cursor = conexao.cursor()
# Leitura dos sensores
cpu = psutil.cpu_percent(interval=1)
mem = psutil.virtual_memory()
disco = psutil.disk_usage('/')

#tratamento dos dados
mem_used = float(round(mem.used/1000000000,2))
disco_used = float(round(disco.used/1000000000,2))
cpu = float(cpu)
mem_used = float(mem_used)
disco_used = float(disco_used)

#printar os valores
print(strftime("%a, %d %b %Y %H:%M:%S", localtime()))
print("CPU :", cpu,"%")
print("Uso de Disco : ", disco_used, "GB")
print("Uso de memoria : ", mem_used, "GB")


#instruções  de Criação das tabelas MYSQL
#cursor.execute("create table analises(cpu_percent float(6), memory_use float(6), disk_use float(6))")

#instruções  de inserção MYSQL
insere = "insert into analise(cpu_percent, disk_use, memory_use)values(%s, %s, %s)"
valor = (cpu, disco_used, mem_used)
cursor.execute(insere,valor)
conexao.commit()

#intruções de seleção MYSQL
cursor.execute("SELECT * FROM trabalho.analise where cpu_percent between 30 and 60 order by cpu_percent")
resultado = cursor.fetchall()
for linha in resultado :
print(linha)
  ~~~
