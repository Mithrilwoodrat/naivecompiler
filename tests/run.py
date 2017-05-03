# -*- coding: utf-8 -*-
from pycparser import c_parser
import sys


parser = c_parser.CParser()
with open(sys.argv[1]) as f:
    text = f.read()
ast = parser.parse(text)
ast.show()
