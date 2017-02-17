# -*- coding: utf-8 -*-

class ASTNode(object):
    def __init__(self):
        self.node_name = "ASTNode"

    def show(self):
        print self.node_name
        
class StringTable(object):
    def __init__(self):
        self.table = []
        self.index = 0
        
    def add(self, string):
        self.table.append(string)
        old_index = self.index
        self.index+=1
        return old_index

class SymbolTable(object):
    pass

class AST(object):
    def __init__(self):
        symbol_table = []

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

    def serialize(self):
        pass

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

class StmtList(ASTNode):
    def __init__(self):
        self.node_name = "StmtList"
        self.l = []

    def add_stat(self, s):
        self.l.append(s)

    def __add__(self, rhs):
        if issubclass(rhs.__class__, Statement):
            self.add_stat(rhs)
        elif type(rhs) is StmtList:
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
        stat_list = StmtList()
        if type(rhs) is StmtList:
            rhs.add_stat(self)
            return rhs
        else:
            stat_list.add_stat(self)
            stat_list.add_stat(rhs)
        return stat_list

class IfStmt(object):
    pass

class ForStmt(Statement):
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

class ReadStmt(Statement):
    def __init__(self, ID):
        self._id = ID
        self.node_name = "ReadStat"

class WriteStmt(Statement):
    def __init__(self, ID):
        self._id = ID
        self.node_name = "WriteStat"

class AssignmentStmt(Statement):
    def __init__(self, AssignmentExpr):
        self.node_name = "AssigmentStmt"
        self.expr = AssignmentExpr

    def show(self):
        print "AssigmentStmt"
        self.expr.show()

class AssignmentExpr(ASTNode):
    def __init__(self, _id, rhs):
        self.node_name = "AssignmentExpr"
        self._id = _id
        self.rhs = rhs

    def show(self):
        print "AssignmentExpr", self._id
        self.rhs.show()

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
        
class BoolExpr(object):
    def __init__(self, lhs, op , rhs):
        self.node_name = "BoolExpr"
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def show(self):
        print "BoolExpr"
        self.lhs.show()
        print self.op
        self.rhs.show()


class Symbol(ASTNode):
    def __init__(self, name):
        self.node_name = "Symbol"
        self.name = name
        
    def show(self):
        print self.node_name, self.name

class Number(ASTNode):
    def __init__(self, val):
        self.node_name = "Number"
        self.val = val

    def show(self):
        print self.node_name, self.val
