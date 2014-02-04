#Author: 'GUOPING'
#Email: huang.guoping08@gmail.com

import sys
import Cgi.pcgi_d
import Cgi.pcgi_e
from Main.main_context import GlobalHttpContext


global_http_context = GlobalHttpContext()

# param format
# 0 no value
# 1 has one value after
default_argv_params = {'version': 0,
                       'process': 1,
                       'thread': 1,
                       'host': 1,
                       'mode': 1}

def return_param_format(key, index):
    if key == '--v':
        argv_param_version_callback()
        return default_argv_params['version']
    elif key == '--h':
        argv_param_host_callback(sys.argv[index + 1])
        return default_argv_params['host']
    elif key == '--p':
        argv_param_process_callback(sys.argv[index + 1])
        return default_argv_params['process']
    elif key == '--t':
        argv_param_thread_callback(sys.argv[index + 1])
        return default_argv_params['thread']
    elif key == '--m':
        argv_param_mode_callback(sys.argv[index + 1])
        return default_argv_params['mode']
    else:
        return -1

# argv fromat can key:value or just key
def print_default_argv_info():
    #info  = '----------------------------------------------------------------------------------\n'
    info  = ''
    info += 'python fpm server v1.0\n'
    info += 'server argv default:\n'
    info += '-v show fpm version\n'
    info += '-h bind the host when run fpm server,default host: 127.0.0.1:9001(ip:port)\n'
    info += '-p process count when run fpm server\n'
    info += '-t thread count when run fpm server\n'
    info += '-m use socket mode when run fpm server\n'
    info += '\n'
    print(info)
    sys.exit(0)

def get_argv_param():
    if len(sys.argv) > 1:
        current = 1
        max_index = len(sys.argv) - 1
        while current <= max_index:
            param = sys.argv[current]
            param_type = return_param_format('-' + param, current)
            if 0 == param_type:
                current += 1
            elif 1 == param_type:
                current += 2
            else:
                current += 1
    else:
        print_default_argv_info()

def argv_param_version_callback():
    print('version: v 1.0.0')

def argv_param_host_callback(origion_param):
    i = origion_param.find(':')
    if i >= 0:
        global_http_context.ip = origion_param[:i]
        global_http_context.port = origion_param[i:]
    else:
        print('warning: host format is wrong. default 127.0.0.1;9001')
        sys.exit(-1)

def argv_param_process_callback(origion_param):
    print(origion_param)

def argv_param_thread_callback(origion_param):
    print(origion_param)

def argv_param_mode_callback(origion_param):
    if origion_param == 'epoll':
        global_http_context.mode = global_http_context.MODE_EPOLL

def cgi_main():
    if global_http_context.mode == GlobalHttpContext.MODE_DEFAULT:
        fpm = Cgi.pcgi_d.Pcgi()
    else:
        fpm = Cgi.pcgi_e.Pcgi()
    fpm.host = global_http_context.ip
    fpm.port = global_http_context.port
    fpm.run()

if __name__ == '__main__':
    get_argv_param()
    cgi_main()