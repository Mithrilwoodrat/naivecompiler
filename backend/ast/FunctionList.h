#ifndef FUNTIONLIST_H
#define FUNTIONLIST_H

#include "ASTNode.h"
#include "NodeFactory.h"
#include "FunctionNode.h"
#include "Util.h"
#include <map>


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