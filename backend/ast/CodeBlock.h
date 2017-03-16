#ifndef CODEBLOCK_H
#define CODEBLOCK_H

#include "NaiveScript.h"
#include "ASTNode.h"
#include "NodeFactory.h"
#include "DeclarationList.h"
#include "StmtList.h"
#include "Util.h"


namespace naivescript{

class CodeBlock : public ASTNode
{
public:
    virtual bool Parse( struct serialize::CodeBlock * body, size_t size )
    {
        std::cout << "Parsing CodeBlock ";
        uint8_t *p_decls = (uint8_t *)(body->decls.data);
        uint8_t *p_stmts = p_decls + body->decls_size;
        decls = NodeFactory::CreateDeclarationList(p_decls, body->decls_size);
        stmts = NodeFactory::CreateStmtList(p_stmts, body->stmts_size);
        children.push_back(decls);
        children.push_back(stmts);
        return true;
    }

    virtual const std::vector<ASTNode *> GetChildren( void ) override
    {
        return children;
    }

    StmtList* GetStmts(void)
    {
        return static_cast<StmtList*>(stmts);
    }

    DeclarationList* GetDecls(void)
    {
        return static_cast<DeclarationList*>(decls);
    }

    virtual void show( void ) override
    {
        std::cout <<  "CodeBlock\t";
        for (ASTNode * node : children) {
            node->show();
        }
    }

    virtual llvm::Value* accept(Visitor* v) override;

    ~CodeBlock() {
        for (ASTNode * node : children) {
            free(node);
        }
    }

private:
    ASTNode *decls;
    ASTNode *stmts;
    std::vector<ASTNode*> children;
};

}

#endif