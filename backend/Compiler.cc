#include "Compiler.h"

namespace naivescript
{
Compiler* Compiler::instance = 0;

void Compiler::Compile( void ) 
{
    u_int8_t *body = const_cast<u_int8_t *>(file.GetBody());
    func_list.Parse(reinterpret_cast<struct serialize::FunctionList*>(body),
    file.GetBodySize() );
    func_list.show();
    genVisitor.run(&func_list);
}

}
