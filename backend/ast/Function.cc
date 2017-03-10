#include "Function.h"
#include "Compiler.h"
#include "NodeFactory.h"

namespace naivescript
{

bool Function::Parse( struct serialize::Function * func, size_t size )
{
    std::cout << "Parsing Function ";
    func_name = Compiler::GetCompiler()->ResolveSymbol(func->id);
    return_type = func->return_type;
    uint8_t *p_params_list = (uint8_t *)(func->param_list.data);
    uint8_t *p_body = p_params_list + func->params_size;
    params_list = NodeFactory::CreateDeclarationList(p_params_list, func->params_size);
    body = NodeFactory::CreateCodeBlock(p_body, func->body_size);
    children.push_back(params_list);
    children.push_back(body);
    return true;
}

llvm::Value* Function::accept(Visitor* v)
{
    return v->visit(this);
}

}