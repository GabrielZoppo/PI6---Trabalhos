# Projeto Integrador IV 

## 1º Parte da avaliação

 ### Código Python:
 
~~~
import paho.mqtt.publish as publish
import time
from time import localtime, strftime
import serial
import psutil 
import subprocess 

SERVER = "mqtt.thingspeak.com"
CHANNEL_ID = "1056037"
WRITE_API_KEY = "O6LDX4RKVBD7X4OY"
topic = "channels/" + CHANNEL_ID + "/publish/" + WRITE_API_KEY
ser = serial.Serial('/dev/ttyUSB0', 9600)

sleep = 59 # Intervalo em segundos de cada postagem


while True:
    # Leitura dos sensores
	cpu_percent = psutil.cpu_percent(interval=1)
    tr_ssd = psutil.disk_usage('/')
	str_hd = psutil.disk_usage('/')
	
	try:
		# Printa os valores enviados, data e status da conexão
		print("CPU %:", var)

		print(strftime("%a, %d %b %Y %H:%M:%S", localtime()))

		params = "field1="+str(cpu_percent)+"&field2="+str(str_ssd.used)+"&field3="+str(str_hd.used)
		publish.single(topic,payload=params,hostname=SERVER)

	except:
		print("connection failed") # Em caso de erro de conexão

		time.sleep(sleep)
~~~
      
      
       ## Valores disponiveis No thingspeak:
      https://thingspeak.com/channels/1056037
      
      
