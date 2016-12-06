# -*- coding: utf-8 -*-

class ASTNode(object):
    def __init__(self):
        self.node_name = "ASTNode"

    def show(self):
        print node_name

class AST(object):
    pass

class CodeBlock(ASTNode):
    def __init__(self, declaration_list, statement_list):
        pass

class DeclarationList(ASTNode):
    def __init__(self, declarations, declaration):
        pass

class StatList(object):
    def __init__(self, stats, stat):
        pass

class Declaration(object):
    '''Declaration: Type Assignment SEIM'''
    def __init__(self, ID, Type):
        self._id = ID
        self._type = Type

    def show(self):
        print 'Declaration Node:', self._id, self._type

class Statement(object):
    pass

class IfStat(object):
    pass

class ForStat(object):
    def __init__(self, expr1, expr2, expr3, body):
        pass

    def show(self):
        pass

class ReadStat(object):
    def __init__(self, ID):
        self._id = ID

class WriteStat(object):
    def __init__(self, ID):
        self._id = ID

class BinaryOp(ASTNode):
    def __init__(self, lft, op , rht):
        pass
    
class ExprStat(object):
    pass

class Expr(object):
    pass

class BoolExpr(object):
    pass

class AssigmentExpr(object):
    pass
