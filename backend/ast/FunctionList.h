#ifndef FUNTIONLIST_H
#define FUNTIONLIST_H

#include "NaiveScript.h"
#include "ASTNode.h"
#include "NodeFactory.h"
#include "Function.h"
#include "Util.h"


namespace naivescript{

class FunctionList
{
public:
    bool Parse( struct serialize::FunctionList * func_list, size_t size )
    {
        std::cout << "Parsing FunctionList ";
        count =  func_list->count;
        std::cout << "Count: " << count << std::endl;
        uint8_t * data = func_list->data;
        size_t node_size;
        for (size_t i=0; i<count; i++) {
            node_size = util::getVarStructSize(data);
            children.push_back(NodeFactory::CreateFunction(data, node_size));
            data += node_size;
        }
        return true;
    }

    const std::vector<Function *> GetChildren( void ) 
    {
        return children;
    }

    void show( void )
    {
        std::cout <<  "FunctionList\t";
        std::cout <<  "Node Count: " << count << std::endl;
        for (Function * node : children) {
            node->show();
        }
    }

    std::vector<llvm::Function*> accept(Visitor* v);

    ~FunctionList() {
        for (Function * node : children) {
            free(node);
        }
    }

private:
    size_t count;
    std::vector<Function*> children;
};

}
#endif