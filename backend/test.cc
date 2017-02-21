#include "serialize/SerializeFile.h"
#include <string>

int main() {
    naivescript::serialize::SerializeFile file_handler("ns.data");
    file_handler.Load();
}