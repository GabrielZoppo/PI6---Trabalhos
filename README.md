# Projeto Integrador IV 

## Métricas Escolhidas: 
 * Uso  de CPU 	
 * Uso de Mémoria 	
 * Uso de Disco

## Elaborando o código:
~~~phython
import paho.mqtt.publish as publish
import time
from time import localtime, strftime
import psutil 
import subprocess 

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
		print("Uso de Disco :", disk_use)
		print("Uso de memoria :", memory_use)
		print(strftime("%a, %d %b %Y %H:%M:%S", localtime()))

		params = "field1="+str(cpu_percent)+"&field2="+str(memory_use.percent)+"&field3="+str(disk_use.percent)
		publish.single(topic,payload=params,hostname=SERVER)

	except:
		print("connection failed") # Em caso de erro de conexão

		time.sleep(sleep)
~~~
      
   ## Visualização dos dados:    
   * [Thingspeak](https://thingspeak.com/channels/1056037)
   
  ## Organização dos dados:
  * Jogando num emulador e ouvindo música no youtube:
  ![Tempo 1:](https://media.discordapp.net/attachments/738492246583803997/747509523819921528/foto_1_trabalho_PI_VI.png?width=1024&height=587)
  
  * nada aberto:
  ![Tempo 2:](https://media.discordapp.net/attachments/738492246583803997/748241872287170681/foto_5_trabalho_PI_VI.png?width=906&height=586)
  
  * Fazendo live e jogando video game:
  ![Tempo 3:](https://media.discordapp.net/attachments/738492246583803997/747629081348014130/foto_2_trabalho_PI_VI.png?width=956&height=586)
  
  * Assistindo a aula:
  ![Tempo 4:](https://media.discordapp.net/attachments/738492246583803997/747968586693345370/foto_3_trabalho_PI_VI.png?width=1034&height=586)
  
  * Estudando
  ![Tempo 5:](https://media.discordapp.net/attachments/738492246583803997/748203686852821032/foto_4_trabalho_PI_VI.png?width=954&height=587)
      
