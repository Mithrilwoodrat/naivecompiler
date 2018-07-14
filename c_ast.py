# -*- coding: utf-8 -*-
import sys
import logging


class ASTNode(object):
    attr_names = ()
    def __init__(self):
        self.node_name = "ASTNode"
        
    def show(self, buf=sys.stdout, offset=0):
        buf.write(' '*offset + self.__class__.__name__+ ': ')
        
        if self.attr_names:
            nvlist = [(n, getattr(self,n)) for n in self.attr_names]
            attrstr = ', '.join('%s=%s' % nv for nv in nvlist)
            buf.write(attrstr)
        buf.write('\n')
        
        for  child in self.children():
            child.show(offset = offset + 2)

    def children(self):
        raise NotImplementedError


class AST(ASTNode):
    def __init__(self, trans_unit):
        self.l = [trans_unit]

    def children(self):
        return self.l
    
    
class ArgumentList(ASTNode):
    def __init__(self, argument=None):
        if argument is None:
            self.l = []
        elif type(argument) in frozenset([VariableSymbol, Const]):
            self.l = [argument]
        else:
            logging.error('Initial with error type')


    def children(self):
        return self.l


class FuncDecl(ASTNode):
    attr_names = ('return_type', 'storage')
    def __init__(self, return_type, function_name, param_list, storage='extern'):
        super(FuncDecl, self).__init__()
        self.storage = storage
        self.return_type = return_type
        self.function_name = function_name
        self.param_list = param_list

    def children(self):
        return [self.function_name, self.param_list]

    
class FuncDef(ASTNode):
    attr_names = ('return_type', 'storage')
    def __init__(self, return_type, function_name, param_list, body, storage='extern'):
        self.node_name = "FuncDef"
        super(FuncDef, self).__init__()
        self.return_type = return_type
        self.function_name = function_name
        self.param_list = param_list
        self.body = body
        self.storage = storage

    def children(self):
        return [self.function_name, self.param_list, self.body]
        

class DeclarationList(ASTNode):
    decl_types = ["TypeDecl", "ArrayDecl", "FuncDecl"]
    def __init__(self, decl=None):
        self.node_name = "DeclarationList"
        if decl is None:
            self.l = []
        elif decl.__class__.__name__ in self.decl_types:
            self.l = [decl]
        else:
            logging.error('Initial with error type,decl: {}'.format(decl))
        
    def add_declaration(self, d):
        self.l.append(d)

    def __add__(self, rhs):
        if rhs.__class__.__name__ in self.decl_types:
            self.add_declaration(rhs)
        elif type(rhs) is DeclarationList:
            self.l += rhs.l
        return self

    def children(self):
        return self.l


class StmtList(ASTNode):
    def __init__(self, stmt=None):
        self.node_name = "StmtList"
        if stmt is None:
            self.l = []
        elif  issubclass(stmt.__class__, Statement):
            self.l = [stmt]
        else:
            logging.error('Initial with error type: {0}'.format(stmt.__class__))

    def add_stmt(self, s):
        self.l.append(s)

    def __add__(self, rhs):
        if issubclass(rhs.__class__, Statement):
            self.add_stat(rhs)
        elif type(rhs) is StmtList:
            self.l += rhs.l
        return self

    def children(self):
        return self.l

# Decl:
# name: the variable being declared
# quals: list of qualifiers (const, volatile)
# funcspec: list function specifiers (i.e. inline in C99)
# storage: list of storage specifiers (static, auto, extern, register, etc.)
# type: declaration type (probably nested with all the modifiers)
# init: initialization value, or None
# bitsize: bit field size, or None

class TypeDecl(ASTNode):
    '''Declaration: storage type name init
    '''
    attr_names = ('_type', 'storage')
    def __init__(self, _type, _id, init=None, storage='auto'):
        self.storage = storage
        self._id = _id
        self._type = _type
        self.init = init

    def children(self):
        if self.init:
            return [self._id, self.init]
        return [self._id]

    def __add__(self, rhs):
        decls = DeclarationList(self)
        return decls + rhs


class ArrayDecl(ASTNode):
    attr_names = ('_type', 'length')
    def __init__(self, _type, _id, length, init=None, storage='auto'):
        self.storage = storage
        self._id = _id
        self._type = _type
        self.length = length
        self.init = init

    def children(self):
        if self.init:
            return [self._id, self.init]
        return [self._id]

    def __add__(self, rhs):
        decls = DeclarationList(self)
        return decls + rhs


class Statement(ASTNode):
    def __init__(self):
        pass
    
    def __add__(self, rhs):
        stmts = StmtList(self)
        return stmts + rhs

    def children(self):
        return []

class DeclStmt(Statement):
    ''' DeclStmt: Decl SEIM '''
    def __init__(self, decl):
        self.decl = decl

    def children(self):
        return [self.decl]

class FuncCall(Statement):
    def __init__(self, func_name, argument_list):
        self.func_name = func_name
        self.argument_list = argument_list
    
    def children(self):
        return [self.func_name, self.argument_list]


class IfStmt(Statement):
    def __init__(self, cond, then, _else=None):
        self.cond = cond
        self.then = then
        self._else = _else

    def children(self):
        if self._else is None:
            return [self.cond, self.then]
        return [self.cond, self.then, self._else]
    

class WhileStmt(Statement):
    def __init__(self, expr, body):
        self.cond_expr = expr
        self.body = body
        self.node_name = "ForStat"

    def children(self):
        return [self.cond_expr, self.body]
    

class ReturnStmt(Statement):
    def __init__(self, expr=None):
        self.expr = expr

    def children(self):
        if self.expr is None:
            return []
        return [self.expr]

    
class Assignment(Statement):
    def __init__(self, cast_expr, rhs):
        self.cast_expr = cast_expr
        self.rhs = rhs

    def children(self):
        return [self.cast_expr, self.rhs]


class BinaryOp(ASTNode):
    attr_names = ('op',)
    def __init__(self, lhs, op , rhs):
        self.node_name = "BinaryOp"
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def is_logicalOp(self):
        return self.op == '&&' or self.op == "||"

    def is_compareOp(self):
        return self.op in [">", "<", ">=", "<=", "==", "!="]

    def children(self):
        return [self.lhs, self.rhs]

class UnaryOp(ASTNode):
    attr_names = ('op',)
    def __init__(self, op, expr):
        self.node_name = "UnaryOp"
        self.op = op
        self.expr = expr

    def children(self):
        return [self.expr]


class BreakStmt(Statement):
    pass

class ContinueStmt(Statement):
    pass


class Symbol(ASTNode):
    attr_names = ('name', )
    def __init__(self, name):
        self.node_name = "Symbol"
        self.name = name
        self._type = 0

    def children(self):
        return []

class MethodSymbol(Symbol):
    attr_names = ('name',)
    def __init__(self, name):
        super(MethodSymbol, self).__init__(name)
        self.node_name = "MethodSymbol"


class VariableSymbol(Symbol):
    attr_names = ('name',)
    def __init__(self, name):
        super(VariableSymbol, self).__init__(name)
        self.node_name = "VariableSymbol"

class Const(ASTNode):
    attr_names = ('_type', 'val',)
    def __init__(self, _type, val):
        self.node_name = "const"
        self.val = val
        self._type = _type
        
    def children(self):
        return []


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
