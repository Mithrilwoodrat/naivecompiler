# -*- coding: utf-8 -*-
import sys
import logging
from serialize_structure import *

logger = logging.getLogger(__file__)

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
    def __init__(self, root):
        self.root = root

    def children(self):
        return [self.root]
    
    
class ArgumentList(ASTNode):
    def __init__(self, argument=None):
        if argument is None:
            self.l = []
        elif type(argument) in frozenset([VariableSymbol, Const]):
            self.l = [argument]
        else:
            logger.error('Initial with error type')


    def children(self):
        return self.l

    
class Function(ASTNode):
    attr_names = ('return_type', )
    def __init__(self, return_type, function_name, param_list, body):
        self.node_name = "FuncDef"
        super(Function, self).__init__()
        self.return_type = return_type
        self.function_name = function_name
        self.param_list = param_list
        self.body = body

    def children(self):
        return [self.function_name, self.param_list, self.body]

    
class FuncList(ASTNode):
    def __init__(self, funcdef):
        self.node_name = "FuncList"
        if type(funcdef) is Function:
            self.l = [funcdef]
        else:
            logger.error('Initial with error type: {0}'.format(funcdef))
        
    def add_funcdef(self, f):
        self.l.append(f)

    def __add__(self, rhs):
        if type(rhs) is Function:
            self.add_funcdef(rhs)
        elif type(rhs) is FuncList:
            self.l += rhs.l
        return self

    def children(self):
        return self.l
        
# class CodeBlock(ASTNode):
#     def __init__(self, declaration_list, statement_list):
#         self.node_name = "CodeBlock"
#         super(CodeBlock, self).__init__()
#         self.decl_list = declaration_list
#         self.stmt_list = statement_list

#     def children(self):
#         return [self.decl_list, self.stmt_list]

#     def serialize(self, env):
#         codeblock = S_CodeBlock()
#         codeblock['declaration_list'] = self.declaration_list.serialize(env)
#         codeblock['statement_list'] = self.statement_list.serialize(env)
#         return codeblock

class DeclarationList(ASTNode):
    decl_types = ["TypeDecl", "ArrayDecl"]
    def __init__(self, decl=None):
        self.node_name = "DeclarationList"
        if decl is None:
            self.l = []
        elif decl.__class__.__name__ in self.decl_types:
            self.l = [decl]
        else:
            logger.error('Initial with error type')
        
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
            logger.error('Initial with error type: {0}'.format(stmt.__class__))

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
# storage: list of storage specifiers (extern, register, etc.)
# type: declaration type (probably nested with all the modifiers)
# init: initialization value, or None
# bitsize: bit field size, or None
    
class TypeDecl(ASTNode):
    '''Declaration: storage type name init
    '''
    attr_names = ('_type', )
    def __init__(self, _type, _id, init=None, storage='local'):
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
    def __init__(self, _type, _id, length, init=None, storage='local'):
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
    ''' DeclStmt: DeclExpr SEIM '''
    def __init__(self, decls):
        self.decls = decls

    def children(self):
        return [self.decls]

class FuncCall(Statement):
    def __init__(self, func_name, argument_list):
        self.func_name = func_name
        self.argument_list = argument_list
    
    def children(self):
        return [self.func_name, self.argument_list]


class IfStmt(Statement):
    def __init__(self, cond, iftrue, iffalse=None):
        self.cond = cond
        self.iftrue = iftrue
        self.iffalse = iffalse

    def children(self):
        if self.iffalse is None:
            return [self.cond, self.iftrue]
        return [self.cond, self.iftrue, self.iffalse]
    

class WhileStmt(Statement):
    def __init__(self, expr, body):
        self.bool_expr = expr
        self.body = body
        self.node_name = "ForStat"

    def children(self):
        return [self.bool_expr, self.body]
    

class ReturnStmt(Statement):
    def __init__(self, expr):
        self.expr = expr

    def children(self):
        return [self.expr]

    
class AssignmentStmt(Statement):
    def __init__(self, AssignmentExpr):
        self.node_name = "AssigmentStmt"
        self.expr = AssignmentExpr

    def children(self):
        return [self.expr]

    def serialize(self, env):
        return self.expr.serialize(env)

class AssignmentExpr(ASTNode):
    def __init__(self, _id, rhs):
        self.node_name = "AssignmentExpr"
        self._id = _id
        self.rhs = rhs

    def children(self):
        return [self._id, self.rhs]

    def serialize(self, env):
        assigment_expr =  S_AssignmentExpr()
        assigment_expr['id'] = env.add_string(self._id.name)
        assigment_expr['exp'] = self.rhs.serialize(env)
        return assigment_expr

class BinaryOp(ASTNode):
    attr_names = ('op',)
    def __init__(self, lhs, op , rhs):
        self.node_name = "BinaryOp"
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

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
    
    def serialize(self, env):
        symbol = S_Symbol()
        symbol['_id'] = env.add_string(self.name)
        symbol['_type'] = self._type
        return symbol

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
