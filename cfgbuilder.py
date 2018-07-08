# -*- coding: utf-8 -*-
import logging
import sys

from visitor import NodeVisitor
from c_ast import *

logger = logging.getLogger(__file__)
LabelId = 0


def LabelIDGen():
    global LabelId
    LabelId += 1
    return LabelId

def get_id():
    _id = 0
    while(1):
        yield _id
        _id += 1

id_generator = get_id()

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

def build_cfg(ast):
    def visit(node, parent):
        """ Visit a node.
        """
        # deep first
        for c in node.children():
            if node.__class__ is FuncDef:
                cfg = CFG.build_cfg(node.body, node)
                return cfg
            else:
                visit(c, node)
        return None
    return visit(ast, ast)

class CFGBlock(object):
    """ Hold a BasicBlock, To Replace AST Label"""
    BlockKind = ["Reachable", "Unreachable", "Unknown"] # 该 BasicBlock 是否可达
    def __init__(self):
        self.Label = None # Label
        self.Label_id = -1 # Label id
        self.block_id = id_generator.next() # block id
        self.block_name = ''
        self.stmts = [] # StmtList
        self.block_kind = "Reachable"
        self.preds = []
        self.successors = []
        self.Terminator = None
        self.LoopTarget = None
        
    def insert_stmt(self, node):
        if node is not None:
            self.stmts.insert(0, node)

    def set_loop_target(self, node):
        self.LoopTarget = node

    def set_terminator(self, node):
        self.Terminator = node

    def add_successor(self, block):
        self.successors.append(block)

class CFG(object):
    def __init__(self):
        self.blocks = []
        self.entry_block = None
        self.exit_block = None

    def insert_block(self, block):
        if block:
            self.blocks.insert(0, block)

    def create_block(self):
        block = CFGBlock()
        self.insert_block(block)
        # 将第一个 Block 设置为起始 block
        if len(self.blocks) == 0 or self.blocks[0] == self.blocks[-1]:
            self.entry_block = self.exit_block = block
            block.block_name = 'Exit'
        return block

    def set_entry(self, block):
        self.entry_block = block
        self.entry_block.block_name = 'Entry'

    @staticmethod
    def build_cfg(stmtlist, funcdef):
        cfgbuilder = CFGBuilder()
        return cfgbuilder.build_cfg(stmtlist, funcdef)
    
            
class CFGBuilder(object):
    """ 至低向上构建 CFG，向构建继承的 block 再构建 上一层的 block"""
    Terminator_STMTS = ["BreakStmt", "ContinueStmt", "ReturnStmt"]
    def __init__(self):
        self.cfg = CFG()
        self.current_block = None
        self.current_successor = None
        self.break_jumptarget = None
        self.continue_jumptarget = None
        # if nested control flow stmt, append and pop targets
        self.block_stack = self.successor_stack = []
        self.break_jumptarget_stack = []
        self.continue_jumptarget_stack = []
        self.labels = []
    
    def create_block(self, add_successor=True):
        block = self.cfg.create_block()
        # 添加到当前的继承链中
        # print self.current_block, add_successor
        if add_successor and self.current_successor:
            block.add_successor(self.current_successor)
        return block

    def auto_create_block(self):
        if self.current_block is None:
            self.current_block = self.create_block()
    
    def visit(self, node):
        """ Visit a Stmt.
        """
        node_class =  node.__class__.__name__
        # print node_class
        if issubclass(node.__class__, Statement) or node.__class__ is StmtList:
            method = 'visit_' + node_class
            visitor = getattr(self, method)
        else:
            logger.warning("Unsupported Stmt: {0}".format(node_class))
            sys.exit(1)
        return visitor(node)

    # add stmt to block , return current_block if stmt has no children
    def visitStmt(self, stmt, add_to_block=True):
        if add_to_block:
            self.auto_create_block()
            self.current_block.insert_stmt(stmt)
        return self.visitStmt_children(stmt)

    def visitStmt_children(self, stmt):
        block = self.current_block
        # visit in resverse order
        for c in stmt.children()[::-1]:
            if issubclass(c.__class__, Statement):
                tmp = self.visit(c)
                if tmp:
                    block = tmp
        return block

    # CFG.cpp::1124
    # https://code.woboq.org/llvm/clang/lib/Analysis/CFG.cpp.html#_ZN12_GLOBAL__N_110CFGBuilder11createBlockEb
    def build_cfg(self, node, parent):
        """ 将 StmtList 转换为 CFG，从尾向头遍历子节点"""
        assert node.__class__.__name__ == 'StmtList'
        self.current_successor = self.create_block() # exit Block
        self.current_block = None
        
        block = self.visit(node)
        
        if block is not None:
            self.current_successor = block

        print self.current_successor
        self.cfg.set_entry(self.create_block())
        blocks = self.cfg.blocks
        print 'Blocks', blocks
        for b in blocks:
            print b.block_id,b.block_name
            print b.stmts
            print 'Succs:', [i.block_id for i in b.successors]
    
    # https://code.woboq.org/llvm/clang/lib/Analysis/CFG.cpp.html VisitCompoundStmt
    def visit_StmtList(self, node):
        last_block = self.current_block
        for c in node.children()[::-1]:
            tmp = self.visit(c)
            if tmp:
                last_block = tmp
        return last_block
        
    def visitStmt_BreakStmt(self, node, parent):
        self.current_block.Terminator = node
        
    def visitStmt_IfStmt(self, node, parent):
        TrueBlock = self.create_block()
        
    def visit_ReturnStmt(self, stmt):
        # create new block
        self.current_block = self.create_block(False)
        self.current_block.add_successor(self.cfg.blocks[-1]) # add exit block as successor
        return self.visitStmt(stmt, add_to_block=True)
        
    def visit_DeclStmt(self, stmt):
        self.visitStmt(stmt)

    def visit_Assignment(self, stmt):
        self.visitStmt(stmt)

    # TODO Build CFG for WhileStmt
    def visitStmt_WhileStmt(self, stmt):
        loop_successor = None

        # add loop exit block, for analysis only
        # self.auto_create_block()
        # self.current_block.insert_stmt(stmt)
        
        # while is control-flow stmt, stop process current_block
        if (self.current_block):
            loop_successor = self.current_block
            self.current_block = None
        else:
            loop_successor = self.current_successor

        # process loop body stmtlist

        self.block_stack.append(self.current_block)
        self.succ_stack.append(self.current_successor)
        self.continue_jumptarget_stack.append(self.continue_jumptarget)
        self.break_jumptarget_stack.append(self.continue_jumptarget)

        transition_block = self.create_block(add_successor=False)
        self.current_successor = transition_block
        transition_block.set_loop_target(node)
        self.continue_jumptarget = self.current_successor
        self.break_jumptarget = loop_successor

        body_block = self.visit(node.body)

        if body_block is None:
            body_block = self.continue_jumptarget
        

        entry_cond_block = exit_cond_block = None
        cond = node.cond_expr
        print 'cond', cond.__class__.__name__
        if cond.__class__ is BinaryOp and cond.op in ['&&', '||']:
            entry_cond_block = exit_cond_block = visit_LogicalOp(cond, body_block, loop_successor)
        else:
            exit_cond_block = self.create_block(false)
            self.current_block = exit_cond_block
            self.current_block = entry_cond_block = self.visit(cond)

            # True and False cond, set 2 successors
            exit_cond_block.add_successor(body_block)
            exit_cond_block.add_successor(loop_successor)
            
        transition_block.add_successor(entry_cond_block)
        self.current_block = None
        self.current_successor = entry_cond_block
        return entry_cond_block

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
