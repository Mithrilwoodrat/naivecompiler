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
# double 1

Type_FuncList = 0
Type_Function = 1
Type_CodeBlock = 2
Type_DeclarationList = 3
Type_StatementList = 4
Type_ArgumentList = 5
Type_Declaration = 6
Type_WhileStmt =  7
Type_IfStmt =  8
Type_FuncCall =  9
Type_AssignmentExpr = 10
Type_ReturnStmt = 11
Type_BreakStmt = 12
Type_ContinueStmt = 13
Type_BinaryOp =  14
Type_Symbol = 15
Type_Const = 16
Type_Label = 17
Type_ABSJMP = 18
Type_CMPJMP = 19

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

class S_Declaration(Structure):
    structure = (
        ( "type", "<I=%d" % Type_Declaration),
        ( "size", "<I=4*4" ),
        ( "_type", "<I"), # int : 0, double : 1
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

class S_CodeBlock(Structure):
    structure = (
        ("type", "<I=%d" % Type_CodeBlock),
        ("DeclsSize", "<I=len(decl_list)"),
        ("StmtsSize", "<I=len(stmt_list)"),
        ("decl_list", ":"),
        ("stmt_list", ":")
    )

class S_Function(Structure):
    structure = (
        ("type", "<I=%d" % Type_Function),
        ("size", "<I=4*6 + len(param_list) + len(body)"),
        ("id", "<I"),
        ("return_type", "<I"),
        ("paramsSize", "<I=len(param_list)"),
        ("bodySize", "<I=len(body)"),
        ("param_list", ":"),
        ("body", ":")
    )

class S_FuncCall(Structure):
    structure = (
        ("type", "<I=%d" % Type_FuncCall),
        ("size", "<I=4*4+len(argument_list)"),
        ("id", "<I"),
        ("argsSize", "<I=len(argument_list)"),
        ("argument_list", ":"),
    )
    
class S_FuncList(Structure):
    structure = (
        ( "type", "<I=%d" % Type_FuncList),
        ( "size", "<I=4*4 + len(data)" ),
        ( "count", "<I"),
        ( "datasize", "<I=len(data)"),
        ( "data", ":"),
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

    
class S_AssignmentExpr(Structure):
    structure = (
        ("type", "<I=%d" % Type_AssignmentExpr),
        ("size", "<I=4*4 + len(expr)"),
        ("id", "<I"),
        ("expr_size", "<I=len(expr)"),
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
