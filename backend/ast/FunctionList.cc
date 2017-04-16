#include "FunctionList.h"
#include "Compiler.h"
#include "NodeFactory.h"

namespace naivescript
{
bool FunctionList::Parse( struct serialize::FunctionList * func_list, size_t size )
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

std::map<std::string, llvm::Function*>FunctionList::accept(Visitor* v)
{
    return v->visit(this);
}

}