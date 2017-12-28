from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import serial
from serial import SerialException
import time
import string
import glob
import os
flag = 's'
while(flag == 's'):
    conected = 0
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]

    result = []
    os.system("cls")
    print("Procurando dispositivo...")
    time.sleep(1)
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
                print("Conectado ao modem")
                conected = 1
                break
            else:
                s.close()
                print("Não conectado ao modem")
        except (OSError, serial.SerialException):
            pass

    if(conected):
        s.write(b'ATE1\n')
        time.sleep(1)
        s.flushInput()
        s.flushOutput()

        print("Buscando ICCID e Operadora...\n")
        s.write(b'AT+ICCID\n')
        time.sleep(1)
        arduinoData = str(s.read_all())
        iccid = arduinoData[24:44]
        str1 = "ICCID: " + iccid + "\n"
        print(str1)

        s.flushInput()
        s.flushOutput()

        s.write(b'AT+COPS=3,0\n')
        time.sleep(1)
        s.flushInput()
        s.write(b'AT+COPS?\n')
        time.sleep(1)
        arduinoData = str(s.read_all())
        operadora = arduinoData[28:33]

        if(operadora == "72405"):
            op = "CLARO"
        elif(operadora == "72410" or operadora == "72411"):
            op = "VIVO"
        elif(operadora == "72431"):
            op = "OI"
        elif(operadora == "72403"):
            op = "TIM"
        else:
            op = "Desconhecida"
        str2 ="Operadora: " + op + ", " + operadora + "\n"

        print("Operadora: " + op + ", " + operadora)

        print("\nEnviando sms...")

        s.flushInput()
        s.flushOutput()
        s.write(b'AT+CMGF=1\n')
        time.sleep(1)

        s.flushInput()
        s.flushOutput()
        s.write(b'AT+CMGF=1\n')
        time.sleep(1)

        s.flushInput()
        s.flushOutput()
        str1 = "AT+CMGS=\"+5585985628574\",145\n"
        s.write(str1.encode())
        time.sleep(1)

        s.flushInput()
        s.flushOutput()
        s.write("Teste".encode())
        time.sleep(1)

        s.flushInput()
        s.flushOutput()
        s.write(b'\032')
        time.sleep(1)

        responseData = str(s.readline())
        responseData = str(s.readline())
        responseData = str(s.readline())
        responseData = str(s.readline()[:-2])


        if(responseData.find("OK") != -1):
            print("sms enviado com sucesso")
        else:
            print("sms não enviado")

        time.sleep(3)
        os.system("cls")
        print("##########  Nova pesquisa  ##########")
        print("########## [s] SIM [n] NÃO ##########")
        flag = input()

        s.close()
