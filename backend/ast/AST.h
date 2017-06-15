#ifndef FUNTIONLIST_H
#define FUNTIONLIST_H

#include "ASTNode.h"
#include "FunctionNode.h"
#include "Util.h"
#include <map>


namespace naivescript{

class AST
{
public:
    bool Parse( struct serialize::AST * ast, size_t size );

    const std::vector<ASTNode *> GetChildren( void )
    {
        return children;
    }

    void show( void )
    {
        std::cout <<  "AST\t";
        std::cout <<  "Node Count: " << count << std::endl;
        for (ASTNode * node : children) {
            node->show();
        }
    }

    std::map<std::string, llvm::Value*> accept(Visitor* v);

    ~AST() {
        for (ASTNode * node : children) {
            free(node);
        }
    }

private:
    size_t count;
    std::vector<ASTNode*> children;
};

}
#endif