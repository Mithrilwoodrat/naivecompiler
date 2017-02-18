# -*- coding: utf-8 -*-
import logging
import sys
import ctypes
import traceback
import hashlib
from c_parser import Parser
from c_ast import *


logger = logging.getLogger(__file__)

class StringTable(object):
    def __init__(self):
        self.table = []
        self.index = 0
        
    def add(self, string):
        if string not in self.table:
            self.table.append(string)
            old_index = self.index
            self.index+=1
            return old_index
        return self.table.index(string)

    def get_id(self,string):
        if string in self.table:
            return self.table.index(string)
        return -1

class Env(object):
    '''
    在序列化过程中使用
    如全局字符串表
    '''
    def __init__(self):
        self.string_table = StringTable()

    def add_string(self, string):
        return self.string_table.add(string)

    def get_id(self, string):
        pass
        

class Compiler(object):
    '''
    Use PLY Parser parse source code to AST
    then dump AST to Binary 
    '''
    def __init__(self, source):
        self.source = source
        self.parser = Parser()
        self.env = Env()

    def ast_gen(self):
        self.ast = self.parser.parse(self.source)
        self.ast.show()

    def analysis(self):
        pass

    def dump_stringtable(self):
        string_table = self.env.string_table
        print string_table.index
        print string_table.table
        data = ''
        for string in string_table.table:
            data += string + '\0'
        return data
    
    def compile(self):
        obj = FileFormat()
        body = self.ast.serialize(self.env)
        stringtable = self.dump_stringtable()
        logger.info("StringTable: %s " % stringtable)
        obj['stringtable'] = stringtable
        obj['body'] = body
        obj[ "bodyMD5" ] = hashlib.md5( str(body) ).digest()
        with open('ns.data','w') as fout:
            fout.write(str(obj))
    
if __name__ == "__main__":
    logging.basicConfig(format='[%(asctime)s] (%(module)s:%(funcName)s:%(lineno)s): <%(levelname)s> %(message)s', level=logging.INFO)
    with open(sys.argv[1]) as f:
        source = f.read()
    compiler = Compiler(source)
    compiler.ast_gen()
    compiler.compile()
