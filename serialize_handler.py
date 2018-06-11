# -*- coding: utf-8 -*-
from visitor import NodeVisitor
from serialize_structure import *
import logging
import sys

class SerializeHandler(object):
    def __init__(self, env):
        self.env = env

    def serialize(self, node):
        method = 'serialize_' + node.__class__.__name__
        # print method + ' called' 
        visitor = getattr(self, method, self.generic_serialize)
        return visitor(node)

    def generic_serialize(self, node):
        print node.__class__.__name__
        raise NotImplementedError

    def serialize_AST(self, node):
        ast = S_AST()
        ast['count'] = len(node.l)
        data = ''
        for n in node.l:
            # print func.__class__.__name__, len(str(self.serialize(func)))
            data += str(self.serialize(n))
        ast['data'] = data
        return ast

    def unaryop_op_to_int(self, op):
        op_map = {
            '*': 0,
            '&': 1
        }
        if op in op_map:
            return op_map.get(op)
        logging.error('unsupported unary op')

    def type_to_int(self, _type):
        type_map = {
            'int': 0,
            'float': 1,
            'char': 2,
            'string': 3
        }
        if _type in type_map:
            return type_map.get(_type)
        logging.error('unsupported _type')

    def storage_type_to_int(self, _type):
        type_map = {
            'auto': 0,
            'extern': 1,
            'static': 2
        }
        if _type in type_map:
            return type_map.get(_type)
        logging.error('unsupported storage _type')

    def serialize_FuncDef(self, node):
        func = S_FuncDef()
        func['id'] = self.env.add_string(node.function_name.name)
        func['return_type'] = self.type_to_int(node.return_type)
        func['storage_type'] = self.storage_type_to_int(node.storage)
        func['param_list'] = self.serialize(node.param_list)
        func['body'] = self.serialize(node.body)
        return func
        
    def serialize_FuncDecl(self, node):
        func = S_FuncDecl()
        func['id'] = self.env.add_string(node.function_name.name)
        func['return_type'] = self.type_to_int(node.return_type)
        func['storage_type'] = self.storage_type_to_int(node.storage)
        func['param_list'] = self.serialize(node.param_list)
        return func

    def serialize_DeclarationList(self, node):
        decl_list = S_DeclarationList()
        decl_list['count'] = len(node.l)
        data = ''
        for decl in node.l:
            # print decl.__class__.__name__, len(str(self.serialize(decl)))
            data += str(self.serialize(decl))
        decl_list['data'] = data
        return decl_list

    def serialize_TypeDecl(self, node):
        decl_expr =  S_Declaration()
        decl_expr['id'] = self.env.add_string(node._id.name)
        decl_expr['_type'] = 0
        return decl_expr

    def serialize_DeclStmt(self, node):
        return self.serialize(node.decl)
    
    def serialize_StmtList(self, node):
        stmt_list = S_StatementList()
        stmt_list['count'] = len(node.l)
        data = ''
        for stmt in node.l:
            data += str(self.serialize(stmt))
        stmt_list['data'] = data
        return stmt_list

    def serialize_WhileStmt(self, node):
        while_stmt = S_WhileStmt()
        while_stmt['expr'] = self.serialize(node.bool_expr)
        while_stmt['body'] = self.serialize(node.body)
        return while_stmt

    def serialize_IfStmt(self, node):
        if_stmt = S_IfStmt()
        if_stmt['cond'] = self.serialize(node.cond)
        if_stmt['then'] = self.serialize(node.iftrue)
        if_stmt['_else'] = ''
        if node.iffalse:
            if_stmt['_else'] = self.serialize(node.iffalse)
        return if_stmt
        
    def serialize_ArgumentList(self, node):
        arg_list = S_StatementList()
        arg_list['count'] = len(node.l)
        data = ''
        for arg in node.l:
            # print arg.__class__.__name__, len(str(self.serialize(arg)))
            data += str(self.serialize(arg))
        arg_list['data'] = data
        return arg_list

    def serialize_UnaryOp(self, node):
        logging.error("unaryop not supported now!")
        sys.exit(0)
        unaryop = S_UnaryOp()
        op = self.unaryop_op_to_int(node.op)
        unaryop['op'] = op
        unaryop['expr'] = self.serialize(node.expr)
        return unaryop

    def serialize_Assignment(self, node):
        assigment_expr =  S_Assignment()
        if node.cast_expr.__class__.__name__ == 'UnaryOp':
            logging.error("Assignment not support UnaryOp now!")
            sys.exit(0)
        assigment_expr['castexpr'] = self.serialize(node.cast_expr)
        assigment_expr['expr'] = self.serialize(node.rhs)
        return assigment_expr

    def serialize_ReturnStmt(self, node):
        return_statement = S_ReturnStmt()
        return_statement['expr'] = self.serialize(node.expr)
        return return_statement

    def serialize_BreakStmt(self, node):
        return S_BreakStmt()

    def serialize_ContinueStmt(self, node):
        return S_ContinueStmt()

    def serialize_BinaryOp(self, node):
        binary_op = S_BinaryOp()
        binary_op['op'] = node.op
        binary_op['exp1'] = self.serialize(node.lhs)
        binary_op['exp2'] = self.serialize(node.rhs)
        return binary_op

    def serialize_VariableSymbol(self, node):
        symbol = S_Symbol()
        symbol['_id'] = self.env.add_string(node.name)
        symbol['_type'] = node._type
        return symbol
        
    def serialize_Const(self, node):
        print node._type , node.val
        const = S_Const()
        const['_type'] = self.type_to_int(node._type)
        if node._type == "int":
            const['val'] = int(node.val)
        elif node._type == "string":
            const['val'] = self.env.add_string(node.val)
        else:
            logging.error("Const Type:{0} not supported".format(node._type))
        return const

    def serialize_FuncCall(self, node):
        func_call = S_FuncCall()
        func_call['id'] = self.env.add_string(node.func_name.name)
        func_call['argument_list'] = self.serialize(node.argument_list)
        return func_call

    def serialize_Label(self, node):
        label = S_Label()
        label['_id'] = node._id
        return label

    def serialize_ABSJMP(self, node):
        jmp = S_ABSJMP()
        jmp['_id'] = node._id
        return jmp

    def serialize_CMPJMP(self, node):
        jmp = S_CMPJMP()
        jmp['id1'] = node.id1
        jmp['id2'] = node.id2
        jmp['expr']  = self.serialize(node.expr)
        return jmp
