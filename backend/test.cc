#include "Compiler.h"
#include <string>

using namespace naivescript;

int main() {
    Compiler * compiler = Compiler::GetCompiler();
    compiler->LoadData("ns.data");
    compiler->Compile();
}
