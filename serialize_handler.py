# -*- coding: utf-8 -*-
from visitor import NodeVisitor
from serialize_structure import *

class SerializeHandler(object):
    def __init__(self, env):
        self.env = env

    def serialize(self, node):
        method = 'serialize_' + node.__class__.__name__
        print method + ' called' 
        visitor = getattr(self, method, self.generic_serialize)
        return visitor(node)

    def generic_serialize(self, node):
        print node.__class__.__name__
        raise NotImplementedError
    
    def serialize_StmtList(self, node):
        stmt_list = S_StatementList()
        stmt_list['count'] = len(node.l)
        data = ''
        for stmt in node.l:
            print stmt.__class__.__name__, len(str(self.serialize(stmt)))
            data += str(self.serialize(stmt))
            stmt_list['data'] = data
        return stmt_list

    def serialize_WriteStmt(self, node):
        writestmt = S_WriteStmt()
        writestmt['id'] = self.env.add_string(node._id.name)
        return writestmt

    def serialize_AssignmentStmt(self, node):
        return self.serialize(node.expr)

    def serialize_AssignmentExpr(self, node):
        assigment_expr =  S_AssignmentExpr()
        assigment_expr['id'] = self.env.add_string(node._id.name)
        assigment_expr['exp'] = self.serialize(node.rhs)
        return assigment_expr

    def serialize_BinaryOp(self, node):
        binary_op = S_BinaryOp()
        binary_op['op'] = node.op
        binary_op['exp1'] = str(self.serialize(node.lhs))
        binary_op['exp2'] = str(self.serialize(node.rhs))
        return binary_op

    def serialize_VariableSymbol(self, node):
        symbol = S_Symbol()
        symbol['_id'] = self.env.add_string(node.name)
        symbol['_type'] = node._type
        return symbol
        
    def serialize_Number(self, node):
        number = S_Number()
        number['val'] = int(node.val)
        number['_type'] = node._type
        return number
        
