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
    return *((uint32_t*)(data) + 2);
}
#ifdef __cplusplus
}
#endif
}
}

