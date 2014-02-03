#Author: 'GUOPING'
#Email: huang.guoping08@gmail.com
import struct
import time


class CPackage(object):
    DT_BYTE = b'\x01'
    DT_CHAR = b'\x02'
    DT_INT = b'\x03'
    DT_SHORT = b'\x04'
    DT_LONG = b'\x05'
    DT_DECIMAL = b'\x06'

    #Little-End
    LITTLE_END = '<'

    @classmethod
    def pack(cls, package_element_list):
        data = b''
        for element in package_element_list:
            if element.data_type == cls.DT_BYTE:
                data += struct.pack(cls.LITTLE_END + 'ci' + str(len(element.data)) + 's',
                                    cls.DT_BYTE,
                                    len(element.data),
                                    element.data)
            elif element.data_type == cls.DT_CHAR:
                data += struct.pack(cls.LITTLE_END + 'cc', cls.DT_CHAR, element.data)
            elif element.data_type == cls.DT_INT:
                data += struct.pack(cls.LITTLE_END + 'ci', cls.DT_INT, element.data)
            elif element.data_type == cls.DT_LONG:
                data += struct.pack(cls.LITTLE_END + 'cL', cls.DT_LONG, element.data)
            elif element.data_type == cls.DT_DECIMAL:
                data += struct.pack(cls.LITTLE_END + 'cd', cls.DT_DECIMAL, element.data)
        return data

    @classmethod
    def unpack(cls, binary_data):
        data_index = 0
        length = len(binary_data)
        rows = []
        while length > 0:
            row = []
            data_type = binary_data[data_index:data_index + 1]
            if data_type == cls.DT_BYTE:
                _len = struct.unpack('i', binary_data[data_index + 1: data_index + 5])[0]
                _data = binary_data[data_index + 5:data_index + 5 + _len]
                data_index += _len + 5
                length -= _len + 5
                row.append(_data)
            elif data_index == cls.DT_CHAR:
                _data = struct.unpack('c', binary_data[data_index + 1:data_index + 2])[0]
                data_index += 2
                length -= 2
                row.append(_data)
            elif data_type == cls.DT_INT:
                _data = struct.unpack('i', binary_data[data_index + 1:data_index + 5])[0]
                data_index += 5
                length -= 5
                row.append(_data)
            elif data_type == cls.DT_SHORT:
                _data = struct.unpack('s', binary_data[data_index + 1:data_index + 3])[0]
                data_index += 3
                length -= 3
                row.append(_data)
            elif data_type == cls.DT_LONG:
                _data = struct.unpack('l', binary_data[data_index + 1:data_index + 5])[0]
                data_index += 5
                length -= 5
                row.append(_data)
            elif data_type == cls.DT_DECIMAL:
                _data = struct.unpack('d', binary_data[data_index + 1: data_index + 9])[0]
                data_index += 9
                length -= 9
                row.append(_data)
            rows.append(row)
        return rows

class CPackageElement(object):
    __data = None
    __data_type = CPackage.DT_CHAR

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

    @property
    def data_type(self):
        return self.__data_type

    @data_type.setter
    def data_type(self, date_type):
        self.__data_type = date_type

    def __init__(self, data_type, data_d):
        self.__data_type = data_type
        self.__data = data_d

def debug_write():
    fd = open('p.dat', 'wb')
    for i in range(0, 1000):
        binary = CPackage.pack([CPackageElement(CPackage.DT_BYTE, ('what the fuck haha. No.' + str(i)).encode('utf8')),
                            CPackageElement(CPackage.DT_DECIMAL, 99.07),
                            CPackageElement(CPackage.DT_LONG, 987654788),
                            CPackageElement(CPackage.DT_INT, int(time.time()))])
        try:
            fd.write(binary)
        except Exception as msg:
            print(msg[0])
    fd.close()

def debug_read(file_name):
    fd = open(file_name, 'rb')
    data = fd.read(1024)
    length = len(data)
    while length == 1024:
        _data = fd.read(1024)
        length = len(_data)
        data += _data
    fd.close()
    print(CPackage.unpack(data))



if __name__ == '__main__':
    debug_write()
    debug_read('p.dat')