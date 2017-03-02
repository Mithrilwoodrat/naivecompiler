#ifndef UTIL_H
#define UTIL_H

#include <stdint.h>

#define  getStructSize(s) (sizeof(s))

namespace naivescript
{

namespace util
{
#ifdef __cplusplus
extern "C"
#endif
{
uint32_t getStructType(uint8_t *s);
uint32_t getVarStructSize(uint8_t* data);
#ifdef __cplusplus
}
#endif
}
}
#endif
