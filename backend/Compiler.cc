#include "Compiler.h"

namespace naivecompiler
{
Compiler* Compiler::instance = 0;

void Compiler::Compile( char * filename , bool dumpIR = true)
{
    u_int8_t *body = const_cast<u_int8_t *>(file.GetBody());
    ast.Parse(reinterpret_cast<struct serialize::AST*>(body),
              file.GetBodySize() );
    ast.show();
    genVisitor.dump(&ast);
    std::string Filename(filename);
    genVisitor.GenObj(Filename);
}

}
#ifdef __cplusplus
extern "C" {
#endif

void InitCompiler( void ) 
{
    naivecompiler::Compiler::GetCompiler();
}

void LoadData(char * path)
{
    naivecompiler::Compiler::GetCompiler()->LoadData(path);
}

void Compile(  char * filename )
{
    naivecompiler::Compiler::GetCompiler()->Compile(filename);
}

#ifdef __cplusplus
}
#endif
