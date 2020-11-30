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

# declarando uma função para imprimir os dados da consulta no terminal
def visao():
  # printa o resultado do relatório
    for x in cursor:
      print (x)

#declarando uma função para adicionar valores no banco
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
def funcao_principal():
    # se o botão de cpu for marcado toda a tabela cpu vai ser buscada entre uma data expecifica
    if pesquisa.cpub.isChecked:
        atributo1  = pesquisa.AtributoL.text()
        atributo2 = pesquisa.AtributoL2.text()
        data1 = pesquisa.dataINI.text()
        data1 = str(data1)
        data2 = pesquisa.dataFim.text()
        data2 = str(data2)
        
        if atributo1 == "" and atributo2 != "":
            cursor.execute("select %s,data from projetobancodados.cpu where data between '%s' and '%s'" %(atributo2, data1, data2))

        if atributo1 != "" and atributo2 == "":
            cursor.execute("select %s,data from projetobancodados.cpu where data between '%s' and '%s'" %(atributo1, data1, data2))
        visao()
        
#declarando a função que vai fazer os testes e selecionar o comando a ser executado
def Pesquisa():
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
        visao()

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
        visao()

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
        visao()

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
        visao()

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
        visao()

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
        visao()

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
        visao()
    
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
        visao()

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
        visao()

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
        visao()

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
        visao()
        
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
        visao()

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
        visao()

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
        visao()

#declarando a função que vai fazer os testes e selecionar o comando a ser executado
def relatorio():
    # se o botão de cpu,memoria e disco for marcado toda a tabela cpu,memoria e disco vai ser buscada
    if pesquisa.cpub.isChecked  and (pesquisa.memoriab.isChecked and pesquisa.Discob.isChecked):
      cursor.execute("select cpu.frequencia,cpu.porcentagem,memoria.memoria_usado,memoria.memoria_disponivel,disco.disco_C_usado,disco.disco_C_livre,disco.disco_D_usado,disco.disco_D_livre,cpu.data from cpu inner join memoria on cpu.data = memoria.data inner join disco on memoria.data = disco.data")
      # chamada da função que imprimi no terminal os valores da consulta
      visao()

    # se o botão de cpu e memoria for marcado toda a tabela cpu e memoria vai ser buscada
    if pesquisa.cpub.isChecked and pesquisa.memoriab.isChecked :
      cursor.execute("select cpu.frequencia,cpu.porcentagem,memoria.memoria_usado,memoria.memoria_disponivel,cpu.data from cpu inner join memoria on cpu.data = memoria.data" )
      visao()

    # se o botão de cpu e disco for marcado toda a tabela cpu e disco vai ser buscada
    if pesquisa.cpub.isChecked and pesquisa.Discob.isChecked:
      cursor.execute("select cpu.frequencia,cpu.porcentagem,disco.disco_C_usado,disco.disco_C_livre,disco.disco_D_usado,disco.disco_D_livre,cpu.data from cpu inner join disco on cpu.data = disco.data")
      visao()

    # se o botão de memoria e disco for marcado toda a tabela memoria e disco vai ser buscada
    if pesquisa.memoriab.isChecked and pesquisa.Discob.isChecked :
      cursor.execute("select memoria.memoria_usado,memoria.memoria_disponivel,disco.disco_C_usado,disco.disco_C_livre,disco.disco_D_usado,disco.disco_D_livre,memoria.data from memoria inner join disco on memoria.data = disco.data")
      visao()

     # se o botão de cpu for marcado toda a tabela cpu vai ser buscada 
    if pesquisa.cpub.isChecked:
      cursor.execute("select frequencia,porcentagem,data from projetobancodados.cpu" )
      # imprime o valor do resultado da pesquisa
      visao()

     # se o botão de memoria for marcado toda a tabela memoria vai ser buscada 
    if pesquisa.memoriab.isChecked:
      cursor.execute("select memoria_usado,memoria_disponivel,data from projetobancodados.memoria")
      visao()

    # se o botão de disco for marcado toda a tabela disco vai ser buscada
    if pesquisa.Discob.isChecked:
      cursor.execute("select disco_C_usado, disco_C_livre, disco_D_usado, disco_D_livre, data from projetobancodados.disco" )
      visao()
       
# conexão com outro arquivo na qual possui a construção da interface
app = QtWidgets.QApplication([])
pesquisa = uic.loadUi("telaPesquisa.ui")

# chamando a função principal se o botão for apertado
pesquisa.pesquisarbot.clicked.connect(Pesquisa)
pesquisa.adicionarbot.clicked.connect(adicionar)
#pesquisa.graficobot.clicked.connect(relatorio)

# imprime a tela
pesquisa.show()
app.exec()
