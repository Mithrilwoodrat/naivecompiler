#include "FuncDeclNode.h"
#include "Compiler.h"
#include "NodeFactory.h"

namespace naivecompiler
{

bool FuncDeclNode::Parse( struct serialize::FuncDecl * func, size_t size )
{
    DLOG(LOG_DEBUG) << "Parsing Function: ";
    func_name = Compiler::GetCompiler()->ResolveSymbol(func->id);
    DLOG(LOG_DEBUG) << "Name:" << func_name << "\t";
    return_type = func->return_type;
    uint8_t *p_params_list = (uint8_t *)(func->param_list.data);
    params_list = NodeFactory::CreateDeclarationList(p_params_list, func->params_size);
    children.push_back(params_list);
    return true;
}

llvm::Value* FuncDeclNode::accept(Visitor* v)
{
    return v->visit(this);
}

}
