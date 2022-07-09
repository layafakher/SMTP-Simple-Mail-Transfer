import os.path
import re
from socket import *
import sys
from _thread import *
from datetime import datetime

global boolean
boolean = True
Boolean = True
save_path = 'email/'
ThreadCount = 0

def client_handler(connection):
    global boolean
    try:
        helo = connectionSocket.recv(1024).decode()
        print(helo)
        if helo[:5] == 'HELLO':
            cl = helo.split()[1]
            st = "250 Hello " + cl+ '. Pleased to meet you.'
            connectionSocket.sendall(st.encode())
            boolean = True
    except:
        print('HELO error. Try again.')
        sys.exit()

    while boolean:
        command = connectionSocket.recv(1024).decode()
        print(command)

        _check1 = re.match(r'RCPT(\s+|$)TO:', command)
        _check2 = re.match(r'DATA', command)
        _cmd = re.match(r'MAIL(\s+|$)FROM:', command)
        _path = re.match(r'MAIL(.+)FROM:(\s*)<[^\s](.+)@(.+)[^\s]>', command)
        _mb = re.match(r'MAIL(.+)FROM:(\s*)<([A-Za-z0-9._%+-]+)@[^\s](.+)[^\s]>', command)
        _lp = re.match(r'MAIL(.+)FROM:(\s*)<([A-Za-z0-9._%+-]+)@(.+)>', command)
        _domain = re.search(r'MAIL(.+)FROM:(\s*)<(.+)@([\D.]+)>', command)

        if _check1:
            connectionSocket.send('503 Bad sequence of commands'.encode())
            continue
        if _check2:
            connectionSocket.send('503 Bad sequence of commands'.encode())
            continue
        elif not _cmd:
            connectionSocket.send('500 Syntax error: command unrecognized'.encode())
            continue
        elif not _path:
            connectionSocket.send('501 Syntax error in parameters or arguments'.encode())
            print("path is")
            continue
        elif not _mb:
            connectionSocket.send('501 Syntax error in parameters or arguments'.encode())
            print("mb is")
            continue
        elif not _lp:
            connectionSocket.send('501 Syntax error in parameters or arguments'.encode())
            print("_lp")
            continue
        elif not _domain:
            connectionSocket.send('501 Syntax error in parameters or arguments'.encode())
            print("domain")
            continue
        else:
            # From = command.replace("MAIL FROM", "From")
            inputFrom1 = command.split("<")[1]
            inputFrom = inputFrom1.split(">")[0]
            user = inputFrom.split("@")[0]
            domain = inputFrom.split("@")[1].split(".")[0]
            save_path = "com/"+domain+"/"+user+"/inbox"
            if os.path.isdir(save_path):
                ok = '250 '+inputFrom+' ... Sender OK'
                connectionSocket.send(ok.encode())
            else:
                err = 'Error, Entered mail address does not exist'
                connectionSocket.send(err.encode())


        _bool = True
        to_list = []
        rcpt_list = []
        while boolean:
            receipt = connectionSocket.recv(1024).decode()
            print(receipt)
            check = re.match(r'DATA', receipt)
            check2 = re.match(r'MAIL(\s+|$)FROM:', receipt)
            rcpt = re.match(r'RCPT(\s+|$)TO:', receipt)

            fpath = re.match(r'RCPT(.+)TO:(\s*)<([A-Za-z0-9._%+-]+)@([\D.]+)>', receipt)

            if receipt[:7] == 'Subject':
                receipt = 'DATA'
                _bool = False
                continue

            if _bool is False:
                if check:
                    break

                if check2:
                    connectionSocket.send('503 Bad sequence of commands'.encode())
                    continue
            if not rcpt:
                connectionSocket.send('501 Syntax error in parameters or arguments'.encode())
                continue
            elif not fpath:
                connectionSocket.send('501 Syntax error in parameters or arguments'.encode())
                continue
            else:
                _bool = False
                to1 = receipt.split("<")[1]
                too = to1.split(">")[0]
                user = too.split("@")[0]
                domain = too.split("@")[1].split(".")[0]
                save_path = "com/"+domain+"/"+user+"/inbox"
                # print("Tooooooooo ",too)
                if os.path.isdir(save_path):
                    ok = '250 '+too+' ... Recipient OK'
                    connectionSocket.send(ok.encode())
                    # name_of_file = name_of_file.strip('>')
                    name_of_file = user+str(datetime.now().strftime(" %d_%m_%Y %H_%M_%S"))
                    to = receipt.replace("RCPT TO: ", "")
                    rcpt_list.append(to)
                    save_name = os.path.join(save_path, name_of_file)
                    file1 = open(save_name, "a")
                    to_list.append(file1)
                else:
                    err = 'Error, Entered mail address does not exist'
                    connectionSocket.send(err.encode())
                continue

        for files in to_list:
            file1 = files
            size = len(rcpt_list)
            # file1.write(From + "\n")
            # file1.write("To: ")
            # for rcpt in rcpt_list:
            #     size = size - 1
            #     if size == 0:
            #         file1.write(rcpt + "\n")
            #     else:
            #         file1.write(rcpt + ", ")
        while boolean:
            if not check:
                datacmd = connectionSocket.recv(1024).decode()
                print(datacmd)
                check = re.match(r'DATA', datacmd)

            if not check:
                connectionSocket.send('500 Syntax error: command unrecognized'.encode())
                continue
            else:
                connectionSocket.send('354 Start mail input; end with \'.\' on a line by itself'.encode())
            while boolean:
                data = connectionSocket.recv(1024).decode()
                print(data)
                if data == '.':
                    connectionSocket.send('250 Message Accepted For Delivery'.encode())
                    boolean = False
                    sendCmd = connectionSocket.recv(1024).decode()
                    if sendCmd.lower() == 'send':
                        for files in to_list:
                            file1 = files
                            file1.write("</email_data>")
                            file1.close()
                            connectionSocket.send('250, Email Sent.'.encode())

                    quitCmd = connectionSocket.recv(1024).decode()
                    print(quitCmd)
                    if re.match(r'QUIT', quitCmd):
                        connectionSocket.send('221 Bye'.encode())
                        boolean = False
                        break

                else:
                    connectionSocket.send(data.encode())
                    for files in to_list:
                        file1 = files
                        if data[:7] == 'Subject':
                            file1.write(data + "\n")
                            file1.write("<email_data>\n")
                        else:
                            file1.write(data + "\n")
                        continue


while True:
    try:
        print("Server starting")
        serverPort = 8080
        serverName = '127.0.0.1'
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.bind((serverName, serverPort))
        serverSocket.listen(5)
        break
    except:
        print('Socket connection error. Try again.')
        sys.exit()
print("Connection Establish")

while Boolean:
    try:
        connectionSocket, addr = serverSocket.accept()
        print("220 Connection accepted from " )
        st = "220 Connection accepted from " + gethostname()
        connectionSocket.send(st.encode())
        start_new_thread(client_handler, (connectionSocket,))
    except Exception as e:
        print(e)
        print('Socket connection error.')
        sys.exit()

