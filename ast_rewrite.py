# -*- coding: utf-8 -*-
import logging
import sys

from visitor import NodeVisitor
from c_ast import Label, CMPJMP, ABSJMP

logger = logging.getLogger(__file__)
LabelId = 0


def LabelIDGen():
    global LabelId
    LabelId += 1
    return LabelId


class SpecialVisitor(object):
    def visit(self, node, parent):
        """ Visit a node.
        """
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        # deep first
        for c in node.children():
            self.visit(c, node)
        return visitor(node, parent)

    def generic_visit(self, node, parent):
        """ Called if no explicit visitor function exists for a
            node. Implements preorder visiting of the node.
        """
        parent = node
        for c in node.children():
            self.visit(c, parent)


class LoopHelper(SpecialVisitor):
    def __init__(self):
        self.L1ID = LabelIDGen()
        self.L1 = Label(self.L1ID)  # loopstart
        self.L2ID = LabelIDGen()
        self.L2 = Label(self.L2ID)  # loopend
        
    def visit_ContinueStmt(self, node, parent):
        jmpstmt = ABSJMP(self.L1ID)
        index = parent.l.index(node)
        parent.l[index] = jmpstmt

    def visit_BreakStmt(self, node, parent):
        jmpstmt = ABSJMP(self.L2ID)
        index = parent.l.index(node)
        parent.l[index] = jmpstmt

    
class StmtsHelper(SpecialVisitor):
    def __init__(self):
        pass
    
    def visit_WhileStmt(self, node, parent):
        helper = LoopHelper()
        helper.visit(node, parent)
        cmpstmt = CMPJMP(node.bool_expr, helper.L1ID, helper.L2ID)
        index = parent.l.index(node)
        beforestmts = parent.l[:index]
        afterstmts = parent.l[index+1:]
        newstmts = []
        beforestmts.append(cmpstmt)
        newstmts.append(helper.L1)
        newstmts.extend(node.body.l)
        newstmts.append(cmpstmt)
        newstmts.append(helper.L2)
        parent.l = beforestmts + newstmts + afterstmts
        parent = node
        
    ENDSTMTS = ["BreakStmt", "ContinueStmt", "ReturnStmt"]
    def visit_IfStmt(self, node, parent):
        L1ID = LabelIDGen()
        L1 = Label(L1ID)  # iftrue
        L2ID = LabelIDGen()
        L2 = Label(L2ID)  # iffalse
        L3ID = LabelIDGen()
        L3 = Label(L3ID)  # endif
        index = parent.l.index(node)
        beforestmts = parent.l[:index]
        afterstmts = parent.l[index+1:]
        newstmts = []
        cmpstmt = CMPJMP(node.cond, L1ID, L2ID)
        beforestmts.append(cmpstmt)
        newstmts.append(L1)
        newstmts.extend(node.iftrue.l)
        jmp = ABSJMP(L3ID)
        if not filter(lambda x: x.__class__.__name__ in self.ENDSTMTS,
                  node.iftrue.l
        ):
            newstmts.append(jmp)
        newstmts.append(L2)
        if node.iffalse:
            newstmts.extend(node.iffalse.l)
            if not filter(lambda x: x.__class__.__name__ in self.ENDSTMTS,
                          node.iffalse.l
            ):
                newstmts.append(jmp)
        else:
            newstmts.append(jmp)
        newstmts.append(L3)
        parent.l = beforestmts + newstmts + afterstmts
        parent = node
            

class ReWriteVisitor(SpecialVisitor):
    def __init__(self):
        pass

    def visit_StmtList(self, node, parent):
        helper = StmtsHelper()
        helper.visit(node, parent)
