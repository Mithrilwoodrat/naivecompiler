#include <Util.h>

namespace naivescript
{

namespace util
{
#ifdef __cplusplus
extern "C" {
#endif
uint32_t getStructType(uint8_t* data) {
    return *((uint32_t*)(data));
}

uint32_t getVarStructSize(uint8_t* data) {
    return *((uint32_t*)(data) + 1);
}

void debug_parse(uint8_t *data, uint32_t size) {
    uint32_t i;
    for(i=0;i<size;i++)
        printf("%x", *data++);
    printf("\n");
}

#ifdef __cplusplus
}
#endif
}
}

