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
import optparse

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
    def __init__(self):
        self.parser = Parser()
        self.env = Env()
        self.source = None
        self.ast = None

    def parse(self, source):
        with open(source) as f:
            self.source = f.read()
        self.ast_gen()

    def ast_gen(self):
        self.ast = self.parser.parse(self.source)
        if self.ast is None:
            logger.error('Parsing Failed')
            return False
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

    def show_ast(self):
        self.ast.show()

    def build_cfg(self):
        self.cfgs = build_cfg(self.ast)

    def show_cfg(self):
        for func in self.cfgs:
            print 'Func ', func.function_name    .name
            self.cfgs[func].show()

    def build_basic_blocks(self):
        nodes = self.ast.l
        for i in range(len(nodes)):
            node = nodes[i]
            if node.__class__ is FuncDef:
                cfg = self.cfgs[node]
                stmts = self.merge_cfg(cfg)
                stmt_list = StmtList()
                stmt_list.l = stmts
                nodes[i].body = stmt_list

    Terminator_STMTS = ["ABSJMP", "CMPJMP"]

    def is_terminator_stmt(self, stmt):
        return stmt.__class__.__name__ in self.Terminator_STMTS

    # TODO: merge cfg for code gen
    def merge_cfg(self, cfg):
        bbs = {}
        blocks = cfg.blocks
        terminated = False
        last_stmt = None
        for block in blocks:
            stmts = []
            if len(block.stmts) != 0:
                if terminated:
                    stmts.append(Label(block.block_id))
                terminated = False
                stmts.extend(block.stmts)
                last_stmt = block.stmts[-1]
                if self.is_terminator_stmt(last_stmt):
                    if last_stmt.__class__.__name__ == "ABSJMP":
                        if bbs.has_key(last_stmt._id) and bbs[last_stmt._id][0].__class__ is not Label:
                            bbs[last_stmt._id].insert(0, Label(last_stmt._id))
                        else:
                            bbs[last_stmt._id] = [Label(last_stmt._id)]
                    elif last_stmt.__class__.__name__ == "CMPJMP":
                        if bbs.has_key(last_stmt.id1) and bbs[last_stmt.id1][0].__class__ is not Label:
                            bbs[last_stmt.id1].insert(0, Label(last_stmt.id1))
                        else:
                            bbs[last_stmt.id1] = [Label(last_stmt.id1)]
                        if bbs.has_key(last_stmt.id2) and bbs[last_stmt.id2][0].__class__ is not Label:
                            bbs[last_stmt.id2].insert(0, Label(last_stmt.id2))
                        else:
                            bbs[last_stmt.id2] = [Label(last_stmt.id2)]
                    terminated = True
                bbs[block.block_id] = stmts
        stmts = []
        bbids = bbs.keys()
        bbids.sort()
        for block in blocks:
            if block.block_id in bbs:
                stmts.extend(bbs[block.block_id])
        return stmts

    def old_compile(self, pout):
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

    def compile(self, pout):
        self.lib = LibNaiveScript('./libNaiveScript.so')
        obj = FileFormat()
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

def parse_opt():
    usage = "usage: %prog [options] sourcefile.."
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-o', dest="fout", help="output file")
    parser.add_option('--show-ast', dest="show_ast", action="store_true", default=False, help="show ast")
    parser.add_option('--show-cfg', dest="show_cfg", action="store_true", default=False, help="show cfg")

    options, remainder = parser.parse_args()
    if len(remainder) == 0:
        parser.print_help()
        sys.exit(0)

    return options, remainder

def main():
    options, sources = parse_opt()
    source = sources[0]
    compiler = Compiler()
    compiler.parse(source)

    if options.show_ast or options.show_cfg:
        if options.show_ast:
            print '----------- show ast ------------'
            compiler.show_ast()
        if options.show_cfg:
            print '----------- show cfg ------------'
            compiler.build_cfg()
            compiler.show_cfg()
        sys.exit(0)

    fout = source.split('.')[0] + '.o'
    if options.fout:
        fout = options.fout
    # compiler.analysis()
    compiler.build_cfg()
    compiler.build_basic_blocks()
    compiler.show_ast()
    compiler.compile(fout)


    
if __name__ == "__main__":
    logging.basicConfig(format='[%(asctime)s] (%(module)s:%(funcName)s:%(lineno)s): <%(levelname)s> %(message)s', level=logging.INFO)
    main()
    # with open(sys.argv[1]) as f:
    #     source = f.read()
    # compiler = Compiler(source)
    # compiler.ast_gen()
    # #compiler.analysis()
    # if len(sys.argv) == 3:
    #     compiler.compile(sys.argv[2])
    # elif len(sys.argv) == 2:
    #     compiler.ast.show()
    #     build_cfg(compiler.ast)
        #compiler.rewrite_ast()
        #print 'After ReWrite'
        #compiler.ast.show()
