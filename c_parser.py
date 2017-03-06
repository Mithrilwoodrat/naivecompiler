# -*- coding: utf-8 -*-
from ply import lex, yacc
from ply.lex import TOKEN
from c_ast import *


class Lexer(object):
    def __init__(self, **kwargs):
        self.lexer = lex.lex(object=self, **kwargs)

    def input(self, text):
        self.lexer.input(text)
    
    def reset_lineno(self):
        self.lexer.lineno = 1
        
    def token(self):
        self.last_token = self.lexer.token()
        return self.last_token
    
    def find_tok_column(self, token):
        """ Find the column of the token in its line.
        """
        last_cr = self.lexer.lexdata.rfind('\n', 0, token.lexpos)
        return token.lexpos - last_cr

    # Test it output
    def test(self, data):
        self.input(data)

        while True:
            tok = self.token()
            if tok:
                print(tok)
            else:
                break

    ## PRIVATE ##
    keywords = {
        "if":'IF',
        "else":"ELSE",
        "for":"FOR",
        "int":"INT",
        "read":"READ",
        "write":"WRITE",
        "void": "VOID"}

    # singlewords = ('{', '}', '(', ')' , ';')
    # binop = ('+', '-', '*', '/', '=', '>', '<')
    # doubleword = ('>=', '<=', '!=')
    # comment = ('/*', '*/'
    #)
    tokens = (
        "ID", "NUM", "NORMSTRING",
        "IF", "ELSE", 'FOR','INT', 'READ', 'WRITE',
        "PLUS", "MINUS", "TIMES", "DIVIDES", "EQUALS", "GT", "LT", "AND", "OR",
        "GE", 'LE', 'NE',
        "LBRACE", "RBRACE", "LPAREN","RPAREN","SEMI","COMMA","VOID",
        "COMMENTS"
    )
    
    identifier       = r'[a-zA-Z_][0-9a-zA-Z_]*'
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
    t_COMMA = r','
    t_VOID = r'void'
    t_AND     = r'&&'
    t_OR      = r'\|\|'
    

    
    # Ignored characters
    t_ignore = " \t"
    

    @TOKEN(identifier)
    def t_ID(self, t):
        if t.value in self.keywords:
            t.type =  self.keywords[t.value]
        return t

    def t_COMMENTS(self, t):
        r'\/\*(.*\n)*.*\*\/'
        pass

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

# lexer = lex.lex()
# with open('test5') as f:
#     data = f.read()
# print data
# lexer.input(data)
# while 1:
#     tok = lexer.token()
#     if not tok:
#         break
#     print tok
    
class Parser(object):
    def __init__(self):
        self.lex = Lexer()
        self.tokens = self.lex.tokens
        self.parser = yacc.yacc(module=self)

    def parse(self, text):
        return self.parser.parse(input=text, lexer=self.lex)
        
        
    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'EQUALS', 'NE'),
        ('left', 'GT', 'GE', 'LT', 'LE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDES')
    )


    def p_error(self, p):
        print("Syntax error at '%s', '%s'" % (p.value, p.lineno))

    def p_funcdeflist(self, p):
        ''' funcdeflist : funcdef
                   | funcdeflist funcdef
        '''
        if len(p) == 2:
            p[0] = FuncDefList(p[1])
        else:
            p[0] = p[1] + p[2]
        
    def p_code_block(self, p):
        '''code_block : LBRACE declaration_list statement_list RBRACE
        '''
        p[0] = CodeBlock(p[2], p[3])
    
    def p_declaration_list(self, p):
        """ declaration_list    : declaration
                        |  declaration_list declaration
        """
        if len(p) == 2:
            p[0] = DeclarationList(p[1])
        else:
            p[0] = p[1] + p[2]

    def p_declaration(self, p):
        """ declaration  : type varsymbol SEMI
        """
        # declaration(ID, TYPE)
        #var = VariableSymbol(p[2])
        #p[0] = Declaration(var, p[1])
        p[0] = Declaration(p[2], p[1])
    
    def p_statement_list(self, p):
        ''' statement_list : statement
                       | statement_list statement 
        '''
        if len(p) == 2:
            p[0] = StmtList(p[1])
        else:
            p[0] = p[1] + p[2]

    def p_statement(self, p):
        ''' statement : assignment_statement 
                  | compound_statement
                  | for_statement
                  | read_statement
                  | write_statement
        '''
        p[0] = p[1]
    
    def p_compound_statement(self, p):
        ''' compound_statement : LBRACE statement_list RBRACE'''
        p[0] = p[2]
    
    def p_for_statement(self, p):
        '''for_statement : FOR LPAREN assignment_expr SEMI expression SEMI assignment_expr RPAREN compound_statement '''
        # forstat(a,b,c,body)
        p[0] = ForStmt(p[3], p[5], p[7], p[9])

    def p_write_statement(self, p):
        ''' write_statement : WRITE varsymbol SEMI '''
        # WriteStat(ID)
        #var = VariableSymbol(p[2])
        p[0] = WriteStmt(p[2])

    def p_read_statement(self, p):
        ''' read_statement : READ varsymbol SEMI '''
        # WriteStat(ID)
        #var = VariableSymbol(p[2])
        p[0] = ReadStmt(p[2])
    
    def p_assignment_statment(self, p):
        '''assignment_statement : assignment_expr SEMI'''
        p[0] = AssignmentStmt(p[1])

    def p_assignment_expr(self, p):
        '''assignment_expr : ID EQUALS expression'''
        var = VariableSymbol(p[1])
        p[0] = AssignmentExpr(var, p[3])
    
    def p_expression(self, p):
        ''' expression : bool_expression '''
        p[0] = p[1]
    
    def p_bool_expression(self, p):
        ''' bool_expression : bool_expression GT bool_expression
                        | bool_expression GE bool_expression
                        | bool_expression LE bool_expression
                        | bool_expression LT bool_expression
                        | bool_expression AND bool_expression
                        | bool_expression OR bool_expression
                        | LPAREN bool_expression RPAREN
                        | binary_expr'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            if p[1] == '(':
                p[0] = p[2]
            else:
                p[0] = BoolExpr(p[1], p[2], p[3])

    def p_binary_expr(self, p):
        ''' binary_expr : binary_expr PLUS binary_expr
                  | binary_expr MINUS binary_expr
                  | binary_expr TIMES binary_expr
                  | binary_expr DIVIDES binary_expr
                  | LPAREN binary_expr RPAREN
                  | varsymbol
                  | number '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            if p[1] == '(':
                p[0] = p[2]
            else:
                p[0] = BinaryOp(p[1], p[2], p[3])
                
    def p_param(self, p):
        ''' param : type varsymbol '''
        p[0] = Param(p[1], p[2])

    def p_param_list(self, p):
        ''' param_list : param
                       | param COMMA param_list
                       | VOID
        '''
        if len(p) == 2:
            if p[1] == 'void':
                p[0] = ParamList()
            else:
                p[0] = ParamList(p[1])
        else:
            p[0] = p[1] + p[3]
        
    def p_funcdef(self, p):
        ''' funcdef : type methodsymbol LPAREN  param_list RPAREN code_block'''
        p[0] = FunctionDef(p[1], p[2], p[4], p[6])
    
    def p_type(self, p):
        ''' type : INT '''
        p[0] = p[1]
        
    def p_methodsymbol(self, p):
        ''' methodsymbol : ID '''
        p[0] = MethodSymbol(p[1])
        
    def p_varsymbol(self, p):
        ''' varsymbol : ID '''
        p[0] = VariableSymbol(p[1])

    def p_number(self, p):
        ''' number : NUM '''
        p[0] = Number(p[1])

# import sys
# yacc.yacc()
# ast =  yacc.parse(data)
# if not ast:
#     sys.exit(0)
# ast.show()

if __name__ == "__main__":
    with open('test5') as f:
        data = f.read()
    print data
    lexer = Lexer()
    lexer.test(data)
    parser = Parser()
    ast = parser.parse(data)
    ast.show()
    
