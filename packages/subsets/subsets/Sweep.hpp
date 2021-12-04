#pragma once

#include "common.hpp"

template<typename T>
vector<T> neibs_up(T u, int n) {
    vector<T> res;
    fori(i, n) {
        uint64_t bit = (1ull << i);
        if ((u & bit) == 0) {
            res.push_back(u ^ bit);
        }
    }
    return res;
}
template<typename T>
vector<T> neibs_down(T u, int n) {
    vector<T> res;
    fori(i, n) {
        uint64_t bit = (1ull << i);
        if ((u & bit) == 1) {
            res.push_back(u ^ bit);
        }
    }
    return res;
}


template<auto func, typename T>
void GenericSweep(vector<T> &arr, uint64_t mask) {
    auto size = arr.size();
    int n = log2(size);
    ensure(arr.size() == (1ull << n));
    fori(i, n) {
        uint64_t bit = (1ull << i);
        if ((mask & bit) == 0)
            continue;

        // fori(j, 1ull << n) {
        //     if (j & bit) {
        //         func(arr[j ^ bit], arr[j]);
        //     }
        // }

        // iterate over all submasks
        // slightly better than the above one
        // due to same branching full loop (~25% faster)
        uint64_t msk = ((1ull << n) - 1) ^ bit;
        uint64_t j = msk;
        fori(_, 1ull << (n-1)) {
            func(arr[j], arr[j | bit]);
            j = (j - 1) & msk;
        }
    }
}

template<auto func, typename WORD>
static inline void GenericSweepWordBit(WORD &word, int shift, WORD mask) {
    // /!\ here mask corresponds to word mask,
    // not index mask as in other places !!!
    WORD lo = word & mask;
    WORD hi = (word >> shift) & mask;
    func(lo, hi);
    word = (hi << shift) | lo;
}

constexpr uint64_t MASK64_SINGLE[6] = {
    0x5555555555555555ull,
    0x3333333333333333ull,
    0x0f0f0f0f0f0f0f0full,
    0x00ff00ff00ff00ffull,
    0x0000ffff0000ffffull,
    0x00000000ffffffffull,
};

template<auto func>
static inline void GenericSweepWord(uint64_t &word, uint64_t mask) {
    if (mask & ( 1)) GenericSweepWordBit<func>(word,  1, MASK64_SINGLE[0]);
    if (mask & ( 2)) GenericSweepWordBit<func>(word,  2, MASK64_SINGLE[1]);
    if (mask & ( 4)) GenericSweepWordBit<func>(word,  4, MASK64_SINGLE[2]);
    if (mask & ( 8)) GenericSweepWordBit<func>(word,  8, MASK64_SINGLE[3]);
    if (mask & (16)) GenericSweepWordBit<func>(word, 16, MASK64_SINGLE[4]);
    if (mask & (32)) GenericSweepWordBit<func>(word, 32, MASK64_SINGLE[5]);
}


TTi void WALSH_HADAMARD(T &a, T &b) { T plus = a + b; b = a - b; a = plus; }

TTi void XOR_down(T &a, T &b) { a ^= b; }
TTi void XOR_up(T &a, T &b) { b ^= a; }
TTi void OR_down(T &a, T &b) { a |= b; }
TTi void OR_up(T &a, T &b) { b |= a; }
TTi void AND_down(T &a, T &b) { a &= b; }
TTi void AND_up(T &a, T &b) { b &= a; }

TTi void SWAP(T &a, T &b) { swap(a, b); }

// b &= (a < b)
TTi void LESS_up(T &a, T &b) { b &= ~a; }
// a &= (a > b)
TTi void MORE_down(T &a, T &b) { a &= ~b; }

TTi void ZERO_up(T &a, T &b) { b = 0; }
TTi void ZERO_down(T &a, T &b) { a = 0; }
TTi void ONE_up(T &a, T &b) { b = 1; }
TTi void ONE_down(T &a, T &b) { a = 1; }