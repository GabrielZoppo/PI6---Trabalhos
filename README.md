# Projeto Integrador IV 

## Primeira Etapa:

### Métricas Escolhidas: 
 * Uso  de CPU 	
 * Uso de Mémoria 	
 * Uso de Disco

  ### Código para entrega parcial
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
  ## Segunda Etapa:
  ### Código do monitoramento e do banco:
  * Rótina de monitoramento do Sistema:
  ~~~Python
from typing import Any, Union
import schedule
import time
from time import strftime, localtime #biblioteca responsável em colocar os dados da data e hora do sistema em timestamp para ser usado no banco
import pymysql #biblioteca utilizada para comunicação entre python e mysql
import psutil #biblioteca responsável pela coleta de dados do sistema como cpu,memoria e disco

from pymysql.cursors import Cursor

#declarando as informações necessárias para a conexão com o banco de dados
conexao = pymysql.connect(
    host = 'localhost',
    user = 'root',
    passwd='',
    database = 'projetobancodados'
)
cursor = conexao.cursor()

def Monitoramento():
    #Leitura de CPU:
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_freq = psutil.cpu_freq(percpu=False)

    #leitura de disco:
    discoC = psutil.disk_usage('C://')
    discoD = psutil.disk_usage('D://')

    #leitura de memória:
    mem = psutil.virtual_memory()

    #leitura de data e hora:
    datahora = strftime("%Y-%m-%d %H:%M:%S", localtime())

    #definindo usuário
    id = 1

    #tratamento dos dados para as devidas medidas:
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
    print()

    # inserção dos dados no Banco de Dados
    inserecpu = "insert into cpu(id, porcentagem, frequencia, data)values(%s, %s, %s, %s)"
    inseremem = "insert into memoria(id, memoria_usado, memoria_disponivel, data)values(%s, %s, %s, %s)"
    inseredis = "insert into disco(id, disco_C_usado, disco_C_livre, disco_D_usado, disco_D_livre, data)values(%s, %s, %s, %s,%s, %s)"

    valorcpu = (id, cpu_p, cpu_f, datahora)
    valormem = (id, mem_used, mem_available, datahora)
    valordis = (id, discoC_used, discoC_free, discoD_used, discoD_free, datahora)

    cursor.execute(inserecpu, valorcpu)
    cursor.execute(inseremem, valormem)
    cursor.execute(inseredis, valordis)

    conexao.commit()
#programar em quanto tempo ele executa o código novamente
schedule.every(3600).seconds.do(Monitoramento)

while 1:
    schedule.run_pending()
    time.sleep(1)
  ~~~

* Código de criação das tabelas:
~~~SQL
-- Criação tabela usuários
create table usuarios(
nome varchar(100),
id int,
primary key(id)
);

-- Criação tabela CPU
create table cpu(
id int,
porcentagem float,
frequencia float,
data timestamp,
foreign key (id) references usuarios(id)
);

-- Criação tabela memoria
create table memoria(
id int,
memoria_usado float,
memoria_disponivel float,
data timestamp,
foreign key (id) references usuarios(id)
);

-- Criação tabela disco
create table disco(
id int,
disco_C_usado float,
disco_C_livre float,
disco_D_usado float,
disco_D_livre float,
data timestamp,
foreign key (id) references usuarios(id)
);
~~~

### Código da tela:
* Código da tela funcional:

~~~python
from PyQt5 import uic, QtWidgets #biblioteca resposável pela criação da tela
from typing import Any, Union
import time
from time import strftime, localtime #biblioteca responsável em colocar os dados da data e hora do sistema em timestamp para ser usado no banco
import pymysql #biblioteca utilizada para comunicação entre python e mysql
import psutil #biblioteca responsável pela coleta de dados do sistema como cpu,memoria e disco

from pymysql.cursors import Cursor

#declarando as informações necessárias para a conexãocle com o banco de dados
conexao = pymysql.connect(
  host = 'localhost',
  user = 'root',
  passwd='',
  database = 'projetobancodados'
)
cursor = conexao.cursor()

# tabela cpu
atrituto = "porcentagem"
atrituto = "frequencia"

# tabela memoria
atrituto = "memoria_usado"
atrituto = "memoria_disponivel"



#declarando a função que vai fazer os testes e selecionar o comando a ser executado
def funcao_principal():
    # se o botão de cpu for marcado toda a tabela cpu vai ser buscada entre uma data expecifica
    if pesquisa.cpub.isChecked:
        atributo1  = pesquisa.AtributoL.text()
        atributo2 = pesquisa.AtributoL2.text()
        data1 = pesquisa.dataINI.text()
        data1 = str(data1)
        data2 = pesquisa.dataFim.text()
        data2 = str(data2)
        
        if atributo1 != "" and atributo2 != "":  
            cursor.execute("select %s,%s,data from projetobancodados.cpu where data between '%s' and '%s'" %(atributo1, atributo2, data1, data2))
        
        if atributo1 == "" and atributo2 != "":
            cursor.execute("select %s,data from projetobancodados.cpu where data between '%s' and '%s'" %(atributo2, data1, data2))

        if atributo1 != "" and atributo2 == "":
            cursor.execute("select %s,data from projetobancodados.cpu where data between '%s' and '%s'" %(atributo1, data1, data2))

        if  atributo1 == "" and atributo2 == "":
            cursor.execute("select * from projetobancodados.cpu where data between '%s' and '%s'" %(data1, data2))

    # se o botão de memoria for marcado toda a tabela memoria vai ser buscada entre uma data expecifica
    if pesquisa.memoriab.isChecked:
        atributo1  = pesquisa.AtributoL.text()
        atributo2 = pesquisa.AtributoL2.text()
        data1 = pesquisa.dataINI.text()
        data1 = str(data1)
        data2 = pesquisa.dataFim.text()
        data2 = str(data2)
        
        if atributo1 != "" and atributo2 != "":  
            cursor.execute("select %s,%s,data from projetobancodados.memoria where data between '%s' and '%s'" %(atributo1, atributo2, data1, data2))
        
        if atributo1 == "" and atributo2 != "":
            cursor.execute("select %s,data from projetobancodados.memoria where data between '%s' and '%s'" %(atributo2, data1, data2))

        if atributo1 != "" and atributo2 == "":
            cursor.execute("select %s,data from projetobancodados.memoria where data between '%s' and '%s'" %(atributo1, data1, data2))

        if  atributo1 == "" and atributo2 == "":
            cursor.execute("select * from projetobancodados.memoria where data between '%s' and '%s'" %(data1, data2))


    # se o botão de disco for marcado toda a tabela disco vai ser buscada entre uma data expecifica
    if pesquisa.discob.isChecked:
        atributo1  = pesquisa.AtributoL.text()
        atributo2 = pesquisa.AtributoL2.text()
        data1 = pesquisa.dataINI.text()
        data1 = str(data1)
        data2 = pesquisa.dataFim.text()
        data2 = str(data2)
        
        if atributo1 != "" and atributo2 != "":  
            cursor.execute("select %s,%s,data from projetobancodados.disco where data between '%s' and '%s'" %(atributo1, atributo2, data1, data2))
        
        if atributo1 == "" and atributo2 != "":
            cursor.execute("select %s,data from projetobancodados.disco where data between '%s' and '%s'" %(atributo2, data1, data2))

        if atributo1 != "" and atributo2 == "":
            cursor.execute("select %s,data from projetobancodados.disco where data between '%s' and '%s'" %(atributo1, data1, data2))

        if  atributo1 == "" and atributo2 == "":
            cursor.execute("select * from projetobancodados.disco where data between '%s' and '%s'" %(data1, data2))


    # se o botão maximo for marcado um atributo vai ser lido para fazer a consulta escolhida
    if pesquisa.maximobot.isChecked:
        atributo1  = pesquisa.AtributoL.text()
        atributo2 = pesquisa.AtributoL2.text()
        if pesquisa.cpub.isChecked:
            if atributo1 or atributo2 == "porcentagem" :
                cursor.execute("SELECT MAX(porcentagem) FROM projetobancodados.cpu")
            else:
                cursor.execute("SELECT MAX(frequencia) FROM projetobancodados.cpu")

        if pesquisa.memoriab.isChecked:
            if atributo1 or atributo2 == "memoria_usado":
                cursor.execute("SELECT MAX(memoria_usado) FROM projetobancodados.memoria")
            else:
                cursor.execute("SELECT MAX(memoria_disponivel) FROM projetobancodados.memoria")

        if pesquisa.Discob.isChecked:
            if atributo1 or atributo2 == "disco_C_usado ":
                cursor.execute("SELECT MAX(disco_C_usado) FROM projetobancodados.disco")

            if atributo1 or atributo2 == "disco_C_livre ":
                cursor.execute("SELECT MAX(disco_C_livre) FROM projetobancodados.disco")

            if atributo1 or atributo2 == "disco_D_usado ":
                cursor.execute("SELECT MAX(disco_D_usado) FROM projetobancodados.disco")

            else:
                cursor.execute("SELECT MAX(disco_D_livre) FROM projetobancodados.disco")

     # se o botão minimo for marcado um atributo vai ser lido para fazer a consulta escolhida
    if pesquisa.minimobot.isChecked:
        atributo1  = pesquisa.AtributoL.text()
        atributo2 = pesquisa.AtributoL2.text()
        if pesquisa.cpub.isChecked:
            if atributo1 or atributo2 == "porcentagem" :
                cursor.execute("SELECT MIN(porcentagem) FROM projetobancodados.cpu")
            else:
                cursor.execute("SELECT MIN(frequencia) FROM projetobancodados.cpu")

        if pesquisa.memoriab.isChecked:
            if atributo1 or atributo2 == "memoria_usado":
                cursor.execute("SELECT MIN(memoria_usado) FROM projetobancodados.memoria")
            else:
                cursor.execute("SELECT MIN(memoria_disponivel) FROM projetobancodados.memoria")

        if pesquisa.Discob.isChecked:
            if atributo1 or atributo2 == "disco_C_usado ":
                cursor.execute("SELECT MIN(disco_C_usado) FROM projetobancodados.disco")

            if atributo1 or atributo2 == "disco_C_livre ":
                cursor.execute("SELECT MIN(disco_C_livre) FROM projetobancodados.disco")

            if atributo1 or atributo2 == "disco_D_usado ":
                cursor.execute("SELECT MIN(disco_D_usado) FROM projetobancodados.disco")

            else:
                cursor.execute("SELECT MIN(disco_D_livre) FROM projetobancodados.disco")

     # se o botão maior for marcado um atributo e um valor vai ser lido para fazer a consulta escolhida
    if pesquisa.Maiorbot.isChecked:
        atributo1 = pesquisa.AtributoL.text()
        atributo2 = pesquisa.AtributoL_2.text()
        valor = pesquisa.Valor.text()
        if pesquisa.cpub.isChecked:
            if atributo1 != "" and atributo2 != "":  
                cursor.execute("select %s from projetobancodados.cpu where %s > %s" %(atributo1,valor))    
        
            if atributo1 == "" and atributo2 != "":
                cursor.execute("select %s from projetobancodados.cpu where %s > %s" %(atributo2,valor))

            if atributo1 != "" and atributo2 == "":
                cursor.execute("select %s from projetobancodados.cpu where %s > %s" %(atributo1,valor))


        if pesquisa.memoriab.isChecked:
            if atributo1 != "" and atributo2 != "":  
                cursor.execute("select %s from projetobancodados.memoria where %s > %s" %(atributo1,valor))    
        
            if atributo1 == "" and atributo2 != "":
                cursor.execute("select %s from projetobancodados.memoria where %s > %s" %(atributo2,valor))

            if atributo1 != "" and atributo2 == "":
                cursor.execute("select %s from projetobancodados.memoria where %s > %s" %(atributo1,valor))

        if pesquisa.Discob.isChecked:
            if atributo1 != "" and atributo2 != "":  
                cursor.execute("select %s from projetobancodados.disco where %s > %s" %(atributo1,valor))    
        
            if atributo1 == "" and atributo2 != "":
                cursor.execute("select %s from projetobancodados.disco where %s > %s" %(atributo2,valor))

            if atributo1 != "" and atributo2 == "":
                cursor.execute("select %s from projetobancodados.disco where %s > %s" %(atributo1,valor))

    # se o botão menor for marcado um atributo e um valor vai ser lido para fazer a consulta escolhida
    if pesquisa.Menorbot.isChecked:
        atributo1 = pesquisa.AtributoL.text()
        atributo2 = pesquisa.AtributoL_2.text()
        valor = pesquisa.Valor.text()
        if pesquisa.cpub.isChecked:
            if atributo1 != "" and atributo2 != "":  
                cursor.execute("select %s from projetobancodados.cpu where %s < %s" %(atributo1,valor))    
        
            if atributo1 == "" and atributo2 != "":
                cursor.execute("select %s from projetobancodados.cpu where %s < %s" %(atributo2,valor))

            if atributo1 != "" and atributo2 == "":
                cursor.execute("select %s from projetobancodados.cpu where %s < %s" %(atributo1,valor))


        if pesquisa.memoriab.isChecked:
            if atributo1 != "" and atributo2 != "":  
                cursor.execute("select %s from projetobancodados.memoria where %s < %s" %(atributo1,valor))    
        
            if atributo1 == "" and atributo2 != "":
                cursor.execute("select %s from projetobancodados.memoria where %s < %s" %(atributo2,valor))

            if atributo1 != "" and atributo2 == "":
                cursor.execute("select %s from projetobancodados.memoria where %s < %s" %(atributo1,valor))

        if pesquisa.Discob.isChecked:
            if atributo1 != "" and atributo2 != "":  
                cursor.execute("select %s from projetobancodados.disco where %s < %s" %(atributo1,valor))    
        
            if atributo1 == "" and atributo2 != "":
                cursor.execute("select %s from projetobancodados.disco where %s < %s" %(atributo2,valor))

            if atributo1 != "" and atributo2 == "":
                cursor.execute("select %s from projetobancodados.disco where %s < %s" %(atributo1,valor))

    # imprime o valor do resultado da pesquisa
    for x in cursor:
        print (x)

# conexão com outro arquivo na qual possui a construção da interface
app = QtWidgets.QApplication([])
pesquisa = uic.loadUi("telaPesquisa.ui")

# chamando a função principal se o botão for apertado
pesquisa.pesquisarbot.clicked.connect(funcao_principal)

# imprime a tela
pesquisa.show()
app.exec()
~~~

* código da criação da tela
~~~ui
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Dialog</class>
 <widget class="QDialog" name="Dialog">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>571</width>
    <height>337</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Dialog</string>
  </property>
  <widget class="QLabel" name="label">
   <property name="geometry">
    <rect>
     <x>120</x>
     <y>40</y>
     <width>271</width>
     <height>20</height>
    </rect>
   </property>
   <property name="text">
    <string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p align=&quot;center&quot;&gt;&lt;span style=&quot; font-size:10pt; font-weight:600;&quot;&gt;Sistema de Buscas de dados&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
   </property>
  </widget>
  <widget class="QPushButton" name="pesquisarbot">
   <property name="geometry">
    <rect>
     <x>450</x>
     <y>100</y>
     <width>93</width>
     <height>28</height>
    </rect>
   </property>
   <property name="text">
    <string>Pesquisar</string>
   </property>
  </widget>
  <widget class="QLabel" name="label_2">
   <property name="geometry">
    <rect>
     <x>80</x>
     <y>90</y>
     <width>91</width>
     <height>16</height>
    </rect>
   </property>
   <property name="text">
    <string>Data Inicial:</string>
   </property>
  </widget>
  <widget class="QLabel" name="label_3">
   <property name="geometry">
    <rect>
     <x>80</x>
     <y>120</y>
     <width>91</width>
     <height>16</height>
    </rect>
   </property>
   <property name="text">
    <string>Data Final:</string>
   </property>
  </widget>
  <widget class="QRadioButton" name="minimobot">
   <property name="geometry">
    <rect>
     <x>140</x>
     <y>250</y>
     <width>95</width>
     <height>20</height>
    </rect>
   </property>
   <property name="text">
    <string>Minimo</string>
   </property>
  </widget>
  <widget class="QRadioButton" name="maximobot">
   <property name="geometry">
    <rect>
     <x>140</x>
     <y>290</y>
     <width>95</width>
     <height>20</height>
    </rect>
   </property>
   <property name="text">
    <string>Maximo</string>
   </property>
  </widget>
  <widget class="QLabel" name="label_5">
   <property name="geometry">
    <rect>
     <x>80</x>
     <y>150</y>
     <width>91</width>
     <height>16</height>
    </rect>
   </property>
   <property name="text">
    <string>Valor:</string>
   </property>
  </widget>
  <widget class="QLineEdit" name="Valor">
   <property name="geometry">
    <rect>
     <x>170</x>
     <y>150</y>
     <width>161</width>
     <height>22</height>
    </rect>
   </property>
   <property name="placeholderText">
    <string>Digite um valor </string>
   </property>
  </widget>
  <widget class="QRadioButton" name="Maiorbot">
   <property name="geometry">
    <rect>
     <x>230</x>
     <y>250</y>
     <width>95</width>
     <height>20</height>
    </rect>
   </property>
   <property name="text">
    <string>Maior</string>
   </property>
  </widget>
  <widget class="QRadioButton" name="Menorbot">
   <property name="geometry">
    <rect>
     <x>230</x>
     <y>290</y>
     <width>95</width>
     <height>20</height>
    </rect>
   </property>
   <property name="text">
    <string>Menor</string>
   </property>
  </widget>
  <widget class="QLineEdit" name="dataINI">
   <property name="geometry">
    <rect>
     <x>170</x>
     <y>90</y>
     <width>161</width>
     <height>22</height>
    </rect>
   </property>
   <property name="placeholderText">
    <string>AAAA-MM-DD</string>
   </property>
  </widget>
  <widget class="QLineEdit" name="dataFim">
   <property name="geometry">
    <rect>
     <x>170</x>
     <y>120</y>
     <width>161</width>
     <height>22</height>
    </rect>
   </property>
   <property name="placeholderText">
    <string>AAAA-MM-DD</string>
   </property>
  </widget>
  <widget class="QCheckBox" name="cpub">
   <property name="geometry">
    <rect>
     <x>360</x>
     <y>90</y>
     <width>81</width>
     <height>20</height>
    </rect>
   </property>
   <property name="text">
    <string>CPU</string>
   </property>
  </widget>
  <widget class="QCheckBox" name="memoriab">
   <property name="geometry">
    <rect>
     <x>360</x>
     <y>120</y>
     <width>81</width>
     <height>20</height>
    </rect>
   </property>
   <property name="text">
    <string>Memória</string>
   </property>
  </widget>
  <widget class="QCheckBox" name="Discob">
   <property name="geometry">
    <rect>
     <x>360</x>
     <y>150</y>
     <width>81</width>
     <height>20</height>
    </rect>
   </property>
   <property name="text">
    <string>Disco</string>
   </property>
  </widget>
  <widget class="QLabel" name="label_4">
   <property name="geometry">
    <rect>
     <x>80</x>
     <y>180</y>
     <width>55</width>
     <height>16</height>
    </rect>
   </property>
   <property name="text">
    <string>Atributo1::</string>
   </property>
  </widget>
  <widget class="QLineEdit" name="AtributoL">
   <property name="geometry">
    <rect>
     <x>170</x>
     <y>180</y>
     <width>161</width>
     <height>22</height>
    </rect>
   </property>
   <property name="placeholderText">
    <string>Digite um atributo</string>
   </property>
  </widget>
  <widget class="QLineEdit" name="AtributoL2">
   <property name="geometry">
    <rect>
     <x>170</x>
     <y>210</y>
     <width>161</width>
     <height>22</height>
    </rect>
   </property>
   <property name="placeholderText">
    <string>Digite um atributo</string>
   </property>
  </widget>
  <widget class="QLabel" name="label_6">
   <property name="geometry">
    <rect>
     <x>80</x>
     <y>210</y>
     <width>55</width>
     <height>16</height>
    </rect>
   </property>
   <property name="text">
    <string>Atributo2:</string>
   </property>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>

~~~
* Código para botão adicionar
~~~python
from PyQt5 import uic, QtWidgets #biblioteca resposável pela criação da tela
from typing import Any, Union
import time
from time import strftime, localtime #biblioteca responsável em colocar os dados da data e hora do sistema em timestamp para ser usado no banco
import pymysql #biblioteca utilizada para comunicação entre python e mysql
import psutil #biblioteca responsável pela coleta de dados do sistema como cpu,memoria e disco

from pymysql.cursors import Cursor

#declarando as informações necessárias para a conexão com o banco de dados
conexao = pymysql.connect(
  host = 'localhost',
  user = 'root',
  passwd='',
  database = 'projeto'
)
cursor = conexao.cursor()

def adicionar():
    #Leitura de CPU:
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_freq = psutil.cpu_freq(percpu=False)

    #leitura de disco:
    discoC = psutil.disk_usage('C://')
    discoD = psutil.disk_usage('D://')

    #leitura de memória:
    mem = psutil.virtual_memory()

    #leitura de data e hora:
    datahora = strftime("%Y-%m-%d %H:%M:%S", localtime())

    #definindo usuário
    id = 1

    #tratamento dos dados para as devidas medidas:
    mem_used      = float(round(mem.used/1000000000,2))
    mem_available = float(round(mem.available/1000000000,2))
    discoC_used   = float(round(discoC.used/1000000000,2))
    discoC_free   = float(round(discoC.free/1000000000,2))
    discoD_used   = float(round(discoD.used/1000000000,2))
    discoD_free   = float(round(discoD.free/1000000000,2))
    cpu_p = float(cpu_percent)
    cpu_f = float(round(cpu_freq.current,2))


    # inserção dos dados no Banco de Dados
    inserecpu = "insert into cpu(id, porcentagem, frequencia, data)values(%s, %s, %s, %s)"
    inseremem = "insert into memoria(id, memoria_usado, memoria_disponivel, data)values(%s, %s, %s, %s)"
    inseredis = "insert into disco(id, disco_C_usado, disco_C_livre, disco_D_usado, disco_D_livre, data)values(%s, %s, %s, %s,%s, %s)"
    valorcpu = (id, cpu_p, cpu_f, datahora)
    valormem = (id, mem_used, mem_available, datahora)
    valordis = (id, discoC_used, discoC_free, discoD_used, discoD_free, datahora)
    if pesquisa.cpub.isChecked:
        cursor.execute(inserecpu, valorcpu)

    if pesquisa.memoriab.isChecked:
        cursor.execute(inseremem, valormem)

    if pesquisa.Discob.isChecked:
        cursor.execute(inseredis, valordis)

    if pesquisa.cpub.isChecked and pesquisa.memoriab.isChecked:
         cursor.execute(inserecpu, valorcpu)
         cursor.execute(inseremem, valormem)

    if pesquisa.cpub.isChecked and pesquisa.Discob.isChecked:
         cursor.execute(inserecpu, valorcpu)
         cursor.execute(inseredis, valordis)

    if pesquisa.memoriab.isChecked and pesquisa.Discob.isChecked:
         cursor.execute(inseremem, valormem)
         cursor.execute(inseredis, valordis)
    else:
        cursor.execute(inserecpu, valorcpu)
        cursor.execute(inseremem, valormem)
        cursor.execute(inseredis, valordis)
    conexao.commit()




#declarando a função que vai fazer os testes e selecionar o comando a ser executado


# conexão com outro arquivo na qual possui a construção da interface
app = QtWidgets.QApplication([])
pesquisa = uic.loadUi("telaPesquisa.ui")



# chamando a função principal se o botão for apertado
pesquisa.adicionarbot.clicked.connect(adicionar)

# imprime a tela
pesquisa.show()
app.exec()



~~~
