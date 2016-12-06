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
    print("Syntax error at '%s'" % p.value)

def p_code_block(p):
    '''code_block : LBRACE declaration_list statement_list RBRACE
    '''
    p[0] = CodeBlock(p[2], p[3])
    
def p_declaration_list(p):
    """ declaration_list    : declaration
                            | declaration_list declaration
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        DeclarationList(p[1], p[2])

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
        p[0] = StatList(p[1], p[2])

def p_statement(p):
    ''' statement : expression_statement 
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
    '''for_statement : FOR LPAREN expression SEMI expression SEMI expression RPAREN compound_statement '''
    # forstat(a,b,c,body)
    p[0] = ForStat(p[3], p[5], p[7], p[9])

def p_write_statement(p):
    ''' write_statement : WRITE ID SEMI '''
    # WriteStat(ID)
    p[0] = WriteStat(p[2])

def p_read_statement(p):
    ''' read_statement : READ ID SEMI '''
    # WriteStat(ID)
    p[0] = ReadStat(p[2])
    
def p_expression_statement(p):
    ''' expression_statement : expression SEMI'''
    p[0] = p[1]

def p_expression(p):
    ''' expression : bool_expression
                   | assignment_expr'''
    p[0] = p[1]
    
def p_bool_expression(p):
    ''' bool_expression : ID GT bool_expression
                        | ID GE bool_expression
                        | ID LE bool_expression
                        | ID LT bool_expression
                        | NUM GT bool_expression
                        | NUM GE bool_expression
                        | NUM LE bool_expression
                        | NUM LT bool_expression
                        | LPAREN bool_expression RPAREN
                        | ID
                        | NUM'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[1] == '(':
            p[0] = p[2]
        else:
            p[0] = BinaryOp(p[2], p[1], p[3])

def p_assignment_expr(p):
    ''' assignment_expr : ID EQUALS assignment_expr
                  | ID PLUS assignment_expr
                  | ID MINUS assignment_expr
                  | ID TIMES assignment_expr
                  | ID DIVIDES assignment_expr
                  | NUM PLUS assignment_expr
                  | NUM MINUS assignment_expr
                  | NUM TIMES assignment_expr
                  | NUM DIVIDES assignment_expr
                  | LPAREN assignment_expr RPAREN
                  | ID
                  | NUM'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[1] == '(':
            p[0] = p[2]
        else:
            p[0] = BinaryOp(p[2], p[1], p[3])


yacc.yacc()
print yacc.parse(data)
