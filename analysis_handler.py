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
        #print "define symbol : {0}, type {1}".format(symbol, _type)
        self.symbols[symbol] = _type
        
    def resolve_symbol(self, symbol):
        if symbol not in self.symbols:
            print "error: '{}' undeclared".format(symbol)
            self.has_error = True
            return
        _type = self.symbols[symbol]
        #print "resolve symbol : {0}, type {1}".format(symbol, _type)
        return _type


class AnalysisVisitor(NodeVisitor):
    def __init__(self):
        self.scope = Scope()

    def has_error(self):
        return self.scope.has_error
        
    def visit_Declaration(self, node):
        self.scope.define_symbol(node._id.name, node._type)

    def visit_ReadStmt(self, node):
        self.scope.resolve_symbol(node._id.name)

    def visit_WriteStmt(self, node):
        self.scope.resolve_symbol(node._id.name)
        
    class AssignmentExprHelpr(NodeVisitor):
        ''' resolve VariableSymbol in AssignmentExpr'''
        def __init__(self, scope):
            self.scope = scope
            
        def visit_VariableSymbol(self, node):
            self.scope.resolve_symbol(node.name)
            
    def visit_AssignmentExpr(self, node):
        self.scope.resolve_symbol(node._id.name)
        helper = self.AssignmentExprHelpr(self.scope)
        helper.visit(node) 
        
        
