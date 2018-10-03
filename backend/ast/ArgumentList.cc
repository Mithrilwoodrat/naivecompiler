#include "ArgumentList.h"
#include "Compiler.h"
#include "NodeFactory.h"

namespace naivecompiler{
bool ArgumentList::Parse( struct serialize::ArgumentList * args, size_t size )
{
    std::cout << "Parsing ArgumentList ";;
    count =  args->count;
    std::cout << "Count: " << count << std::endl;
    uint8_t * data = args->data;
    size_t total_size = 0;
    size_t node_size;
    // argument : varsymbol
    //          | constant
    for (size_t i=0; i<count; i++) {
        if (total_size > size)
             break;
        uint32_t type = util::getStructType(data);
        switch(type) {
            case serialize::TypeValue:
                node_size = getStructSize(serialize::Value);
                children.push_back(NodeFactory::CreateValue(data, node_size));
                break;
            case serialize::TypeSymbol:
                node_size = getStructSize(serialize::Symbol);
                children.push_back(NodeFactory::CreateSymbol(data, node_size));
                break;
            default:
                std::cout << "Error when parsing ArgumentList, wrong arg type" << std::endl;
                return false;
        }
        total_size += node_size;
        data += node_size;
    }
    return true;
}

llvm::Value* ArgumentList::accept(Visitor* v)
{
    return v->visit(this);
}

}