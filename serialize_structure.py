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

# enum NodeType
# {
#     S_FuncList = 0,
#     S_Func = 1,
#     CodeBlock = 2,
#     DeclarationList, 3
#     StatementList, 4
#     Declaration, 5
#     ForStmt, 6
#     FuncCall, 7
#     AssignmentExpr, 8
#     BinaryOp, 9
#     Symbol, 10
#     Const, 11
# };
    
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

class S_DeclarationList(Structure):
    structure = (
        ( "type", "<I=2"),
        ( "count", "<I"),
        ( "size", "<I=len(data)"),
        ( "data", ":"), # for declaration in DeclarationList: data+=str(declaration)
    )

class S_StatementList(Structure):
    structure = (
        ( "type", "<I=3"),
        ( "count", "<I"),
        ( "size", "<I=len(data)"),
        ( "data", ":"), # for stmt in StatementList: data+=str(stmt)
    )

class S_CodeBlock(Structure):
    structure = (
        ("type", "<I=1"),
        ("DeclsSize", "<I=len(declaration_list)"),
        ("StmtsSize", "<I=len(statement_list)"),
        ("declaration_list", ":", S_DeclarationList),
        ("statement_list", ":", S_StatementList)
    )

class S_Function(Structure):
    structure = (
        ("type", "<I"),
        ("id", "<I"),
        ("paramsSize", "<I=len(param_list)"),
        ("bodySize", "<I=len(body)"),
        ("param_list", ":", S_DeclarationList),
        ("body", ":", S_CodeBlock)
    )

class S_FuncList(Structure):
    structure = (
        ( "type", "<I"),
        ( "count", "<I"),
        ( "size", "<I=len(data)"),
        ( "data", ":"),
    )

class S_Declaration(Structure):
    structure = (
        ( "type", "<I=4"),
        ( "_type", "<I"), # int : 0, double : 1
        ( "id", "<I"),
    )


class S_ForStmt(Structure):
    structure = (
        ( "type", "<I=5"),
        ( "assigment_expr", ":"),
        ( "bool_expr", ":"),
        ( "assigment_expr", ":")
    )

class S_ReadStmt(Structure):
    structure = (
        ("type", "<I=6"),
        ("id", "<I"),
    )   

class S_WriteStmt(Structure):
    structure = (
        ("type", "<I=7"),
        ("id", "<I"),
    )

class S_AssignmentExpr(Structure):
    structure = (
        ("type", "<I=8"),
        ("id", "<I"),
        ("size", "<I=4*4 + len(exp)"),
        ("exp_size", "<I=len(exp)"),
        ("exp", ":")
    )

class S_BinaryOp(Structure):
    structure = (
        ("type", "<I=9"),
        ("op", "c"),
        ("size", "<I=4*4 + 1 + len(exp1) + len(exp2)"),
        ("exp1_size", "<I=len(exp1)"),
        ("exp2_size", "<I=len(exp2)"),
        ("exp1", ":"),
        ("exp2", ":")
    )

class S_Symbol(Structure):
    structure = (
        ("type", "<I=10"),
        ("_id", "<I"), # id in StringTable
        ("_type", "<I"),
    )

class S_Const(Structure):
    structure = (
        ("type", "<I=11"),
        ("_type", "<I"),
        ("val", "<I"),
    )
