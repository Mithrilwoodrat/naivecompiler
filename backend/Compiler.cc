#include "Compiler.h"

namespace naivescript
{
Compiler* Compiler::instance = 0;

void Compiler::Compile( char * filename ) 
{
    u_int8_t *body = const_cast<u_int8_t *>(file.GetBody());
    func_list.Parse(reinterpret_cast<struct serialize::FunctionList*>(body),
    file.GetBodySize() );
    func_list.show();
    genVisitor.dump(&func_list);
    std::string Filename(filename);
    genVisitor.GenObj(Filename);
}

}
#ifdef __cplusplus
extern "C" {
#endif

void InitCompiler( void ) 
{
    naivescript::Compiler::GetCompiler();
}

void LoadData(char * path)
{
    naivescript::Compiler::GetCompiler()->LoadData(path);
}

void Compile(  char * filename )
{
    naivescript::Compiler::GetCompiler()->Compile(filename);
}

#ifdef __cplusplus
}
#endif