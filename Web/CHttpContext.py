#Author: 'GUOPING'
#Email: huang.guoping08@gmail.com
from Utility.CUrlRoute import CUrlRoute

from Web.CHttpCookie import CHttpCookie
from Web.CHttpRequest import *

class CHttpContext(object):
    __request = None
    __request_content = None
    __cookie = None
    __route = None
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

    def set_cookies(self, cookie_content):
        self.__cookie.set_cookies(cookie_content)

    def run(self):
        self.__request.uri

    def __init__(self, request_content):
        self.__request_content = request_content
        self.__cookie = CHttpCookie(self)
        self.__request = CHttpRequest(self)
        self.__route = CUrlRoute()
