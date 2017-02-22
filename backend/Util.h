#ifndef UTIL_H
#define UTIL_H

#include <stdint.h>

#define  getStructSize(s) (sizeof(s))

namespace naivescript
{

namespace util
{
extern "C"
{
uint32_t getStructType(uint8_t *s);
uint32_t getVarStructSize(uint8_t* data);

}
}

}
#endif