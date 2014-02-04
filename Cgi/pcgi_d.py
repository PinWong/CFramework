#Author: 'GUOPING'
#Email: huang.guoping08@gmail.com
import socket
import sys
import Web

'''
    cgi default v1.0
'''

class Pcgi(object):
    __host = '127.0.0.1'
    __port = 9001

    __socket_listen = 1024
    __socket_recv = 101024

    __response_header = "HTTP/1.1 200 OK\r\nServer: danengine/1.2.2\r\nContent-Type: text/html; charset=UTF-8\r\n"\
               "Vary: Accept-Encoding\r\nConnection: close\r\nX-Powered-By: W3 Total Cache/0.9b\r\n\r\n"

    __response_body = "<!DOCTYPE html>\r\n<html>\r\n<head>\r\n<title>Python FPM</title>\r\n</head>\r\n"\
                   "<body>Ptyhon Hello world!</body>\r\n</html>\n"

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, host):
        self.__host = host

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, port):
        self.__port = port

    def run(self):
        count = 1
        try:
            socketHandler = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socketHandler.bind((self.__host, int(self.__port[1:])))
            socketHandler.listen(self.__socket_listen)
            while True:
                clientSocket, clientAddr = socketHandler.accept()
                acceptHander = clientSocket.recv(self.__socket_recv)
                #print(acceptHander)
                http_context = Web.CHttpContext.CHttpContext(acceptHander.decode())
                print('======================= ' + str(count))
                print(self.__response_header + self.__response_body)
                clientSocket.sendall(self.__response_header + self.__response_body)
                clientSocket.close()
                print('_______________________ \r\n')
                count += 1
            print('-----> finish.')
        except socket.error as msg:
            print('socket has a error: ' + str(msg[0]))
            sys.exit(-1)
        finally:
            socketHandler.close()