# -*- coding: utf-8 -*-
from visitor import NodeVisitor

def minify_ast(ast):
    ''' 
    minify for codegen. 
    remove declarations.
    '''
    assert ast.__class__.__name__ == 'CodeBlock'
    return ast.statement_list
