#include "SerializeFile.h"

#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <string.h>
#include <stdio.h>

namespace naivescript{
namespace serialize {


#ifdef __cplusplus
extern "C" {
#endif
uint8_t * LoadBinaryFile(const char *filename)
{
    struct stat sbuf;
    if (stat(filename, &sbuf) < 0) {
        return NULL;
    }
    size_t filesize = sbuf.st_size;
    FILE* fd = fopen(filename, "rb");
    uint8_t *filebody = (uint8_t *)malloc(filesize);
    memset(filebody, filesize, 0);
    fread (filebody, 1, filesize, fd);
    fclose(fd);
    return filebody;
}
#ifdef __cplusplus
}
#endif

bool SerializeFile::Load( const std::string& path ) 
{
    const char *filename = path.c_str();
    uint8_t *filebody = LoadBinaryFile(filename);

    FileFormat *file;
    file = reinterpret_cast<FileFormat*>( filebody ); 
    body_size = file->bodySize;
    string_table_size = file->stringtableSize;
     std::cout << "StringTableEntry: " << 
        file->stringTableEntry << std::endl;
    std::cout << "Bodyentry: " << 
        file->bodyEntry << std::endl;
    std::cout << "bodySize: " << 
        file->bodySize << std::endl;
    std::cout << "StringTableSize: " << 
        file->stringtableSize << std::endl;

    symbol_table.Parse(filebody + file->stringTableEntry, string_table_size);
    this->body = reinterpret_cast<u_int8_t *>(filebody + file->bodyEntry);
    return true;

}

}
}
