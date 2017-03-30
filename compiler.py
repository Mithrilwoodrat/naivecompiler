# -*- coding: utf-8 -*-
import logging
import sys
import ctypes
import traceback
import hashlib
from c_parser import Parser
from c_ast import *
from serialize_structure import FileFormat
from analysis_handler import AnalysisVisitor
from serialize_handler import SerializeHandler
from irgen import IRGenVisitor


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
            # logging.info("add symbol: {}".format(string))
            return old_index
        # logging.info("get symbol: {}".format(string))
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
        if self.ast is None:
            logger.error('Parsing Failed')
            return False
        # self.ast.show()
        return True

    def minify_ast(self, ast):
        ''' 
        minify for codegen. 
        '''
        assert ast.__class__.__name__ == 'AST'
        return ast.root

    def analysis(self):
        if self.ast is None:
            return
        av = AnalysisVisitor()
        av.visit(self.ast)
        if av.has_error():
            logger.error('Compile Failed')
            return False
        return True

    def dump_stringtable(self):
        string_table = self.env.string_table
        data = ''
        for string in string_table.table:
            data += string + '\0'
        print 'dumped stringtable:',
        for c in data:
            print '%x' % ord(c),
        print
        return data

    def dump_body(self):
        sh = SerializeHandler(self.env)
        return sh.serialize(self.ast)
    
    def compile(self):
        obj = FileFormat()
        self.ast = self.minify_ast(self.ast)
        #self.ast.show()
        body = self.dump_body()
        stringtable = self.dump_stringtable()
        logger.info("StringTable: %s ,len: %d" % (stringtable, len(stringtable)))
        obj['stringtable'] = stringtable
        obj['body'] = body
        obj[ "bodyMD5" ] = hashlib.md5( str(body) ).digest()
        with open('ns.data','wb') as fout:
            fout.write(str(obj))

        irgen = IRGenVisitor()
        irgen.visit(self.ast)
    
if __name__ == "__main__":
    logging.basicConfig(format='[%(asctime)s] (%(module)s:%(funcName)s:%(lineno)s): <%(levelname)s> %(message)s', level=logging.INFO)
    with open(sys.argv[1]) as f:
        source = f.read()
    compiler = Compiler(source)
    compiler.ast_gen()
    compiler.analysis()
    compiler.compile()
