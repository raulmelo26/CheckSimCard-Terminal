import sys
import serial
from serial import SerialException
import time
import os
flag = 's'
phoneNumber = "+5585985628574"#"+5585991779376" #"+5585981560324"
dataMessage = "!r0"

####### Habilita o echo do modem #######
def setEcho(s):
    s.write(b'ATE1\n')
    time.sleep(1)
    s.flushInput()
    s.flushOutput()

####### Retorna o ICCID do chip #######
def getICCID(s):
    s.write(b'AT+ICCID\n')
    time.sleep(1)
    arduinoData = str(s.read_all())
    iccid = arduinoData[24:44]
    return iccid

####### Numero da operadora ######
def getNumOperadora(s):
    s.write(b'AT+COPS=3,0\n')
    time.sleep(1)
    s.flushInput()
    s.write(b'AT+COPS?\n')
    time.sleep(1)
    arduinoData = str(s.read_all())
    operadora = arduinoData[28:33]
    return operadora

####### Nome da operadora #######
def getOperadora(operadora):
    if (operadora == "72405"):
        op = "CLARO"
    elif (operadora == "72410" or operadora == "72411"):
        op = "VIVO"
    elif (operadora == "72431"):
        op = "OI"
    elif (operadora == "72403"):
        op = "TIM"
    else:
        op = "Desconhecida"
    return op

####### Verifica se o medem suporta texto #######
def textModeSupported(s):
    s.write(b'AT+CMGF=1\n')
    time.sleep(1)
    responseData = str(s.read_all())
    if(responseData.find("OK")):
        return True
    else:
        return False

####### Set o numero do destinatario #######
def setPhoneNumber(s,number):
    str1 = "AT+CMGS=\"" + number + "\",145\n"
    s.write(str1.encode())
    time.sleep(1)

####### Escreve a mensagem #######
def writeMessage(s,message):
    s.write(message.encode())
    time.sleep(1)
    s.flushInput()
    s.flushOutput()
    s.write(b'\032')
    time.sleep(1)

    responseData = str(s.readline())
    responseData = str(s.readline())
    responseData = str(s.readline())
    responseData = str(s.readline()[:-2])

    if (responseData.find("OK") != -1):
        return True
    else:
        return False

####### Limpa saida e entreda #######
def flush():
    s.flushInput()
    s.flushOutput()

while(flag == 's'):
    conected = 0
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]

    result = []
    os.system("cls")
    print("###############################")
    print("##  Procurando dispositivo   ##")
    time.sleep(0.3)
    os.system("cls")
    print("###############################")
    print("##  Procurando dispositivo.  ##")
    time.sleep(0.3)
    os.system("cls")
    print("###############################")
    print("##  Procurando dispositivo.. ##")
    time.sleep(0.3)
    os.system("cls")
    print("###############################")
    print("##  Procurando dispositivo...##")
    time.sleep(0.3)

    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass

    for p in result:
        try:
            s = serial.Serial(p)
            s.write("AT\n".encode())
            responseData = str(s.readline())
            responseData = str(s.readline())
            responseData = str(s.readline()[:-2])
            #print(responseData)
            #print(p)
            if(responseData == "b'OK'"):
                print("##   Conexão estabelecida    ##")
                print("###############################")
                conected = 1
                break
            else:
                s.close()
                print("##      Falha na conexão     ##")
        except (OSError, serial.SerialException):
            pass

    if(conected):
        setEcho(s)
        print("#  Buscando ICCID e Operadora #")
        iccid = getICCID(s)
        str1 = "# ICCID: " + iccid + " #"
        print(str1)

        flush()
        time.sleep(3)
        operadora = getNumOperadora(s)
        op = getOperadora(operadora)
        if(op == "Desconhecida"):
            print("##  Operadora Desconhecida   ##")
            print("##  Número OP: %s         ##" %operadora)
        else:
            str2 ="Operadora: " + op + ", " + operadora
            print("#  Operadora: " + op + ", " + operadora+"    #")

        print("###############################")
        print("##      Enviando sms...      ##")

        if(not textModeSupported(s)):
            print("Mode text not supported")

        flush()

        setPhoneNumber(s,phoneNumber)

        flush()

        if(writeMessage(s,dataMessage)):
            print("##  sms enviado com sucesso  ##")
        else:
            print("##     sms não enviado       ##")
        print("###############################")
        print("######  Nova pesquisa?   ######")
        print("###### [s] SIM [n] NÃO   ######")
        flag = input()

        s.close()

