# -*- coding: utf-8 -*-
import logging
import sys
import ctypes
import traceback
from Structure import Structure
#from ctypes import CFUNCTYPE, POINTER, Structure, c_int, c_double, c_uint, c_char_p, c_void_p, c_ulonglong, cast


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
Type_ForStmt =  7
Type_FuncCall =  8
Type_AssignmentExpr = 9
Type_BinaryOp =  10
Type_Symbol = 11
Type_Const = 12

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
        ( "_type", "<I"), # int : 0, double : 1
        ( "id", "<I"),
    )

class S_DeclarationList(Structure):
    structure = (
        ( "type", "<I=%d" % Type_DeclarationList),
        ( "count", "<I"),
        ( "size", "<I=len(data)"),
        ( "data", ":"), # for declaration in DeclarationList: data+=str(declaration)
    )

class S_StatementList(Structure):
    structure = (
        ( "type", "<I=%d" % Type_StatementList),
        ( "count", "<I"),
        ( "size", "<I=len(data)"),
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
        ( "count", "<I"),
        ( "size", "<I=len(data)"),
        ( "data", ":"),
    )

class S_ArgumentList(Structure):
    structure = (
        ( "type", "<I=%d" % Type_ArgumentList),
        ( "count", "<I"),
        ( "size", "<I=len(data)"),
        ( "data", ":"),
    )


class S_ForStmt(Structure):
    structure = (
        ( "type", "<I=%d" % Type_ForStmt),
        ( "assigment_expr", ":"),
        ( "bool_expr", ":"),
        ( "assigment_expr", ":")
    )

    
class S_AssignmentExpr(Structure):
    structure = (
        ("type", "<I=%d" % Type_AssignmentExpr),
        ("size", "<I=4*4 + len(exp)"),
        ("id", "<I"),
        ("exp_size", "<I=len(exp)"),
        ("exp", ":")
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
