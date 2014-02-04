#Author: 'GUOPING'
#Email: huang.guoping08@gmail.com

class CHttpCookie(object):
    __context = None
    __cookies = {}

    def set_cookies(self, cookies_content):
        #print(cookies_content)
        # have a bug
        cookies = cookies_content.split('; ')
        for c in cookies:
            index = c.find('=')
            if index > 0:
                self.__cookies[c[:index]] = c[index + 1:]
        print(self.__cookies)

    def __init__(self, context):
        self.__context = context