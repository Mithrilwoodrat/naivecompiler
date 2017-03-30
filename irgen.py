# -*- coding: utf-8 -*-
import logging
import sys

from visitor import NodeVisitor
from c_ast import ASTNode, Const


logger = logging.getLogger(__file__)


class Label(ASTNode):
    attr_names = ('name', )
    def __init__(self, _id):
        self._id = _id
        self.name = 'L' + str(_id)

    def children(self):
        return []

class ABSJMP(ASTNode):
    attr_names = ('_id', )
    def __init__(self, _id):
        self._id = _id

    def children(self):
        return []

class CMPJMP(ASTNode):
    attr_names = ('id1', 'id2')
    def __init__(self, expr, id1, id2):
        self.expr = expr
        self.id1 = id1
        self.id2 = id2

    def children(self):
        return [self.expr]

LabelId = 0

def LabelIDGen():
    global LabelId
    LabelId += 1
    return LabelId

class LoopBlock(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
class FuncHelper(NodeVisitor):
    def __init__(self):
        self.block_stack = []

    def gen_while(self, node):
        stmts =  node.children()
        for stmt in stmts:
            if stmt.__class__.__name__ == "WhileStmt":
                print "While"
                index = node.l.index(stmt)
                L1ID = LabelIDGen()
                L1 = Label(L1ID)
                L2ID = LabelIDGen()
                L2 = Label(L2ID)
                block = LoopBlock(L1, L2)
                self.block_stack.append(block)
                cmpstmt = CMPJMP(stmt.bool_expr, L1ID, L2ID)
                beforestmts = stmts[:index]
                afterstmts = stmts[index+1:]
                newstmts = []
                newstmts.append(L1)
                newstmts.append(cmpstmt)
                newstmts.extend(stmt.body.l)
                newstmts.append(cmpstmt)
                newstmts.append(L2)
                node.l = beforestmts + newstmts + afterstmts

    def gen_break(self, node):
        stmts =  node.children()
        for stmt in stmts:
            if stmt.__class__.__name__ == "BreakStmt":
                print "BreakStmt"
                jmpstmt = ABSJMP(self.block_stack[-1].end._id)
                index = node.l.index(stmt)
                node.l[index] = jmpstmt
                
    def visit_StmtList(self, node):
        self.gen_while(node)
        self.gen_break(node)
        if self.block_stack:
            self.block_stack.pop()
        node.show()

    def visit_IfStmt(self, node):
        pass

        #node.show()
            


class IRGenVisitor(NodeVisitor):
    def __init__(self):
        pass

    def visit_Function(self, node):
        helper = FuncHelper()
        helper.visit(node)
