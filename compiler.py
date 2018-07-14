#!/usr/bin/env python2.7
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
from ast_rewrite import ReWriteVisitor
from interface import LibNaiveScript
from cfgbuilder import build_cfg


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
        
    def rewrite_ast(self):
        rewriter = ReWriteVisitor()
        rewriter.visit(self.ast, self.ast)

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
    
    def compile(self, pout):
        self.lib = LibNaiveScript('./libNaiveScript.so')
        obj = FileFormat()
        #self.ast = self.minify_ast(self.ast)
        self.ast.show()
        self.rewrite_ast()
        print 'After ReWrite'
        self.ast.show()
        body = self.dump_body()
        stringtable = self.dump_stringtable()
        logger.info("StringTable: %s ,len: %d" % (stringtable, len(stringtable)))
        obj['stringtable'] = stringtable
        obj['body'] = body
        obj[ "bodyMD5" ] = hashlib.md5( str(body) ).digest()
        with open('ns.data','wb') as fout:
            fout.write(str(obj))

        self.lib.LoadData('./ns.data')
        self.lib.Compile(pout)

    
if __name__ == "__main__":
    logging.basicConfig(format='[%(asctime)s] (%(module)s:%(funcName)s:%(lineno)s): <%(levelname)s> %(message)s', level=logging.INFO)
    with open(sys.argv[1]) as f:
        source = f.read()
    compiler = Compiler(source)
    compiler.ast_gen()
    #compiler.analysis()
    if len(sys.argv) == 3:
        compiler.compile(sys.argv[2])
    elif len(sys.argv) == 2:
        compiler.ast.show()
        build_cfg(compiler.ast)
        #compiler.rewrite_ast()
        #print 'After ReWrite'
        #compiler.ast.show()
