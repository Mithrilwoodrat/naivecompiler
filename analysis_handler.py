# -*- coding: utf-8 -*-
import logging
import sys

from visitor import NodeVisitor
from c_ast import *


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
            
    
class LoopHelper(NodeVisitor):
    def __init__(self, parent_scope=None):
        self.scope = parent_scope
        if parent_scope is None:
            self.scope = Scope()
        
    def _has_error(self):
        return self.scope.has_error

    def visit_ContinueStmt(self, node):
        logging.info("continue inside loop!")

    def visit_BreakStmt(self, node):
        logging.info("break inside loop!")

    def visit_Assignment(self, node):
        if type(node.cast_expr) is VariableSymbol:
            self.scope.resolve_symbol(node.cast_expr.name)
        #print node.cast_expr.__class__.__name__
        #self.scope.resolve_symbol(node._id.name)
        
class FuncHelper(NodeVisitor):
    def __init__(self):
        self.scope = Scope()
        
    def _has_error(self):
        return self.scope.has_error
    
    def visit_TypeDecl(self, node):
        # print 'TypeDecl', node.__class__.__name__
        self.scope.define_symbol(node._id.name, node._type)

    def visit_DeclStmt(self, node):
        # self.generic_visit(node.decl)
        self.visit_TypeDecl(node.decl)

    def visit_ArrayDecl(self, node):
        self.scope.define_symbol(node._id.name, node._type)
        
    #def visit_VariableSymbol(self, node):
    #    self.scope.resolve_symbol(node.name)

    def visit_WhileStmt(self, node):
        helper = LoopHelper(parent_scope=self.scope)
        helper.visit(node)
        self.has_error = helper._has_error()
        
    def visit_ContinueStmt(self, node):
        logging.error("continue outside loop!")
        self.scope.has_error = True

    def visit_BreakStmt(self, node):
        logging.error("break outside loop!")
        self.scope.has_error = True
        
    def visit_Assignment(self, node):
        if type(node.cast_expr) is VariableSymbol:
            self.scope.resolve_symbol(node.cast_expr.name)
        #helper = AssignmentExprHelper(self.scope)
        #helper.visit(node)

class AnalysisVisitor(NodeVisitor):
    def __init__(self):
        self.has_error = False

    def _has_error(self):
        return self.has_error

    def visit_FuncDef(self, node):
        helper = FuncHelper()
        helper.visit(node)
        self.has_error = helper.has_error
