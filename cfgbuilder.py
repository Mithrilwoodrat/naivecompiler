# -*- coding: utf-8 -*-
import logging
import sys

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
    cfgs = {}
    for c in ast.children():
        if c.__class__ is FuncDef:
            cfg = CFG.build_cfg(c.body, c)
            cfgs[c] = cfg
    return cfgs


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
        cfgs = cfgbuilder.build_cfg(stmtlist, funcdef)
        return cfgs

    def show(self):
        blocks = self.blocks
        for b in blocks:
            print b.block_id, b.block_name
            for stmt in b.stmts:
                stmt.show()
            print 'Succs:', [i.block_id for i in b.successors], '\n'

    def get_entry(self):
        return self.entry_block
            
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

    def save_current_successor(self):
        self.successor_stack.append(self.current_successor)
        self.current_successor = None

    def restore_current_successor(self):
        self.current_successor =  self.successor_stack.pop()

    def save_current_block(self):
        self.block_stack.append(self.current_block)
        self.current_block = None

    def restore_current_block(self):
        self.current_block =  self.block_stack.pop()

    def save_break_jumptarget(self):
        self.break_jumptarget_stack.append(self.break_jumptarget)

    def restore_break_jumptarget(self):
        self.break_jumptarget =  self.break_jumptarget_stack.pop()

    def save_continue_jumptarget(self):
        self.continue_jumptarget_stack.append(self.continue_jumptarget)

    def restore_continue_jumptarget(self):
        self.continue_jumptarget = self.continue_jumptarget_stack.pop()

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

        self.cfg.set_entry(self.create_block())

        return self.cfg

    def try_eval_bool(self, cond):
        if cond.__class__ is Const:
            if cond._type == 'int':
                return cond.val > 0
        return None

    # https://code.woboq.org/llvm/clang/lib/Analysis/CFG.cpp.html VisitCompoundStmt
    def visit_StmtList(self, node):
        last_block = self.current_block
        for c in node.children()[::-1]:
            tmp = self.visit(c)
            if tmp:
                last_block = tmp
        return last_block
        
    def visit_BreakStmt(self, node):
        self.current_block = self.create_block(False)
        self.current_block.Terminator = node
        if self.break_jumptarget:
            self.current_block.add_successor(self.break_jumptarget)
            self.current_block.insert_stmt(ABSJMP(self.break_jumptarget.block_id))
        return self.current_block

    def visit_IfStmt(self, node):
        if self.current_block: # stop process current block
            self.current_successor = self.current_block

        # 若没有 else， else block 设置为后续语句
        else_block = self.current_successor

        if (node._else is not None):
            self.save_current_successor()

            self.current_block = None # set current block to None, so visit will create new block

            else_block = self.visit(node._else)
            self.restore_current_successor()

        then_block = None
        self.save_current_successor()
        self.current_block = None
        then_block = self.visit(node.then)
        self.restore_current_successor()

        last_block = None
        cond = node.cond
        if cond.is_logicalOp():
            last_block = self.visit_LogicalOp(cond,then_block, else_block)[0]
        else:
            # create new empty block
            self.current_block = self.create_block(False)
            self.current_block.set_terminator(node)

            # self.current_block.insert_stmt(CMPJMP(cond, then_block.block_id, else_block.block_id))

            self.current_block.add_successor(then_block)
            self.current_block.add_successor(else_block)
            last_block = self.visit_BinaryOp(cond, then_block, else_block)


        TrueBlock = self.create_block()
        
    def visit_ReturnStmt(self, stmt):
        # create new block
        self.current_block = self.create_block(False)
        self.current_block.add_successor(self.cfg.blocks[-1]) # add exit block as successor
        return self.visitStmt(stmt, add_to_block=True)
        
    def visit_DeclStmt(self, stmt):
        return self.visitStmt(stmt)

    def visit_Assignment(self, stmt):
        return self.visitStmt(stmt)

    def visit_BinaryOp(self, node, true_block, false_block):
        if node.is_logicalOp():
            return self.visit_LogicalOp(node, None, None)
        else:
            # logger.warning('unsupported op: {}'.format(node.op))
            self.auto_create_block()
            self.current_block.insert_stmt(CMPJMP(node, true_block.block_id, false_block.block_id))
            return None

    def visit_LogicalOp(self, cond, true_block, false_block):
        rhs = cond.rhs
        rhs_block = exit_block = None

        if rhs.is_logicalOp():
            rhs_block, exit_block = self.visit_LogicalOp(rhs, true_block, false_block)
        else:
            rhs_block = exit_block = self.create_block(False)

            rhs_block.set_terminator(cond)

            rhs_block.add_successor(true_block)
            rhs_block.add_successor(false_block)
            self.current_block = rhs_block
            rhs_block.insert_stmt(CMPJMP(rhs, true_block.block_id, false_block.block_id))

        lhs = cond.lhs

        if lhs.is_logicalOp():
            if lhs.op == '||':
                return self.visit_LogicalOp(lhs, true_block, rhs_block)
            elif lhs.op == '&&':
                return self.visit_LogicalOp(lhs, rhs_block, false_block)

        lhs_block = self.create_block(False)
        lhs_block.set_terminator(lhs)

        self.current_block = lhs_block
        try_result = self.try_eval_bool(lhs)
        if try_result:
            pass
        else:
            if cond.op == "||":
                lhs_block.add_successor(true_block)
                lhs_block.add_successor(rhs_block)
                lhs_block.insert_stmt(CMPJMP(lhs, true_block.block_id, rhs_block.block_id))
            elif cond.op == '&&':
                lhs_block.add_successor(rhs_block)
                lhs_block.add_successor(false_block)
                lhs_block.insert_stmt(CMPJMP(lhs, rhs_block.block_id, false_block.block_id))

        return lhs_block, exit_block

    # TODO Build CFG for WhileStmt
    def visit_WhileStmt(self, stmt):
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

        loop_successor.block_name = 'loop_succ'

        # process loop body stmtlist

        self.save_current_block()
        self.save_current_successor()
        self.save_break_jumptarget()
        self.save_continue_jumptarget()

        transition_block = self.create_block(add_successor=False)
        transition_block.block_name = 'transition_block'
        self.current_successor = transition_block
        transition_block.set_loop_target(stmt)

        self.continue_jumptarget = self.current_successor
        self.break_jumptarget = loop_successor

        body_block = self.visit(stmt.body)
        body_block.block_name = "while_body"

        if body_block is None:
            body_block = self.continue_jumptarget

        self.restore_current_block()
        self.restore_current_successor()
        self.restore_break_jumptarget()
        self.restore_continue_jumptarget()

        entry_cond_block = exit_cond_block = None
        cond = stmt.cond_expr

        if cond.__class__ is BinaryOp and cond.op in ['&&', '||']:
            entry_cond_block , exit_cond_block = self.visit_LogicalOp(cond, body_block, loop_successor)
        else:
            exit_cond_block = self.create_block(False)
            entry_cond_block = exit_cond_block
            self.current_block = exit_cond_block

            try_result = self.try_eval_bool(cond)
            if try_result:
                if try_result == True:
                    exit_cond_block.add_successor(body_block)
                    self.current_block.insert_stmt(ABSJMP(body_block.block_id))
                elif try_result == False:
                    exit_cond_block.add_successor(loop_successor)
                    self.current_block.insert_stmt(ABSJMP(loop_successor.block_id))
            else:
                cond_block = self.visit_BinaryOp(cond, body_block, loop_successor) # 如果 cond 中有赋值的操作，添加到 entry_cond_block
                if cond_block:
                    self.current_block = entry_cond_block = cond_block

                # True and False cond, set 2 successors
                exit_cond_block.add_successor(body_block)
                exit_cond_block.add_successor(loop_successor)


        transition_block.add_successor(entry_cond_block)
        transition_block.insert_stmt(ABSJMP(entry_cond_block.block_id))

        exit_cond_block.block_name = 'exit_cond_block'
        self.current_block = None
        self.current_successor = entry_cond_block
        return entry_cond_block
