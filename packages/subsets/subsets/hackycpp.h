#pragma once

#include <string>
#include <vector>
#include <exception>
#include <stdexcept>

#include <set>
#include <map>
#include <unordered_set>
#include <unordered_map>

#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <stdint.h>

using namespace std;

typedef uint64_t u64;
typedef uint32_t u32;
typedef uint16_t u16;
typedef uint8_t u8;

typedef int64_t i64;
typedef int32_t i32;
typedef int16_t i16;
typedef int8_t i8;

#define TTi template<typename T> inline

#define __CONCAT3_NX(x, y, z) x ## y ## z
#define __CONCAT3(x, y, z) __CONCAT3_NX(x, y, z)
#define __VAR(name) __CONCAT3(__tmpvar__, name, __LINE__)

// https://stackoverflow.com/a/11763277
// overload by number of arguments
#define GET_MACRO3(_1, _2, _3, NAME, ...) NAME

#define fori(i, ...) GET_MACRO3(__VA_ARGS__, fori3, fori2, fori1)(i, __VA_ARGS__)
#define fori1(i, end) \
    for (int64_t i = 0, __VAR(vend) = (end); i < __VAR(vend); i++)
#define fori2(i, start, end) \
    for (int64_t i = (start), __VAR(vend) = (end); i < __VAR(vend); i++)
#define fori3(i, start, end, step) \
    for (int64_t i = (start), __VAR(vend) = (end), __VAR(vstep) = (step); i < __VAR(vend); i += __VAR(vstep))

#define rfori(i, ...) GET_MACRO3(__VA_ARGS__, rfori3, rfori2, rfori1)(i, __VA_ARGS__)
#define rfori1(i, end) \
    for (int64_t i = (end)-1; i >= 0; i--)
#define rfori2(i, start, end) \
    for (int64_t i = (end)-1, __VAR(vstart) = (start); i >= __VAR(vstart); i--)
#define rfori3(i, start, end, step) \
    for (int64_t __VAR(vstart) = (start), __VAR(vstep) = (step), i = __VAR(vstart) + (((end)-1-__VAR(vstart)) / __VAR(vstep)) * __VAR(vstep); i >= __VAR(vstart); i -= __VAR(vstep))


#define GET_MACRO2(_1, _2, NAME, ...) NAME
#define ensure1(cond) _ensure(cond, __FILE__, __LINE__, __PRETTY_FUNCTION__, #cond, "")
#define ensure2(cond, err) _ensure(cond, __FILE__, __LINE__, __PRETTY_FUNCTION__, #cond, err)
#define ensure(...) GET_MACRO2(__VA_ARGS__, ensure2, ensure1)(__VA_ARGS__)

TTi void _ensure(T cond, const char *file, int lno, const char *func, const char *condstr, const char * err) {
    if (!cond) {
        string res;
        res = res + err + " (at " + file + ":" + to_string(lno) + ":" + func + " " + ", expression: " + condstr + " )";
        throw std::runtime_error(res.c_str());
    }
    assert(cond);  // for compiler hints
}