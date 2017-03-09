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

    def serialize_FuncList(self, node):
        func_list = S_FuncList()
        func_list['count'] = len(node.l)
        data = ''
        for func in node.l:
            print func.__class__.__name__, len(str(self.serialize(func)))
            data += str(self.serialize(func))
            func_list['data'] = data
        return func_list

    def serialize_Function(self, node):
        func = S_Function()
        func['id'] = node.function_name.name
        func['return_type'] = 0
        func['param_list'] = self.serialize(node.param_list)
        func['body'] = self.serialize(node.body)

    def serialize_CodeBlock(self, node):
        code_block = S_CodeBlock()
        code_block['decl_list'] = self.serialize(node.decl_list)
        code_block['stmt_list'] = self.serialize(node.stmt_list)

    def serialize_DeclarationList(self, node):
        decl_list = S_DeclarationList()
        decl_list['count'] = len(node.l)
        data = ''
        for decl in node.l:
            print decl.__class__.__name__, len(str(self.serialize(decl)))
            data += str(self.serialize(decl))
            decl_list['data'] = data
        return decl_list

    def serialize_Declaration(self, node):
        decl_expr =  S_Declaration()
        decl_expr['id'] = self.env.add_string(node._id.name)
        decl_expr['_type'] = 0
        return decl_expr
    
    def serialize_StmtList(self, node):
        stmt_list = S_StatementList()
        stmt_list['count'] = len(node.l)
        data = ''
        for stmt in node.l:
            print stmt.__class__.__name__, len(str(self.serialize(stmt)))
            data += str(self.serialize(stmt))
            stmt_list['data'] = data
        return stmt_list

    def serialize_ArgumentList(self, node):
        arg_list = S_StatementList()
        arg_list['count'] = len(node.l)
        data = ''
        for arg in node.l:
            print arg.__class__.__name__, len(str(self.serialize(arg)))
            data += str(self.serialize(arg))
            arg_list['data'] = data
        return arg_list
        

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
        
    def serialize_Const(self, node):
        const = S_Const()
        const['val'] = int(node.val)
        const['_type'] = node._type
        return const

    def serialize_FuncCall(self, node):
        func_call = S_FuncCall()
        func_call['id'] = node.func_name.name
        func_call['argument_list'] = self.serialize(node.argument_list)

