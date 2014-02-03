#Author: 'GUOPING'
#Email: huang.guoping08@gmail.com

'''
    server & client socket should be setting non-blocking

'''

import socket
import select
import sys
import Web.CHttpContext

class Fpm(object):
    #__host = '127.0.0.1'
    __host = '192.168.41.128'
    __port = 9001
    __socket_listen = 1024
    __socket_recv = 1024
    NON_BLOCKING = False


    __server_socket = None
    __epoll = None
    __epoll_poll = 1

    __response_body  = b'HTTP/1.0 200 OK\r\nDate: Mon, 1 Jan 1996 01:01:01 GMT\r\n'
    __response_body += b'Content-Type: text/plain\r\nContent-Length: 13\r\n\r\n'
    __response_body += b'Hello, world!'

    EOL1 = b'\n\n'
    EOL2 = b'\n\r\n'

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

    @property
    def listen(self):
        return self.__socket_listen
    @listen.setter
    def listen(self, num):
        self.__socket_listen = num

    def __init__(self, host='0.0.0.0', port=9001):
        self.__host = host
        self.__port = port
        self.__init_server()
        self.__init_epoll()

    def __init__(self):
        self.__init_server()
        self.__init_epoll()

    def __init_server(self):
        try:
            self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.__server_socket.bind((self.__host, self.__port))
            self.__server_socket.listen(self.__socket_listen)
            self.__server_socket.setblocking(self.NON_BLOCKING)
            self.__server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        except socket.error as msg:
            print('initialize server socket failure, error code :' + str(msg[0]))
            sys.exit()

    def __init_epoll(self):
        try:
            self.__epoll = select.epoll()
            self.__epoll.register(self.__server_socket.fileno(), select.EPOLLIN)
        except select.error as msg:
            print('initialize epoll failure, error code :' + str(msg[0]))
            sys.exit()

    def run(self):
        try:
            connections = {}; requests = {}; responses = {}
            while True:
                events = self.__epoll.poll(self.__epoll_poll)
                for fileno, event in events:
                    if fileno == self.__server_socket.fileno():
                        connection, address = self.__server_socket.accept()
                        connection.setblocking(self.NON_BLOCKING)
                        self.__epoll.register(connection.fileno(), select.EPOLLIN)
                        connections[connection.fileno()] = connection
                        # no request, have response
                        requests[connection.fileno()] = b''
                        responses[connection.fileno()] = self.__response_body
                    elif event & select.EPOLLIN: # epoll_in
                        requests[fileno] += connections[fileno].recv(self.__socket_recv)
                        if self.EOL1 in requests[fileno] or self.EOL2 in requests[fileno]:
                            self.__epoll.modify(fileno, select.EPOLLOUT)
                            print('-'*40 + '[' + str(fileno) + '] \n') # print the http response header
                            http_context = Web.CHttpContext.CHttpContext(requests[fileno].decode())
                    elif event & select.EPOLLOUT: # epoll_out
                        response_length = connections[fileno].send(responses[fileno])
                        print('='*40 + '[' + str(fileno) + '] \n' + responses[fileno])
                        responses[fileno] = responses[fileno][response_length:] # set response empty
                        if len(responses[fileno]) == 0:
                            self.__epoll.modify(fileno, 0)
                            connections[fileno].shutdown(socket.SHUT_RDWR)
                    elif event & select.EPOLLHUP:
                        self.__epoll.unregister(fileno)
                        connections[fileno].close()
                        del connections[fileno]
        finally:
            self.__epoll.unregister(self.__server_socket.fileno())
            self.__epoll.close()
            self.__server_socket.close()

    def __delete__(self, instance):
        self.__epoll.close
        self.__server_socket.close()
