# -*- coding: utf-8 -*-
from ply import lex, yacc
from ply.lex import TOKEN
from c_ast import *
import logging


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
        "int":"INT",
        "return":"RETURN",
        "while": "WHILE",
        "break": "BREAK",
        "continue": "CONTINUE",
        "void": "VOID"}

    # singlewords = ('{', '}', '(', ')' , ';')
    # binop = ('+', '-', '*', '/', '=', '>', '<')
    # doubleword = ('>=', '<=', '!=')
    # comment = ('/*', '*/'
    #)
    tokens = (
        "ID", "INT_CONST", "NORMSTRING",
        "IF", "ELSE", 'WHILE', 'RETURN', 'BREAK', 'CONTINUE',
        "PLUS", "MINUS", "TIMES", "DIVIDES", "EQUALS", "GT", "LT", "AND", "OR",
        'INT',
        "GE", 'LE', 'NE',
        "LBRACE", "RBRACE", "LPAREN","RPAREN","SEMI","COMMA","VOID",
        "COMMENTS"
    )
    
    identifier       = r'[a-zA-Z_][0-9a-zA-Z_]*'
    t_IF = r'if'
    t_ELSE = r'else'
    t_WHILE = r'while'
    t_BREAK = r'break'
    t_CONTINUE = r'continue'
    t_INT = r'int'
    #t_READ = r'read'
    #t_WRITE = r'write'
    t_INT_CONST = r'[0-9]+'
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

    def p_root(self, p):
        ''' root : funcdeflist '''
        p[0] = AST(p[1])
            
    def p_funcdeflist(self, p):
        ''' funcdeflist : funcdef
                   | funcdeflist funcdef
        '''
        if len(p) == 2:
            p[0] = FuncList(p[1])
        else:
            p[0] = p[1] + p[2]
        
    # def p_code_block(self, p):
    #     '''code_block : LBRACE declaration_list statement_list RBRACE
    #                   | LBRACE statement_list RBRACE
    #     '''
    #     if len(p) == 4:
    #         decls = DeclarationList()
    #         p[0] = CodeBlock(decls, p[2])
    #     else:
    #         p[0] = CodeBlock(p[2], p[3])

    def p_identifier_list(self, p):
        """ identifier_list : ID
                             | ID COMMA identifier_list
        
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + p[3]
            
    def p_declaration_list(self, p):
        """ declaration_list : declaration
                             | declaration COMMA declaration_list
        """
        if len(p) == 2:
            p[0] = DeclarationList(p[1])
        else:
            p[0] = p[1] + p[3]
    
    def p_statement_list(self, p):
        ''' statement_list : statement
                       | statement statement_list 
        '''
        if len(p) == 2:
            p[0] = StmtList(p[1])
        else:
            p[0] = p[1] + p[2]

    def p_statement(self, p):
        ''' statement : assignment_statement 
                  | declstmt
                  | while_statement
                  | funccall_stmt
                  | jump_statement
                  | selection_statement
        '''
        p[0] = p[1]
        
    def p_typedecl(self, p):
        '''typedecl : type varsymbol'''
        p[0] = TypeDeclaration(p[1], p[2])

    def p_arraydecl(self, p):
        '''arraydecl : '''

    def p_declaration(self, p):
        ''' declaration : typedecl '''
        p[0] = p[1]
    
    def p_declstmt(self, p):
        """ declstmt : declaration_list SEMI
        """
        p[0] = DeclStmt(p[1])

    def p_compound_statement(self, p):
        ''' compound_statement : LBRACE statement_list RBRACE'''
        p[0] = p[2]
    
    def p_while_statement(self, p):
        '''while_statement : WHILE LPAREN expression RPAREN compound_statement'''
        p[0] = WhileStmt(p[3], p[5])

    def p_if_statement1(self, p):
        '''if_statement1 : IF LPAREN expression RPAREN compound_statement ELSE compound_statement'''
        p[0] = IfStmt(p[3], p[5], p[7])

    def p_if_statement2(self, p):
        '''if_statement2 : IF LPAREN expression RPAREN compound_statement'''
        p[0] = IfStmt(p[3], p[5])
        
    def p_selection_statement(self, p):
        ''' selection_statement : if_statement1
                                | if_statement2
        '''
        p[0] = p[1]

    def p_break_statement(self, p):
        """ break_statement  : BREAK SEMI """
        p[0] = BreakStmt()

    def p_continue_statement(self, p):
        """ continue_statement  : CONTINUE SEMI """
        p[0] = ContinueStmt()

    def p_jump_statement(self, p):
        """ jump_statement  : return_statement
                            | continue_statement
                            | break_statement"""
        p[0] = p[1]

    def p_return_statement(self, p):
        ''' return_statement : RETURN expression SEMI '''
        p[0] = ReturnStmt(p[2])
    
    def p_assignment_statment(self, p):
        '''assignment_statement : assignment_expr SEMI'''
        p[0] = AssignmentStmt(p[1])

    def p_assignment_expr(self, p):
        '''assignment_expr : ID EQUALS expression'''
        var = VariableSymbol(p[1])
        p[0] = AssignmentExpr(var, p[3])
    
    def p_expression(self, p):
        ''' expression : binary_expr
        '''
        p[0] = p[1]

    def p_binary_expr(self, p):
        ''' binary_expr : binary_expr PLUS binary_expr
                  | binary_expr MINUS binary_expr
                  | binary_expr TIMES binary_expr
                  | binary_expr DIVIDES binary_expr
                  | binary_expr GT binary_expr
                  | binary_expr LT binary_expr
                  | binary_expr LE binary_expr
                  | binary_expr GE binary_expr
                  | binary_expr NE binary_expr
                  | binary_expr AND binary_expr
                  | binary_expr OR binary_expr
                  | LPAREN binary_expr RPAREN
                  | funccall_expr
                  | varsymbol
                  | constant '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            if p[1] == '(':
                p[0] = p[2]
            else:
                p[0] = BinaryOp(p[1], p[2], p[3])
                
    def p_param(self, p):
       ''' param : type varsymbol '''
       p[0] = TypeDeclaration(p[1], p[2])

    def p_param_list(self, p):
        ''' param_list : param
                       | param COMMA param_list
                       | VOID
        '''
        if len(p) == 2:
            if p[1] == 'void':
                p[0] = DeclarationList()
            else:
                p[0] = DeclarationList(p[1])
        else:
            p[0] = p[1] + p[3]

    def p_argument(self, p):
        ''' argument : varsymbol
                     | constant
        '''
        p[0] = p[1]

    def p_argument_list(self, p):
        ''' argument_list : argument 
                          | argument COMMA argument_list
        '''
        if len(p) == 2:
            p[0] = ArgumentList(p[1])
        elif len(p) == 4:
            p[3].l.insert(0, p[1])
            p[0] = p[3]
        else:
            logging.error("wrong argument_list")
        
    def p_funcdef(self, p):
        ''' funcdef : type methodsymbol LPAREN param_list RPAREN compound_statement
                    | type methodsymbol LPAREN RPAREN compound_statement
        '''
        if len(p) == 7:
            p[0] = Function(p[1], p[2], p[4], p[6])
        elif len(p) == 6:
            param_list = DeclarationList()
            p[0] = Function(p[1], p[2], param_list, p[5])
        else:
            logging.error("wrong funcdef")
            print len(p)
            print [i for i in p]

    def p_funcall_expr(self, p):
        ''' funccall_expr : methodsymbol LPAREN argument_list RPAREN
                     | methodsymbol LPAREN RPAREN
        '''
        if len(p) == 5:
            p[0] = FuncCall(p[1], p[3])
        elif len(p) == 4:
            argument_list = ArgumentList()
            p[0] = FuncCall(p[1], argument_list)
        else:
            logging.error("wrong FuncCall")
            print len(p)
            print [i for i in p]
        
    def p_funccall_stmt(self, p):
        ''' funccall_stmt : funccall_expr SEMI
        '''
        p[0] = p[1]
            
    def p_type(self, p):
        ''' type : INT '''
        p[0] = p[1]
        
    def p_methodsymbol(self, p):
        ''' methodsymbol : ID '''
        p[0] = MethodSymbol(p[1])
        
    def p_varsymbol(self, p):
        ''' varsymbol : ID '''
        p[0] = VariableSymbol(p[1])

    def p_constant(self, p):
        ''' constant : INT_CONST '''
        p[0] = Const(p[1])

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
    
