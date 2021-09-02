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