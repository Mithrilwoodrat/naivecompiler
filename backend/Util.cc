#include <Util.h>
#include "SerializeStructure.h"

namespace naivecompiler
{

namespace util
{
#ifdef __cplusplus

uint32_t getValueType(uint8_t* data) {
	struct serialize::Value* value = reinterpret_cast<struct serialize::Value*>(data);
	return value->valuetype;
}

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
