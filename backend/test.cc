#include "Compiler.h"
#include <string>

using namespace naivescript;

int main() {
    Compiler * compiler = Compiler::GetCompiler();
    compiler->LoadData("ns.data");
    // ast::StmtList stmt_list;
    // char *body = const_cast<char *>(file_handler.GetBody());
    // stmt_list.Parse(reinterpret_cast<struct serialize::StmtList*>(body),
    //      file_handler.GetBodySize() );
}