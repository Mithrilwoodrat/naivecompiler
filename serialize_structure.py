# -*- coding: utf-8 -*-
import logging
import sys
import ctypes
import traceback
from Structure import Structure


logger = logging.getLogger(__file__)

# defines
FileMD5Size = 16

#types
# int 0
# float 1
# char  2

#unaryop
# * 0
# & 1

Type_AST = 0
Type_FuncDef = 1
Type_FuncDecl = 2
Type_ArrayDecl = 3
Type_DeclarationList = 4
Type_StatementList = 5
Type_ArgumentList = 6
Type_Declaration = 7
Type_WhileStmt =  8
Type_IfStmt =  9
Type_FuncCall =  10
Type_Assignment = 11
Type_ReturnStmt = 12
Type_BreakStmt = 13
Type_ContinueStmt = 14
Type_BinaryOp =  15
Type_Symbol = 16
Type_Const = 17
Type_Label = 18
Type_ABSJMP = 19
Type_CMPJMP = 20
Type_UnaryOp = 21

## File
  # -------
  # magic
  # entry (of body)
  # bodySize
  # stringtableSize
  # bodyMD5
  # stringtable
  # body
  
class FileFormat(Structure):
    structure = (
        ( "magic", "<I=0"),
        ( "stringTableEntry", "<I=4 * 5 + 16"),
        ( "bodyEntry", "<I=4 * 5 + 16 + len(stringtable)"),
        ( "bodySize", "<I=len(body)"),
        ( "stringtableSize", "<I=len(stringtable)"),
        ( "bodyMD5", "%ds" % FileMD5Size),
        ( "stringtable", ":"),
        ( "body", ":"),
    )

class S_AST(Structure):
    structure = (
        ( "type", "<I=%d" % Type_AST),
        ( "size", "<I=4*4 + len(data)" ),
        ( "count", "<I"),
        ( "datasize", "<I=len(data)"),
        ( "data", ":"), # for stmt in StatementList: data+=str(stmt)
    )


class S_Declaration(Structure):
    structure = (
        ( "type", "<I=%d" % Type_Declaration),
        ( "size", "<I=4*4" ),
        ( "_type", "<I"), # int : 0, float : 1, char: 2
        ( "id", "<I"),
    )

class S_DeclarationList(Structure):
    structure = (
        ( "type", "<I=%d" % Type_DeclarationList),
        ( "size", "<I=4*4 + len(data)" ),
        ( "count", "<I"),
        ( "datasize", "<I=len(data)"),
        ( "data", ":"), # for declaration in DeclarationList: data+=str(declaration)
    )

class S_StatementList(Structure):
    structure = (
        ( "type", "<I=%d" % Type_StatementList),
        ( "size", "<I=4*4 + len(data)" ),
        ( "count", "<I"),
        ( "datasize", "<I=len(data)"),
        ( "data", ":"), # for stmt in StatementList: data+=str(stmt)
    )

class S_FuncDef(Structure):
    structure = (
        ("type", "<I=%d" % Type_FuncDef),
        ("size", "<I=4*7 + len(param_list) + len(body)"),
        ("id", "<I"),
        ("return_type", "<I"),
        ("storage_type", "<I"),
        ("paramsSize", "<I=len(param_list)"),
        ("bodySize", "<I=len(body)"),
        ("param_list", ":"),
        ("body", ":")
    )

class S_FuncDecl(Structure):
    structure = (
        ("type", "<I=%d" % Type_FuncDecl),
        ("size", "<I=4*7 + len(param_list)"),
        ("id", "<I"),
        ("return_type", "<I"),
        ("storage_type", "<I"),
        ("paramsSize", "<I=len(param_list)"),
        ("param_list", ":"),
    )

class S_FuncCall(Structure):
    structure = (
        ("type", "<I=%d" % Type_FuncCall),
        ("size", "<I=4*4+len(argument_list)"),
        ("id", "<I"),
        ("argsSize", "<I=len(argument_list)"),
        ("argument_list", ":"),
    )

class S_ArgumentList(Structure):
    structure = (
        ( "type", "<I=%d" % Type_ArgumentList),
        ( "size", "<I=4*4 + len(data)" ),
        ( "count", "<I"),
        ( "datasize", "<I=len(data)"),
        ( "data", ":"),
    )

class S_IfStmt(Structure):
    structure = (
        ( "type", "<I=%d" % Type_IfStmt),
        ( "size", "<I=4*5 + len(cond) + len(then) + len(_else)"),
        ( "condSize", "<I=len(cond)"),
        ( "thenSize", "<I=len(then)"),
        ( "elseSize", "<I=len(_else)"),
        ( "cond", ":"),
        ( "then", ":"),
        ( "_else", ":")
    )

class S_WhileStmt(Structure):
    structure = (
        ( "type", "<I=%d" % Type_WhileStmt),
        ( "size", "<I=4*4 + len(body) + len(expr)"),
        ( "exprSize", "<I=len(expr)"),
        ( "bodySize", "<I=len(body)"),
        ( "expr", ":"),
        ( "body", ":")
    )

class S_UnaryOp(Structure):
    structure = (
        ("type", "<I=%d" % Type_UnaryOp),
        ("size", "<I=4*4 + len(expr)"),
        ("op", "<I"),
        ("exprSize", "<I=len(expr)"),
        ("expr", ":")
    )
    
class S_Assignment(Structure):
    structure = (
        ("type", "<I=%d" % Type_Assignment),
        ("size", "<I=4*4 + len(castexpr) + len(expr)"),
        ("castexprSize", "<I=len(castexpr)"),
        ("exprSize", "<I=len(expr)"),
        ("castexpr", ":"),
        ("expr", ":")
    )

class S_ReturnStmt(Structure):
    structure = (
        ("type", "<I=%d" % Type_ReturnStmt),
        ("size", "<I=4*3 + len(expr)"),
        ("expr_size", "<I=len(expr)"),
        ("expr", ":")
    )

class S_BreakStmt(Structure):
    structure = (
        ("type", "<I=%d" % Type_BreakStmt),
        ("size", "<I=4*2"),
    )

class S_ContinueStmt(Structure):
    structure = (
        ("type", "<I=%d" % Type_ContinueStmt),
        ("size", "<I=4*2"),
    )
    
class S_BinaryOp(Structure):
    structure = (
        ("type", "<I=%d" % Type_BinaryOp),
        ("size", "<I=4*4 + 1 + len(exp1) + len(exp2)"),
        ("exp1_size", "<I=len(exp1)"),
        ("exp2_size", "<I=len(exp2)"),
        ("op", "c"),
        ("exp1", ":"),
        ("exp2", ":")
    )

class S_Symbol(Structure):
    structure = (
        ("type", "<I=%d" % Type_Symbol),
        ("_id", "<I"), # id in StringTable
        ("_type", "<I"),
    )

class S_Const(Structure):
    structure = (
        ("type", "<I=%d" % Type_Const),
        ("_type", "<I"),
        ("val", "<I"),
    )

class S_Label(Structure):
    structure = (
        ("type", "<I=%d" % Type_Label),
        ("size", "<I=4*3"),
        ("_id", "<I"),
    )

class S_ABSJMP(Structure):
    structure = (
        ("type", "<I=%d" % Type_ABSJMP),
        ("size", "<I=4*3"),
        ("_id", "<I"),
    )

class S_CMPJMP(Structure):
    structure = (
        ("type", "<I=%d" % Type_CMPJMP),
        ("size", "<I=4*5 + len(expr)"),
        ("exprSize", "<I=len(expr)"),
        ("id1", "<I"),
        ("id2", "<I"),
        ("expr", ":"),
    )
