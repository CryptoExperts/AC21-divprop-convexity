#pragma once

#include <functional>

#include "common.hpp"
#include "ternary.hpp"
#include "DenseSet.hpp"
#include "Sweep3.hpp"

struct DenseTernary {
    int n;
    uint64_t fullsize;
    vector<BITSET3> data;

    static inline uint64_t HI(uint64_t x) {
        return x / BITSET3_PER3;
    }
    static inline uint64_t LO(uint64_t x) {
        return x % BITSET3_PER3;
    }

    DenseTernary();
    DenseTernary(int _n);
    DenseTernary(const DenseSet & d);

    int get(uint64_t x) const;
    void set(uint64_t x);

    #ifndef SWIG
    template<auto func>
    void do_Sweep(uint64_t mask = -1ull) {
        mask &= (1ull << n)-1;
        // we can use GenericTernarySweep
        // pretending we have bit-slice 64 parallel sets in our array
        uint64_t mask_hi = mask >> BITSET3_LOG3;
        if (mask_hi) {
            GenericSweep3<func>(data, mask_hi);
        }
        // and then it's only left to Sweep each word
        uint64_t mask_lo = mask & ((1ull << BITSET3_LOG3) - 1);
        if (mask_lo) {
            for(auto &word: data) {
                GenericSweep3Word<func>(word, mask_lo);
            }
        }
    }
    #endif

    void do_Sweep_QmC_AND_up_OR(uint64_t mask = -1ull);
    void do_Sweep_QmC_NOTAND_down(uint64_t mask = -1ull);
    void do_QuineMcCluskey(uint64_t mask = -1ull);

    void iter_support(std::function<void(uint64_t x)> const & func) const;

    std::vector<uint64_t> get_support() const;
    uint64_t get_weight() const;

    #ifdef SWIG
    %pythoncode %{
    def __contains__(self, x):
        return bool(self.get(x))
    def __iter__(self):
        return iter(self.get_support())
    def __len__(self):
        return self.get_weight()
    %}
    #endif
};