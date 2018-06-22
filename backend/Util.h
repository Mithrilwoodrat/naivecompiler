#ifndef UTIL_H
#define UTIL_H

#include <stdint.h>
namespace naivescript
{

namespace util
{
#ifdef __cplusplus
uint32_t getValueType(uint8_t *data);
extern "C"
#endif
{
#include <stdio.h>
#define  getStructSize(s) (sizeof(struct s))
uint32_t getStructType(uint8_t *s);
uint32_t getVarStructSize(uint8_t* data);
void debug_parse(uint8_t *data, uint32_t size);
#ifdef __cplusplus
}
#endif
}
}
#endif
