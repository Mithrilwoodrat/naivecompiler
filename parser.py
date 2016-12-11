# -*- coding: utf-8 -*-
from ply import lex, yacc
from ast import *

keywords = {
    "if":'IF',
    "else":"ELSE",
    "for":"FOR",
    "int":"INT",
    "read":"READ",
    "write":"WRITE"}
singlewords = ('{', '}', '(', ')' , ';')
binop = ('+', '-', '*', '/', '=', '>', '<')
doubleword = ('>=', '<=', '!=')
comment = ('/*', '*/')
tokens = (
    "IF", "ELSE", 'FOR','INT', 'READ', 'WRITE',
    "ID", "NUM", "NORMSTRING",
    "PLUS", "MINUS", "TIMES", "DIVIDES", "EQUALS", "GT", "LT", "AND", "OR",
    "GE", 'LE', 'NE',
    "LBRACE", "RBRACE", "LPAREN","RPAREN","SEMI",
    "COMMENTS"
)

t_IF = r'if'
t_ELSE = r'else'
t_FOR = r'for'
t_INT = r'int'
t_READ = r'read'
t_WRITE = r'write'
t_NUM = r'[0-9]+'
t_NORMSTRING    = r'"([^"\n]|(\\"))*"'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDES = r'/'
t_EQUALS  = r'='
t_GT = r'>'
t_LT = r'<'
t_GE = r'>='
t_LE = r'<='
t_NE = r'!='
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_SEMI = r';'
t_AND     = r'&&'
t_OR      = r'\|\|'


# Ignored characters
t_ignore = " \t"

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in keywords:
        t.type =  keywords[t.value]
    return t

def t_COMMENTS(t):
    r'\/\*(.*\n)*.*\*\/'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
with open('test5') as f:
    data = f.read()
print data
lexer.input(data)
while 1:
    tok = lexer.token()
    if not tok:
        break
    print tok
    

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUALS', 'NE'),
    ('left', 'GT', 'GE', 'LT', 'LE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDES')
)


def p_error(p):
    print("Syntax error at '%s', '%s'" % (p.value, p.lineno))

def p_code_block(p):
    '''code_block : LBRACE declaration_list statement_list RBRACE
    '''
    p[0] = CodeBlock(p[2], p[3])
    
def p_declaration_list(p):
    """ declaration_list    : declaration
                            |  declaration_list declaration
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]

def p_declaration(p):
    """ declaration  : INT ID SEMI
    """
    # declaration(ID, TYPE)
    p[0] = Declaration(p[2], p[1])

    
def p_statement_list(p):
    ''' statement_list : statement
                       | statement_list statement 
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]

def p_statement(p):
    ''' statement : assignment_statement 
                  | compound_statement
                  | for_statement
                  | read_statement
                  | write_statement
    '''
    p[0] = p[1]
    
def p_compound_statement(p):
    ''' compound_statement : LBRACE statement_list RBRACE'''
    p[0] = p[2]
    
def p_for_statement(p):
    '''for_statement : FOR LPAREN assignment_expr SEMI expression SEMI assignment_expr RPAREN compound_statement '''
    # forstat(a,b,c,body)
    p[0] = ForStmt(p[3], p[5], p[7], p[9])

def p_write_statement(p):
    ''' write_statement : WRITE ID SEMI '''
    # WriteStat(ID)
    p[0] = WriteStmt(p[2])

def p_read_statement(p):
    ''' read_statement : READ ID SEMI '''
    # WriteStat(ID)
    p[0] = ReadStmt(p[2])
    
def p_assignment_statment(p):
    '''assignment_statement : assignment_expr SEMI'''
    p[0] = AssignmentStmt(p[1])

def p_assignment_expr(p):
    '''assignment_expr : ID EQUALS expression'''
    p[0] = AssignmentExpr(p[1], p[3])
    
def p_expression(p):
    ''' expression : bool_expression '''
    p[0] = p[1]
    
def p_bool_expression(p):
    ''' bool_expression : bool_expression GT bool_expression
                        | bool_expression GE bool_expression
                        | bool_expression LE bool_expression
                        | bool_expression LT bool_expression
                        | LPAREN bool_expression RPAREN
                        | binary_expr'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[1] == '(':
            p[0] = p[2]
        else:
            p[0] = BoolExpr(p[1], p[2], p[3])

def p_binary_expr(p):
    ''' binary_expr : binary_expr PLUS binary_expr
                  | binary_expr MINUS binary_expr
                  | binary_expr TIMES binary_expr
                  | binary_expr DIVIDES binary_expr
                  | LPAREN binary_expr RPAREN
                  | symbol
                  | number '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[1] == '(':
            p[0] = p[2]
        else:
            p[0] = BinaryOp(p[1], p[2], p[3])

    
def p_symbol(p):
    ''' symbol : ID '''
    p[0] = Symbol(p[1])

def p_number(p):
    ''' number : NUM '''
    p[0] = Number(p[1])

import sys
yacc.yacc()
ast =  yacc.parse(data)
if not ast:
    sys.exit(0)
ast.show()
