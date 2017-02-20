# -*- coding: utf-8 -*-
import logging
import sys

logger = logging.getLogger(__file__)

# copy from pycparser
class NodeVisitor(object):
    """ A base NodeVisitor class for visiting c_ast nodes.
        Subclass it and define your own visit_XXX methods, where
        XXX is the class name you want to visit with these
        methods.

        For example:

        class ConstantVisitor(NodeVisitor):
            def __init__(self):
                self.values = []

            def visit_Constant(self, node):
                self.values.append(node.value)

        Creates a list of values of all the constant nodes
        encountered below the given node. To use it:

        cv = ConstantVisitor()
        cv.visit(node)

        Notes:

        *   generic_visit() will be called for AST nodes for which
            no visit_XXX method was defined.
        *   The children of nodes for which a visit_XXX was
            defined will not be visited - if you need this, call
            generic_visit() on the node.
            You can use:
                NodeVisitor.generic_visit(self, node)
        *   Modeled after Python's own AST visiting facilities
            (the ast module of Python 3.0)
    """
    def visit(self, node):
        """ Visit a node.
        """
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """ Called if no explicit visitor function exists for a
            node. Implements preorder visiting of the node.
        """
        for c in node.children():
            #print c.__class__.__name__
            self.visit(c)

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
        
        

