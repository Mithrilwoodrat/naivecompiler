#ifndef FUNTIONLIST_H
#define FUNTIONLIST_H

#include "ASTNode.h"
#include "FunctionNode.h"
#include "Util.h"
#include <map>


namespace naivescript{

class FunctionList
{
public:
    bool Parse( struct serialize::FunctionList * func_list, size_t size );

    const std::vector<FunctionNode *> GetChildren( void ) 
    {
        return children;
    }

    void show( void )
    {
        std::cout <<  "FunctionList\t";
        std::cout <<  "Node Count: " << count << std::endl;
        for (FunctionNode * node : children) {
            node->show();
        }
    }

    std::map<std::string, llvm::Function*> accept(Visitor* v);

    ~FunctionList() {
        for (FunctionNode * node : children) {
            free(node);
        }
    }

private:
    size_t count;
    std::vector<FunctionNode*> children;
};

}
#endif