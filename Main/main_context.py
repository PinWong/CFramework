#Author: 'GUOPING'
#Email: huang.guoping08@gmail.com

class GlobalHttpContext(object):
    MODE_DEFAULT = 0
    MODE_EPOLL = 1
    __ip = '127.0.0.1'
    __port = 9001
    __mode = 0

    @property
    def ip(self):
        return self.__ip

    @ip.setter
    def ip(self, ip):
        self.__ip = ip

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, port):
        self.__port = port

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, mode):
        self.__mode = mode