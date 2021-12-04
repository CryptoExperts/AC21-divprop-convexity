#pragma once

#include "common.hpp"
#include "ternary.hpp"


template<auto func, typename T>
void GenericSweep3(vector<T> &arr, uint64_t mask) {
    auto size = arr.size();
    int n = log3(size);
    ensure(arr.size() == pow3(n));

    uint64_t hi = size / 3;
    uint64_t hi_stride = 3;
    uint64_t lo = 1;
    fori(i, n) {
        if ((mask & (1ull << i))) {
            uint64_t j = 0;
            fori(_, hi) {
                fori(_, lo) {
                    auto j1 = j + lo;
                    auto j2 = j1 + lo;
                    func(arr[j], arr[j1], arr[j2]);
                    j++;
                }
                j -= lo;
                j += hi_stride;
            }
        }
        hi /= 3;
        hi_stride *= 3;
        lo *= 3;
    }
}

template<auto func, typename WORD>
static inline void GenericSweep3WordBit(WORD &word, int shift, const WORD & mask) {
    // /!\ here mask corresponds to word mask,
    // not index mask as in other places !!!
    WORD v0 = word & mask;
    word = word >> shift;
    WORD v1 = word & mask;
    word = word >> shift;
    WORD v2 = word & mask;

    func(v0, v1, v2);

    word = ((v2 << shift) <<shift) | (v1 << shift) | v0;
}

template<auto func, typename WORD>
static inline void GenericSweep3Word(WORD &word, uint64_t mask) {
    if (mask & ( 1)) GenericSweep3WordBit<func>(word, 1,   MASKS_TERNARY[0]);
    if (mask & ( 2)) GenericSweep3WordBit<func>(word, 3,   MASKS_TERNARY[1]);
    if (mask & ( 4)) GenericSweep3WordBit<func>(word, 9,   MASKS_TERNARY[2]);
    if (mask & ( 8)) GenericSweep3WordBit<func>(word, 27,  MASKS_TERNARY[3]);
    if (mask & (16)) GenericSweep3WordBit<func>(word, 81,  MASKS_TERNARY[4]);
    if (mask & (32)) GenericSweep3WordBit<func>(word, 243, MASKS_TERNARY[5]);
}


TTi void QmC_AND_up_OR(T & a, T & b, T & c) {
    c |= a & b;
}
TTi void QmC_NOTAND_down(T & a, T & b, T & c) {
    T nc = ~c;
    a &= nc;
    b &= nc;
}