#Author: 'GUOPING'
#Email: huang.guoping08@gmail.com
import socket
import sys

if __name__ == '__main__':
    serviceAddr = ('127.0.0.1', 9001)
    listenNum = 100
    acceptMax = 1512
    response = "HTTP/1.1 200 OK\r\nServer: danengine/1.2.2\r\nContent-Type: text/html; charset=UTF-8\r\n"\
               "Vary: Accept-Encoding\r\nConnection: close\r\nX-Powered-By: W3 Total Cache/0.9b\r\n\r\n"

    responseBoyd = "<!DOCTYPE html>\r\n<html>\r\n<head>\r\n<title>Python FPM</title>\r\n</head>\r\n"\
                   "<body>Ptyhon Hello world!</body>\r\n</html>\n"
    count = 1
    try:
        socketHandler = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketHandler.bind(serviceAddr)
        socketHandler.listen(listenNum)
        while 1:
            clientSocket, clientAddr = socketHandler.accept()
            acceptHander = clientSocket.recv(acceptMax)
            print(acceptHander)
            print('======================= ' + str(count))
            print(response + responseBoyd)
            clientSocket.sendall(response + responseBoyd)
            clientSocket.close()
            print('_______________________ \r\n')
            count += 1
        print('-----> finish.')
    except socket.error as msg:
        print('socket has a error: ' + str(msg[0]))
        sys.exit()
    finally:
        socketHandler.close()

