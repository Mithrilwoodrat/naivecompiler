#include "NaiveScript.h"
#include <string>


int main() {
    InitCompiler();
    std::string spath = "ns.data";
    char *path = const_cast<char *>(spath.c_str());
    LoadData(path);
    Compile();
    return 0;
}
