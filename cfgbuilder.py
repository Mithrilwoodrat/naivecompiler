# -*- coding: utf-8 -*-
import logging
import sys

from visitor import NodeVisitor
from c_ast import Statement, Label, CMPJMP, ABSJMP, TypeDecl

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
            
class BasicBlock(object):
    """ Hold a BasicBlock, To Replace AST Label"""
    BlockKind = ["Reachable", "Unreachable", "Unknown"] # 该 BasicBlock 是否可达
    def __init__(self):
        self.Label = None # Label
        self.Label_id = -1 # Label id
        self.stmts = [] # StmtList
        self.block_kind = "Reachable"
        self.successor = None
        self.Terminator = None
        self.LoopTarget = None
        
    def insert_stmt(self, node):
        if node is not None:
            self.stmts.insert(0, node)
        
#class CFGBuilder(SpecialVisitor):
#    def visit_StmtList(self, node, parent):
#        helper = CFGBuilderIMPL()
#        helper.build_cfg(node, parent)

#int main()
#{
#        int a = 0;
#        if (a > 10)
#                return 1;
#        a = a + 10;
#        return 0;
#}

#int main()
# [B4 (ENTRY)]
#   Succs (1): B3
#
# [B1]
#   1: a
#   2: [B1.1] (ImplicitCastExpr, LValueToRValue, int)
#   3: 10
#   4: [B1.2] + [B1.3]
#   5: a
#   6: [B1.5] = [B1.4]
#   7: 0
#   8: return [B1.7];
#   Preds (1): B3
#   Succs (1): B0
#
# [B2]
#   1: 1
#   2: return [B2.1];
#   Preds (1): B3
#   Succs (1): B0
#
# [B3]
#   1: 0
#   2: int a = 0;
#   3: a
#   4: [B3.3] (ImplicitCastExpr, LValueToRValue, int)
#   5: 10
#   6: [B3.4] > [B3.5]
#   T: if [B3.6]
#   Preds (1): B4
#   Succs (2): B2 B1
#
# [B0 (EXIT)]
#   Preds (2): B1 B2
            
class CFGBuilder(object):
    """ 至低向上构建 CFG，向构建继承的 block 再构建 上一层的 block"""
    Terminator_STMTS = ["BreakStmt", "ContinueStmt", "ReturnStmt"]
    def __init__(self):
        self.blocks = []
        self.current_block = None
        self.current_successor = None
        self.break_jumptarget = [] # if nested control flow stmt, append and pop targets
        self.continue_jumptarget = []
        self.labels = []
        self.entry_block = None
        self.exit_block = None
    
    # CFG.cpp::1124
    # https://code.woboq.org/llvm/clang/lib/Analysis/CFG.cpp.html#_ZN12_GLOBAL__N_110CFGBuilder11createBlockEb
    def build_cfg(self, node, parent):
        """ 将 StmtList 转换为 CFG，从尾向头遍历子节点"""
        assert node.__class__.__name__ == 'StmtList'
        self.current_successor = self.createBlock() # exit Block
        for c in node.children()[::-1]:
            self.visitStmt(c, node)
        print 'Blocks', self.blocks
        for b in self.blocks:
            print b.stmts
    
    def createBlock(self, add_successor=True):
        block = BasicBlock()
        self.blocks.append(block)
        # 将第一个 Block 设置为起始 block
        if len(self.blocks) == 0 or self.blocks[0] == self.blocks[-1]:
            self.entry_block = self.exit_block = block

        # 添加到当前的继承链中
        if add_successor and self.current_successor:
            block.successor = self.current_successor
        return block

    def visit(self, node, parent):
        """ Visit a node.
        """
        parent = node
        if node.__class__.__name__ == "StmtList":
            self.build_cfg(node,parent)
        else:
            for c in node.children():
                self.visit(c, parent)
    
    def visitStmt(self, node, parent, add_to_block=True):
        """ Visit a Stmt.
        """
        node_class =  node.__class__.__name__
        # print node_class
        if issubclass(node.__class__, Statement):
            method = 'visitStmt_' + node_class
            visitor = getattr(self, method)
        else:
            logger.info("Unsupported Stmt: {0}".format(node_class))
            sys.exit(0)
        # deep first 
        # visit in reverse order for gen Label in order
        # for c in node.children()[::-1]:
        #    self.visit(c, Terminatornode)
        if add_to_block:
            if self.current_block is None:
                self.current_block = self.createBlock()
            self.current_block.insert_stmt(node)
        return visitor(node, parent)
    
    # https://code.woboq.org/llvm/clang/lib/Analysis/CFG.cpp.html#_ZN12_GLOBAL__N_110CFGBuilder5VisitEPN5clang4StmtENS_13AddStmtChoiceE
    def visit_StmtList(self, node, parent):
        self.build_cfg(node, parent)
        
    def visitStmt_BreakStmt(self, node, parent):
        self.current_block.Terminator = node
        
    def visitStmt_IfStmt(self, node, parent):
        TrueBlock = self.createBlock()
        
    def visitStmt_ReturnStmt(self, node, parent):
        pass

    def visitStmt_DeclStmt(self, node, parent):
        pass

    def visitStmt_Assignment(self, node, parent):
        pass

    # TODO Build CFG for WhileStmt
    def visitStmt_WhileStmt(self, node, parent):
        pass

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
        self.root = None
        self.const_strings = []
        
    # def visit(self, node, parent):
        # if self.root is None:
            # self.root = parent
        # super(ReWriteVisitor, self).visit(node, parent)


    def visit_StmtList(self, node, parent):
        helper = StmtsHelper()
        bloacks = helper.visit(node, parent)
        index = parent.l.index(node)
        parent[index] = blocks
