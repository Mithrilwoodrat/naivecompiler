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
            
    
class LoopHelper(NodeVisitor):
    def __init__(self):
        self.scope = Scope()
        
    def has_error(self):
        return self.scope.has_error

    def visit_ContinueStmt(self, node):
        logging.info("continue inside loop!")

    def visit_BreakStmt(self, node):
        logging.info("break inside loop!")
        
class FuncHelper(NodeVisitor):
    def __init__(self):
        self.scope = Scope()
        
    def has_error(self):
        return self.scope.has_error
    
    def visit_TypeDecl(self, node):
        self.scope.define_symbol(node._id.name, node._type)

    def visit_DeclStmt(self, node):
        self.generic_visit(node.decls)

    def visit_ArrayDecl(self, node):
        self.scope.define_symbol(node._id.name, node._type)
        
    def visit_VariableSymbol(self, node):
        self.scope.resolve_symbol(node.name)

    def visit_WhileStmt(self, node):
        helper = LoopHelper()
        helper.visit(node)
        self.has_error = helper.has_error
        
    def visit_ContinueStmt(self, node):
        logging.error("continue outside loop!")
        self.scope.has_error = True

    def visit_BreakStmt(self, node):
        logging.error("break outside loop!")
        self.scope.has_error = True
        
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
