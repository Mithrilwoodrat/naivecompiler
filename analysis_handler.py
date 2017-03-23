# -*- coding: utf-8 -*-
import logging
import sys

from visitor import NodeVisitor


logger = logging.getLogger(__file__)


class Scope(object):
    def __init__(self, name="main"):
        self.name = name
        self.symbols = {} # {name: type}
        self.has_error = False

    def get_name(self):
        return self.name

    def define_symbol(self, symbol, _type):
        if symbol in self.symbols:
            print "error : redeclaration of '{}'".format(symbol)
            self.has_error = True
            return
        self.symbols[symbol] = _type
        
    def resolve_symbol(self, symbol):
        if symbol not in self.symbols:
            print "error: '{}' undeclared".format(symbol)
            self.has_error = True
            return
        _type = self.symbols[symbol]
        #print "resolve symbol : {0}, type {1}".format(symbol, _type)
        return _type

class FuncCallHelper(NodeVisitor):
    ''' resolve VariableSymbol in FuncCallxs'''
    def __init__(self, scope):
        self.scope = scope
            
    

class FuncHelper(NodeVisitor):
    def __init__(self):
        self.scope = Scope()
        
    def has_error(self):
        return self.scope.has_error
    
    def visit_Declaration(self, node):
        self.scope.define_symbol(node._id.name, node._type)
        
    def visit_VariableSymbol(self, node):
        self.scope.resolve_symbol(node.name)

    def visit_BreakStmt(self, node):
        pass
        
    # def visit_AssignmentExpr(self, node):
    #     self.scope.resolve_symbol(node._id.name)
    #     helper = AssignmentExprHelper(self.scope)
    #     helper.visit(node)

class AnalysisVisitor(NodeVisitor):
    def __init__(self):
        self._has_error = False

    def has_error(self):
        return self._has_error

    def visit_Function(self, node):
        helper = FuncHelper()
        helper.visit(node)
        self.has_error = helper.has_error

    def visit_BreakStmt(self, node):
        pass
