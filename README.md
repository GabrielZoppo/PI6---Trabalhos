# Projeto Integrador IV 

## Métricas Escolhidas: 
 * Uso  de CPU 	
 * Uso de Mémoria 	
 * Uso de Disco

## Elaborando o código:
~~~phython
# importação de bibliotecas
import paho.mqtt.publish as publish
import time
from time import localtime, strftime
import psutil
import subprocess

# Configurando os dados para comunicação com Thingspeak
SERVER = "mqtt.thingspeak.com"
CHANNEL_ID = "1056037"
WRITE_API_KEY = "70Q9QHDYG3THOLWX"
topic = "channels/" + CHANNEL_ID + "/publish/" + WRITE_API_KEY

sleep = 59
while True:
   # Leitura dos sensores
   cpu_percent = psutil.cpu_percent(interval=1)
   memory_use = psutil.virtual_memory()
   disk_use = psutil.disk_usage('/')

   try:
       # Printa os valores enviados, data e status da conexão
       print("CPU %:", cpu_percent)
       print("Uso de Disco :", disk use)
       print("Uso de memoria :", memory use)
       print(strftime("%a, %d %b %Y %H:%M:%S", localtime()))

       # Envia os dados para o Thingspeak
       params = "field1=" + str(cpu_percent) + "&field2=" + str(memory_use.percent) + "&field3=" + str(
           disk_use.percent)
       publish.single(topic, payload=params, hostname=SERVER)

   except:
       print("connection failed")  # Em caso de erro de conexão

       time.sleep(sleep)
~~~
      
   ## Visualização dos dados:    
   * [Thingspeak](https://thingspeak.com/channels/1056037)
     
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
  ~~~
