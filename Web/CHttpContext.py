#Author: 'GUOPING'
#Email: huang.guoping08@gmail.com

from Web.CHttpRequest import *

class CHttpContext(object):
    __request = None
    __request_content = None
    __exception = ''

    @property
    def exception(self):
        return self.__exception

    @property
    def request(self):
        return self.__request

    @property
    def request_content(self):
        return self.__request_content

    def __init__(self, request_content):
        self.__request_content = request_content
        self.__request = CHttpRequest(self)