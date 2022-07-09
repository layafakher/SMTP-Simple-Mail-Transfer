import re
import sys
from socket import *
def prRed(skk): print("\033[91m{}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m{}\033[00m" .format(skk))
ins = input()
if ins.lower() == 'smtp()':
    while True:
        try:
            serverName = "127.0.0.1"
            serverPort = 8080
            break
        except ValueError:
            prRed('You need two values.')
            continue
    serverPort = int(serverPort)
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    recv = clientSocket.recv(1024).decode()
    if recv[:3] != '220':
        prRed('Unable to connect to server. Please try again later.')
        clientSocket.close()
        sys.exit()
    heloCommand = 'HELLO micheal.scott'
    print(heloCommand)
    clientSocket.send(heloCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    prRed(recv1)
    if recv1[:3] != '250':
        prRed('Unable to connect to server. Please try again later.')
        clientSocket.close()
        sys.exit()

    x = 0
    while True:
        while True:
            # inputFrom = input('From: ')
            # st = 'MAIL FROM: <' + inputFrom + '>'
            st = input()
            inputFrom1 = st.split("<")[1]
            inputFrom = inputFrom1.split(">")[0]
            clientSocket.send(st.encode())
            okFrom = clientSocket.recv(1024).decode()
            prRed(okFrom)
            if okFrom[:3] != "250":
                prRed('Please enter a valid email address.')
                continue
            else:
                break
        while True:
            if x == 1:
                break
            # to = input('To: ')
            #
            # toList = to.split(", ")
            # st = 'RCPT TO: <' + to + '>'

            st = input()
            toList = st.split(",")
            for rcpt in toList:
                to1 = rcpt.split("<")[1]
                to = to1.split(">")[0]
                st = 'RCPT TO: <' + to + '>'
                clientSocket.send(st.encode())
                okTo = clientSocket.recv(1024).decode()
                prRed(okTo)
                def checkReceiptant():
                    if okTo[:3] != "250":
                        prRed('One or more email addresses are invalid. Please re-enter')
                        global x
                        x = 0
                        return
                    else:
                        x = 1
                        return
                checkReceiptant()
                if x == 0:
                    break
        dataCommand = input()
        # clientSocket.send('DATA'.encode())
        clientSocket.send(dataCommand.encode())
        okData = clientSocket.recv(1024).decode()
        prRed(okData)
        if okData[:3] != "354":
            prRed('There is an error.')
        writeFrom = ('From: ' + inputFrom)
        clientSocket.send(writeFrom.encode())
        clientSocket.recv(1024)
        writeTo = ('To: ' + to)
        clientSocket.send(writeTo.encode())
        clientSocket.recv(1024)
        readSubject = input('Subject: ')
        s = 'Subject: ' + readSubject + '\n'
        clientSocket.send(s.encode())
        clientSocket.recv(1024)
        sys.stdout.write('Data: \n')
        while True:
            readData = input()
            if readData == '':
                readData = '\r'
            clientSocket.sendall(readData.encode())
            okEnd = clientSocket.recv(1024).decode()
            if okEnd[:3] == '250':
                prRed(okEnd)
                sendCmd = input()
                clientSocket.send(sendCmd.encode())
                sendMsg = clientSocket.recv(1024).decode()
                prRed(sendMsg)
                if sendMsg[:3] == '250':
                    quitCmd = input()
                    clientSocket.send(quitCmd.encode())
                    quitMsg = clientSocket.recv(1024).decode()
                    if quitMsg[:3] != '221':
                        prRed('There was an error. Quitting.')
                        sys.exit()
                    else:
                        clientSocket.close()
                        exit()
            else:
                continue

