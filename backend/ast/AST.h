#ifndef AST_H
#define AST_H

#include "ASTNode.h"
#include "Util.h"
#include <map>


namespace naivecompiler{

class AST
{
public:
    bool Parse( struct serialize::AST * ast, size_t size );

    const std::vector<ASTNode *> GetChildren( void )
    {
        return children;
    }

    void show( int offset = 0 )
    {
    	std::string index = std::string(offset, '\t');
    	std::cout << index;
        std::cout <<  "AST  ";
        std::cout <<  "Node Count: " << count << std::endl;
        for (ASTNode * node : children) {
            node->show(offset+1);
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
