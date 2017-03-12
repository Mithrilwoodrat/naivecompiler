#ifndef DECLARACTIONLIST_H
#define DECLARACTIONLIST_H

#include "NaiveScript.h"
#include "ASTNode.h"
#include "NodeFactory.h"
#include "Declaration.h"
#include "Util.h"


namespace naivescript{

class DeclarationList : public ASTNode
{
public:
    virtual bool Parse( struct serialize::DeclarationList * decl_list, size_t size )
    {
        std::cout << "Parsing DeclarationList ";
        count =  decl_list->count;
        std::cout << "Count: " << count << std::endl;
        uint8_t * data = decl_list->data;
        size_t node_size = getStructSize(serialize::Declaration);
        size_t total_size = 0;
        for (size_t i=0; i<count; i++) {
            children.push_back(NodeFactory::CreateDeclaration(data, node_size));
            data += node_size;
            if (total_size > size)
                break;
            total_size += node_size;
        }
        return true;
    }

    virtual const std::vector<ASTNode *> GetChildren( void ) override
    {
        return children;
    }

    virtual void show( void ) override
    {
        std::cout <<  "DeclarationList\t";
        std::cout <<  "Node Count: " << count << std::endl;
        for (ASTNode * node : children) {
            node->show();
        }
    }

    virtual llvm::Value* accept(Visitor* v) override;

    ~DeclarationList() {
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