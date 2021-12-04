#pragma once

#include "hackycpp.h"

static inline int hw(u64 x) {
    return __builtin_popcountll(x);
}

static inline int log2(u64 n) {
    ensure((n & (n - 1)) == 0);
    ensure(n != 0);
    int ret = __builtin_ctzll(n);
    ensure((1ull << ret) == n);
    return ret;
}

static inline int log3(u64 n) {
    ensure(n != 0);
    int ret = 0;
    while (n > 1) {
        ret += 1;
        n /= 3;
    }
    return ret;
}

static inline uint64_t pow3(int e) {
    ensure(e >= 0);
    uint64_t ret = 1;
    uint64_t cur = 3;
    while (e) {
        if (e & 1) {
            ret = ret * cur;
        }
        e >>= 1;
        cur = cur * cur;
    }
    return ret;
}