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
        if argument:
            self.l = [argument]
        else:
            self.l = []

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
        
class CodeBlock(ASTNode):
    def __init__(self, declaration_list, statement_list):
        self.node_name = "CodeBlock"
        super(CodeBlock, self).__init__()
        self.decl_list = declaration_list
        self.stmt_list = statement_list

    def children(self):
        return [self.decl_list, self.stmt_list]

    def serialize(self, env):
        codeblock = S_CodeBlock()
        codeblock['declaration_list'] = self.declaration_list.serialize(env)
        codeblock['statement_list'] = self.statement_list.serialize(env)
        return codeblock

class DeclarationList(ASTNode):
    def __init__(self, declaration=None):
        self.node_name = "DeclarationList"
        if declaration is None:
            self.l = []
        elif type(declaration) is Declaration:
            self.l = [declaration]
        else:
            logger.error('Initial with error type')
        
    def add_declaration(self, d):
        self.l.append(d)

    def __add__(self, rhs):
        if type(rhs) is Declaration:
            self.add_declaration(rhs)
        elif type(rhs) is DeclarationList:
            self.l += rhs.l
        return self

    def children(self):
        return self.l

    def serialize(self, env):
        declaration_list = S_DeclarationList()
        declaration_list['count'] = len(self.l)
        data = ''
        for declaration in self.l:
            data += str(declaration.serialize(env))
        declaration_list['data'] = data
        return declaration_list

class StmtList(ASTNode):
    def __init__(self, stmt):
        self.node_name = "StmtList"
        if 'Stmt' in stmt.__class__.__name__:
            self.l = [stmt]
        else:
            logger.error('Initial with error type: {0}'.format(stmt.__class__))

    def add_stat(self, s):
        self.l.append(s)

    def __add__(self, rhs):
        if issubclass(rhs.__class__, Statement):
            self.add_stat(rhs)
        elif type(rhs) is StmtList:
            self.l += rhs.l
        return self

    def children(self):
        return self.l
    
    def serialize(self, env):
        stmt_list = S_StatementList()
        stmt_list['count'] = len(self.l)
        data = ''
        for stmt in self.l:
            data += str(stmt.serialize(env))
        stmt_list['data'] = data
        return stmt_list

class Declaration(ASTNode):
    '''Declaration: Type ID SEIM'''
    attr_names = ('_type', )
    def __init__(self, ID, Type):
        self._id = ID
        self._type = Type

    def children(self):
        return [self._id]

    def __add__(self, rhs):
        declaration_list = DeclarationList()
        if type(rhs) is DeclarationList:
            rhs.add_declaration(self)
            return rhs
        else:
            declaration_list.add_declaration(self)
            declaration_list.add_declaration(rhs)
            return declaration_list

    def serialize(self, env):
        declaration = S_Declaration()
        declaration['_type'] = 0
        declaration['id'] = env.add_string(self._id.name)
        return declaration
        

class Statement(ASTNode):
    def __add__(self, rhs):
        stat_list = StmtList()
        if type(rhs) is StmtList:
            rhs.add_stat(self)
            return rhs
        else:
            stat_list.add_stat(self)
            stat_list.add_stat(rhs)
        return stat_list


class FuncCall(Statement):
    def __init__(self, func_name, argument_list):
        self.func_name = func_name
        self.argument_list = argument_list
    
    def children(self):
        return [self.func_name, self.argument_list]


class IfStmt(object):
    pass

class ForStmt(Statement):
    def __init__(self, expr1, expr2, expr3, body):
        self.assigment_expr1 = expr1
        self.bool_expr = expr2
        self.assigment_expr2 = expr3
        self.body = body
        self.node_name = "ForStat"

    def children(self):
        return [self.assigment_expr1,
                self.bool_expr,
                self.assigment_expr2,
                self.body]


    def serialize(self, env):
        raise NotImplementedError

class ReadStmt(Statement):
    def __init__(self, ID):
        self._id = ID
        self.node_name = "ReadStat"

    def serialize(self, env):
        readstmt = S_WriteStmt()
        readstmt['id'] = env.add_string(self._id.name)
        return readstmt

    def children(self):
        return [self._id]

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

    def serialize(self, env):
        binary_op = S_BinaryOp()
        binary_op['op'] = self.op
        binary_op['exp1'] = str(self.lhs.serialize(env))
        binary_op['exp2'] = str(self.lhs.serialize(env))
        return binary_op
        
class BoolExpr(ASTNode):
    attr_names = ('op',)
    def __init__(self, lhs, op , rhs):
        self.node_name = "BoolExpr"
        self.lhs = lhs
        self.op = op
        self.rhs = rhs
    
    def children(self):
        return [self.lhs, self.rhs]

    def serialize(self, env):
        raise NotImplementedError

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
    attr_names = ('val',)
    def __init__(self, val):
        self.node_name = "const"
        self.val = val
        self._type = 0
        
    def children(self):
        return []
