# -*- coding: utf-8 -*-
class Symbol(object):
    storage_class = frozenset(["stack", "heap", "bss", "data"])
    def __init__(self, name, size, _type):
        self.name = name
        self._class = 'stack' # 存储类型
        self.size = size # 存储字节数
        self.bitsize = 0 # 存储比特数
        self._type = _type # 符号的类型
        # self.machine_type = ""
        self.register = False # 是否在寄存器中
        self.reg = "" # 存储该符号的寄存器
        self.base_reg = "" # 该符号地址所在的寄存器
        self.disp = 0 # 相对基址寄存器的偏移

class SymbolTable(object):
    pass

class TableStack(object):
    pass
        
