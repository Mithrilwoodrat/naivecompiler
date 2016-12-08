# -*- coding: utf-8 -*-

class ASTNode(object):
    def __init__(self):
        self.node_name = "ASTNode"

    def show(self):
        print self.node_name

class AST(object):
    def __init__(self):
        pass

class CodeBlock(ASTNode):
    def __init__(self, declaration_list, statement_list):
        self.node_name = "CodeBlock"
        super(CodeBlock, self).__init__()
        self.declaration_list = declaration_list
        self.statement_list = statement_list

    def show(self):
        print 'CodeBlock'
        self.declaration_list.show()
        self.statement_list.show()

class DeclarationList(ASTNode):
    def __init__(self):
        self.node_name = "DeclarationList"
        self.l = []
        
    def add_declaration(self, d):
        self.l.append(d)

    def __add__(self, rhs):
        if type(rhs) is Declaration:
            self.add_declaration(rhs)
        elif type(rhs) is DeclarationList:
            self.l += rhs.l
        return self

    def show(self):
        print self.node_name
        for n in self.l:
            n.show()

class StatList(ASTNode):
    def __init__(self):
        self.node_name = "StatList"
        self.l = []

    def add_stat(self, s):
        self.l.append(s)

    def __add__(self, rhs):
        if issubclass(rhs.__class__, Statement):
            self.add_stat(rhs)
        elif type(rhs) is StatList:
            self.l += rhs.l
        return self

    def show(self):
        print self.node_name
        for n in self.l:
            n.show()

class Declaration(ASTNode):
    '''Declaration: Type Assignment SEIM'''
    def __init__(self, ID, Type):
        self._id = ID
        self._type = Type

    def show(self):
        print 'Declaration Node:', self._id, self._type

    def __add__(self, rhs):
        declaration_list = DeclarationList()
        if type(rhs) is DeclarationList:
            rhs.add_declaration(self)
            return rhs
        else:
            declaration_list.add_declaration(self)
            declaration_list.add_declaration(rhs)
            return declaration_list

class Statement(ASTNode):
    def __add__(self, rhs):
        stat_list = StatList()
        if type(rhs) is StatList:
            rhs.add_stat(self)
            return rhs
        else:
            stat_list.add_stat(self)
            stat_list.add_stat(rhs)
        return stat_list

class IfStat(object):
    pass

class ForStat(Statement):
    def __init__(self, expr1, expr2, expr3, body):
        self.expr1 = expr1
        self.expr2 = expr2
        self.expr3 = expr3
        self.body = body
        self.node_name = "ForStat"

    def show(self):
        print self.node_name
        self.expr1.show()
        self.expr2.show()
        self.expr3.show()
        self.body.show()

class ReadStat(Statement):
    def __init__(self, ID):
        self._id = ID
        self.node_name = "ReadStat"

class WriteStat(Statement):
    def __init__(self, ID):
        self._id = ID
        self.node_name = "WriteStat"

class BinaryOp(ASTNode):
    def __init__(self, lhs, op , rhs):
        self.node_name = "BinaryOp"
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def show(self):
        print "BinaryOp"
        self.lhs.show()
        print self.op
        self.rhs.show()

class Var(ASTNode):
    def __init__(self, name):
        self.node_name = "Var"
        self.name = name

class Number(ASTNode):
    def __init__(self, val):
        self.node_name = "Number"
        self.val = val
    
class ExprStat(object):
    pass

class Expr(object):
    pass

class BoolExpr(object):
    pass

class AssigmentExpr(object):
    pass
