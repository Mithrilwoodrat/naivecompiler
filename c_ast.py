# -*- coding: utf-8 -*-
from serialize_structure import *

class ASTNode(object):
    def __init__(self):
        self.node_name = "ASTNode"

    def show(self):
        print self.node_name

        
class SymbolTable(object):
    pass

class AST(object):
    def __init__(self):
        symbol_table = []

class CodeBlock(ASTNode):
    def __init__(self, declaration_list, statement_list):
        self.node_name = "CodeBlock"
        super(CodeBlock, self).__init__()
        self.declaration_list = declaration_list
        self.statement_list = statement_list

    def show(self):
        print 'CodeBlock'
        self.declaration_list.show()
        self.statement_list.show()

    def serialize(self, env):
        codeblock = S_CodeBlock()
        codeblock['declaration_list'] = self.declaration_list.serialize(env)
        codeblock['statement_list'] = self.statement_list.serialize(env)
        return codeblock

class DeclarationList(ASTNode):
    def __init__(self):
        self.node_name = "DeclarationList"
        self.l = []
        
    def add_declaration(self, d):
        self.l.append(d)

    def __add__(self, rhs):
        if type(rhs) is Declaration:
            self.add_declaration(rhs)
        elif type(rhs) is DeclarationList:
            self.l += rhs.l
        return self

    def show(self):
        print self.node_name
        for n in self.l:
            n.show()

    def serialize(self, env):
        declaration_list = S_DeclarationList()
        declaration_list['count'] = len(self.l)
        data = ''
        for declaration in self.l:
            data += str(declaration.serialize(env))
        declaration_list['data'] = data
        return declaration_list

class StmtList(ASTNode):
    def __init__(self):
        self.node_name = "StmtList"
        self.l = []

    def add_stat(self, s):
        self.l.append(s)

    def __add__(self, rhs):
        if issubclass(rhs.__class__, Statement):
            self.add_stat(rhs)
        elif type(rhs) is StmtList:
            self.l += rhs.l
        return self

    def show(self):
        print self.node_name
        for n in self.l:
            n.show()
    
    def serialize(self, env):
        stmt_list = S_StatementList()
        stmt_list['count'] = len(self.l)
        data = ''
        for stmt in self.l:
            data += str(stmt.serialize(env))
        stmt_list['data'] = data
        return stmt_list

class Declaration(ASTNode):
    '''Declaration: Type Assignment SEIM'''
    def __init__(self, ID, Type):
        self._id = ID
        self._type = Type

    def show(self):
        print 'Declaration Node:', self._id, self._type

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
        declaration['id'] = env.add_string(self._id)
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

class IfStmt(object):
    pass

class ForStmt(Statement):
    def __init__(self, expr1, expr2, expr3, body):
        self.expr1 = expr1
        self.expr2 = expr2
        self.expr3 = expr3
        self.body = body
        self.node_name = "ForStat"

    def show(self):
        print self.node_name
        self.expr1.show()
        self.expr2.show()
        self.expr3.show()
        self.body.show()

    def serialize(self, env):
        pass

class ReadStmt(Statement):
    def __init__(self, ID):
        self._id = ID
        self.node_name = "ReadStat"

    def serialize(self, env):
        readstmt = S_WriteStmt()
        readstmt['id'] = env.add_string(self._id)
        return readstmt

class WriteStmt(Statement):
    def __init__(self, ID):
        self._id = ID
        self.node_name = "WriteStat"

    def serialize(self, env):
        writestmt = S_WriteStmt()
        writestmt['id'] = env.add_string(self._id)
        return writestmt

class AssignmentStmt(Statement):
    def __init__(self, AssignmentExpr):
        self.node_name = "AssigmentStmt"
        self.expr = AssignmentExpr

    def show(self):
        print "AssigmentStmt"
        self.expr.show()

    def serialize(self, env):
        return self.expr.serialize(env)

class AssignmentExpr(ASTNode):
    def __init__(self, _id, rhs):
        self.node_name = "AssignmentExpr"
        self._id = _id
        self.rhs = rhs

    def show(self):
        print "AssignmentExpr", self._id
        self.rhs.show()

    def serialize(self, env):
        assigment_expr =  S_AssignmentExpr()
        assigment_expr['id'] = env.add_string(self._id)
        assigment_expr['exp'] = self.rhs.serialize(env)
        return assigment_expr

class BinaryOp(ASTNode):
    def __init__(self, lhs, op , rhs):
        self.node_name = "BinaryOp"
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def show(self):
        print "BinaryOp"
        self.lhs.show()
        print self.op
        self.rhs.show()

    def serialize(self, env):
        binary_op = S_BinaryOp()
        binary_op['op'] = self.op
        binary_op['exp1'] = str(self.lhs.serialize(env))
        binary_op['exp2'] = str(self.lhs.serialize(env))
        return binary_op
        
class BoolExpr(object):
    def __init__(self, lhs, op , rhs):
        self.node_name = "BoolExpr"
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def show(self):
        print "BoolExpr"
        self.lhs.show()
        print self.op
        self.rhs.show()

    def serialize(self, env):
        raise NotImplementedError


class Symbol(ASTNode):
    def __init__(self, name):
        self.node_name = "Symbol"
        self.name = name
        
    def show(self):
        print self.node_name, self.name

    def serialize(self, env):
        symbol = S_ID()
        symbol['_id'] = env.add_string(self.name)
        return symbol

class Number(ASTNode):
    def __init__(self, val):
        self.node_name = "Number"
        self.val = val
        self._type = 0

    def show(self):
        print self.node_name, self.val

    def serialize(self, env):
        number = S_Number()
        number['val'] = int(self.val)
        number['_type'] = self._type
        return number
