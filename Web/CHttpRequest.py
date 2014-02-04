#Author: 'GUOPING'
#Email: huang.guoping08@gmail.com

class CHttpRequest(object):

    #__header = ''
    __context = None
    __headers = {}
    __method = None
    __uri = None
    __http_version = None
    METHOD_TYPE = ['POST', 'GET', 'HEAD']
    __data = None
    __data_type = None
    __content_type = None


    # __header  = 'GET /my/index.py HTTP/1.0\r\n'
    # __header += 'Host: python_fpm_backend\r\n'
    # __header += 'Connection: close\r\n'
    # __header += 'Cache-Control: max-age=0\r\n'
    # __header += 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n'
    # __header += 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36\r\n'
    # __header += 'Accept-Encoding: gzip,deflate,sdch\r\n'
    # __header += 'Accept-Language: en,zh-CN;q=0.8,zh;q=0.6,ja;q=0.4,zh-TW;q=0.2\r\n'
    # __header += 'Cookie: pma_lang=zh_CN; pmaUser-1=Av3WbXVICZTUSPwWPm%2FKGA%3D%3D\r\n\r\n'

    # __header  = 'POST /my/index.py HTTP/1.0\r\n'
    # __header += 'Host: python_fpm_backend\r\n'
    # __header += 'Connection: close\r\n'
    # __header += 'Content-Length: 11048\r\n'
    # __header += 'Cache-Control: max-age=0\r\n'
    # __header += 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n'
    # __header += 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36\r\n'
    # __header += 'Accept-Encoding: gzip,deflate,sdch\r\n'
    # __header += 'Accept-Language: en,zh-CN;q=0.8,zh;q=0.6,ja;q=0.4,zh-TW;q=0.2\r\n'
    # __header += 'Cookie: pma_lang=zh_CN; pmaUser-1=Av3WbXVICZTUSPwWPm%2FKGA%3D%3D\r\n\r\n'
    # __header += 'article_url=http://news.sina.com.cn/s/2013-06-08/120327352118.shtml&ReferUrl=http://roll.news.sina.com.cn/news/shxw/shwx/index.shtml&article_type=%D2%BD%D2%A9%A3%AC%CE%C0%C9%FA/%C9%E7%BB%E1&Tag=%BE%C8%BB%A4%B3%B5/NT/0.247094%20%C1%D6%C4%B3/NR/0.180507%20%BA%FA%C4%B3/NR/0.155480%20%C0%F7%C4%B3/NR/0.155480%20%D6%A3%C4%B3/NR/0.155480%20%BA%FA%B7%BD%BD%DC/NR/0.123215&CMSUser=nd_hainan_user&article_ContentFrom=%B6%BC%CA%D0%BF%EC%B1%A8&Class17=%BD%A1%BF%B5%D1%F8%C9%FA/%C9%E7%BB%E1%C3%F1%C9%FA/%CA%B1%D5%FE%D2%AA%CE%C5&SensWord=&'


    @property
    def header(self):
        return self.__header

    @header.setter
    def header(self, header):
        self.__header = header

    @property
    def method(self):
        return self.__method

    @property
    def uri(self):
        return self.__uri

    def _set_request_info(self):
        header = self.header[:self.header.find('\r\n')]
        method_type, self.__uri, self.__http_version = header.split(' ')
        if method_type in self.METHOD_TYPE:
            self.__method = method_type
        else:
            print('falise.')

    def _set_data(self):
        if self.method == self.METHOD_TYPE[0]: # POST
            self.header, self.__data = self.header.split('\r\n\r\n')

    def _set_headers(self):
        headers = self.__header.split('\r\n')
        for header in headers:
            i = header.find(': ')
            if i >= 0:
                self.__headers[header[:i]] = header[i+2:]
                if header[:i] == 'Cookie':
                    self._set_cookie(header[i + 2:])

    def _set_cookie(self, cookies):
        self.__context.set_cookies(cookies)

    def __init__(self, context):
        self.__context = context
        self.__header = self.__context.request_content
        self._set_request_info()
        self._set_data()
        self._set_headers()
        print(self.__method)
        print(self.__uri)
        print(self.__http_version)
        print(self.__headers)
        print(self.__data)

