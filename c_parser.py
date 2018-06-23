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
        "char":"CHAR",
        "float": "FLOAT",
        "return":"RETURN",
        "while": "WHILE",
        "break": "BREAK",
        "continue": "CONTINUE",
        "extern": "EXTERN",
        "static": "STATIC",
        "void": "VOID"}

    # singlewords = ('{', '}', '(', ')' , ';')
    # binop = ('+', '-', '*', '/', '=', '>', '<')
    # doubleword = ('>=', '<=', '!=')
    # comment = ('/*', '*/'
    #)
    tokens = (
        "ID", "INT_CONST", "FLOAT_CONST", "CHAR_CONST", "NORMALSTRING",
        "IF", "ELSE", 'WHILE', 'RETURN', 'BREAK', 'CONTINUE',
        "PLUS", "MINUS", "TIMES", "DIVIDES", "EQUALS", "GT", "LT", "LAND", "LOR",
        "BAND",
        'INT','CHAR', 'FLOAT',
        "GE", 'LE', 'NE',
        "LBRACE", "RBRACE", "LBRACKET", "RBRACKET", "LPAREN","RPAREN","SEMI","COMMA","VOID",
        "COMMENTS",
        "EXTERN", "STATIC"
    )
    
    identifier       = r'[a-zA-Z_][0-9a-zA-Z_]*'
    t_IF = r'if'
    t_ELSE = r'else'
    t_WHILE = r'while'
    t_BREAK = r'break'
    t_CONTINUE = r'continue'
    t_INT = r'int'
    t_CHAR = r'char'
    t_FLOAT = r'float'
    t_INT_CONST = r'[0-9]+'
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_BAND = r'&'
    t_DIVIDES = r'/'
    t_EQUALS  = r'='
    t_GT = r'>'
    t_LT = r'<'
    t_GE = r'>='
    t_LE = r'<='
    t_NE = r'!='
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_SEMI = r';'
    t_COMMA = r','
    t_EXTERN = r'extern'
    t_STATIC = r'static'
    t_VOID = r'void'
    t_LAND     = r'&&'
    t_LOR      = r'\|\|'
    

    
    # Ignored characters
    t_ignore = " \t"
    

    @TOKEN(identifier)
    def t_ID(self, t):
        if t.value in self.keywords:
            t.type =  self.keywords[t.value]
        return t

    exponent_part = r"""([eE][-+]?[0-9]+)"""
    fractional_constant = r"""([0-9]*\.[0-9]+)|([0-9]+\.)"""
    floating_constant = '(((('+fractional_constant+')'+exponent_part+'?)|([0-9]+'+exponent_part+'))[FfLl]?)'
    
    @TOKEN(floating_constant)
    def t_FLOAT_CONST(self, t):
        return t

    # character constants (K&R2: A.2.5.2)
    # Note: a-zA-Z and '.-~^_!=&;,' are allowed as escape chars to support #line
    # directives with Windows paths as filenames (..\..\dir\file)
    # For the same reason, decimal_escape allows all digit sequences. We want to
    # parse all correct code, even if it means to sometimes parse incorrect
    # code.
    #
    simple_escape = r"""([a-zA-Z._~!=&\^\-\\?'"])"""
    decimal_escape = r"""(\d+)"""
    hex_escape = r"""(x[0-9a-fA-F]+)"""
    bad_escape = r"""([\\][^a-zA-Z._~^!=&\^\-\\?'"x0-7])"""

    escape_sequence = r"""(\\("""+simple_escape+'|'+decimal_escape+'|'+hex_escape+'))'
    cconst_char = r"""([^'\\\n]|"""+escape_sequence+')'
    char_const = "'"+cconst_char+"'"
    wchar_const = 'L'+char_const
    unmatched_quote = "('"+cconst_char+"*\\n)|('"+cconst_char+"*$)"
    bad_char_const = r"""('"""+cconst_char+"""[^'\n]+')|('')|('"""+bad_escape+r"""[^'\n]*')"""

    # string literals (K&R2: A.2.6)
    string_char = r"""([^"\\\n]|"""+escape_sequence+')'
    string_literal = '"'+string_char+'*"'
    wstring_literal = 'L'+string_literal
    bad_string_literal = '"'+string_char+'*?'+bad_escape+string_char+'*"'

    @TOKEN(char_const)
    def t_CHAR_CONST(self, t):
        return t

    @TOKEN(string_literal)
    def t_NORMALSTRING(self, t):
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
        ('left', 'LOR'),
        ('left', 'LAND'),
        ('left', 'EQUALS', 'NE'),
        ('left', 'GT', 'GE', 'LT', 'LE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDES')
    )


    def p_error(self, p):
        print("Syntax error at '%s', '%s'" % (p.value, p.lineno))

    #def p_root(self, p):
    #    ''' root : funcdeflist '''
    #    p[0] = p[1]

    def p_translation_unit(self, p):
        ''' translation_unit : external_decl
                             | translation_unit external_decl
        '''
        if len(p) == 2:
            p[0] = AST(p[1])
        elif len(p) == 3:
            p[1].l.append(p[2])
            p[0] = p[1]
        else:
            logging.error("empty ast")

    def p_external_decl(self, p):
        ''' external_decl : funcdef
                          | declstmt
        '''
        p[0] = p[1]
            
    # def p_funcdeflist(self, p):
    #     ''' funcdeflist : funcdef
    #                | funcdeflist funcdef
    #     '''
    #     if len(p) == 2:
    #         p[0] = FuncList(p[1])
    #     else:
    #         p[0] = p[1] + p[2]
                    
    # def p_declaration_list(self, p):
    #     """ declaration_list : declaration
    #                          | declaration COMMA declaration_list
    #     """
    #     if len(p) == 2:
    #         p[0] = DeclarationList(p[1])
    #     else:
    #         p[0] = p[1] + p[3]
    
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
        '''typedecl : type cast_expr 
                    | type cast_expr EQUALS expression'''
        if len(p) == 5:
            p[0] = TypeDecl(p[1], p[2], p[4])
        elif len(p) == 3:
            p[0] = TypeDecl(p[1], p[2])

    def p_arraydecl(self, p):
        '''arraydecl : type varsymbol LBRACKET INT_CONST RBRACKET EQUALS expression'''
        p[0] = ArrayDecl(p[1], p[2], p[4], p[7])

    def p_arraydecl_2(self, p):
        '''arraydecl : type varsymbol LBRACKET INT_CONST RBRACKET'''
        p[0] = ArrayDecl(p[1], p[2], p[4])
        
    def p_funcdecl(self, p):
        ''' funcdecl : storage type methodsymbol LPAREN param_list RPAREN'''
        p[0] = FuncDecl(p[2], p[3], p[5], p[1])

    def p_funcdecl_2(self, p):
        ''' funcdecl : type methodsymbol LPAREN param_list RPAREN'''
        p[0] = FuncDecl(p[1], p[2], p[4])

    # def p_funcdef_2(self, p):
    #     ''' funcdecl : storage VOID methodsymbol LPAREN param_list RPAREN SEMI'''
    #     print '======'
    #     pass

    def p_pointer(self, p):
        ''' pointer : TIMES 
                    | pointer TIMES'''
        p[0] = p[1] if len(p) == 2 else p[1] + p[2]

    def p_storage(self, p):
        ''' storage : EXTERN
                    | STATIC'''
        p[0] = p[1]
    def p_type(self, p):
        ''' type : basetype pointer
                 | basetype
        '''
        p[0] = p[1] if len(p) == 2 else p[1] + p[2]
        
    def p_declaration(self, p):
        ''' declaration : typedecl 
                        | arraydecl
                        | funcdecl'''
        p[0] = p[1]
    
    def p_declstmt(self, p):
        """ declstmt : declaration SEMI
        """
        #decls = DeclarationList(p[1])
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
        
    def p_return_statement2(self, p):
        ''' return_statement : RETURN SEMI '''
        p[0] = ReturnStmt()
    
    def p_assignment_statment(self, p):
        '''assignment_statement : assignment_expr SEMI'''
        p[0] = p[1]

    def p_assignment_expr(self, p):
        '''assignment_expr : cast_expr EQUALS expression'''
        p[0] = Assignment(p[1], p[3])
    
    def p_expression(self, p):
        ''' expression : binary_expr
                       | funccall_expr
        '''
        p[0] = p[1]

    def p_cast_expr(self, p):
        ''' cast_expr : unary_expr
                      | primary_expr
        '''
        p[0] = p[1]

    def p_primary_expr(self, p):
        ''' primary_expr : varsymbol
                         | constant
        '''
        # | string_literal
        p[0] = p[1]

    # 一元操作符
    def p_unary_op(self, p):
        """ unary_op : BAND
                     | TIMES
        """
        p[0] = p[1]

    def p_unary_expr(self, p):
        """ unary_expr : unary_op primary_expr """
        p[0] = UnaryOp(p[1], p[2])

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
                  | binary_expr LAND binary_expr
                  | binary_expr LOR binary_expr
                  | LPAREN binary_expr RPAREN
                  | cast_expr
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            if p[1] == '(':
                p[0] = p[2]
            else:
                p[0] = BinaryOp(p[1], p[2], p[3])
                
    def p_param(self, p):
       ''' param : type varsymbol '''
       p[0] = TypeDecl(p[1], p[2])

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
            p[0] = FuncDef(p[1], p[2], p[4], p[6])
        elif len(p) == 6:
            param_list = DeclarationList()
            p[0] = FuncDef(p[1], p[2], param_list, p[5])
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
            
    def p_basetype(self, p):
        ''' basetype : INT 
                 | CHAR
                 | FLOAT
                 | VOID '''
        p[0] = p[1]
        
    def p_methodsymbol(self, p):
        ''' methodsymbol : ID '''
        p[0] = MethodSymbol(p[1])
        
    def p_varsymbol(self, p):
        ''' varsymbol : ID '''
        p[0] = VariableSymbol(p[1])

    def p_constant1(self, p):
        ''' constant : INT_CONST '''
        p[0] = Const('int', p[1])

    def p_constant2(self, p):
        ''' constant : CHAR_CONST '''
        p[0] = Const('char', p[1])

    def p_constant3(self, p):
        ''' constant : FLOAT_CONST '''
        p[0] = Const('float', p[1])

    def p_constant4(self, p):
        ''' constant : NORMALSTRING '''
        p[0] = Const('string', p[1])


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
    
