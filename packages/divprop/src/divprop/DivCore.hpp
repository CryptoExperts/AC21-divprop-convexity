#pragma once

#include <random>
#include <algorithm>

#include "hackycpp.h"

#include "DenseSet.hpp"

#ifdef SWIG
%pythoncode %{
import logging
log = logging.getLogger(__name__)
%}
#endif

template <typename T>
struct T_DivCore_StrongComposition {
    int n, r, m;
    std::vector<DenseSet> current;
    std::vector<T> tab1;
    std::vector<T> tab2;
    std::vector<T> keys_left;
    DenseSet _ones;

    DenseSet divcore;

    // T_DivCore_StrongComposition(int _n, int _r, int _m, const std::vector<T> &_tab1, const std::vector<T> &_tab2);
    T_DivCore_StrongComposition(
        int _n, int _r, int _m,
        const std::vector<T> &_tab1, const std::vector<T> &_tab2
    ) :
    n(_n), r(_r), m(_m), tab1(_tab1), tab2(_tab2), _ones(n), divcore(n + m)
    {
        ensure((uint64_t)n <= sizeof(T)*8);
        ensure((uint64_t)r <= sizeof(T)*8);
        ensure((uint64_t)m <= sizeof(T)*8);
        fori (k, 1ull << r) {
            keys_left.push_back(k);
        }
        _ones.fill();
        current.assign(1ull << m, DenseSet(n));
    }

    void set_keys(const std::vector<T> keys) {
        keys_left = keys;
    }

    #ifdef SWIG
    %pythoncode %{
    def process_logged(self, chunk=128):
        nkeys = 2**self.r
        ntotal = len(self.keys_left)
        while len(self.keys_left):
            self.process(chunk)
            proc = ntotal - len(self.keys_left)
            log.info(f"processed {proc}/{ntotal} keys")
    %}
    #endif

    void shuffle() {
        std::shuffle(keys_left.begin(), keys_left.end(), default_random_engine());
    }
    void process(uint64_t num = -1ull) {
        num = min(num, keys_left.size());
        vector<uint64_t> keys(keys_left.end() - num, keys_left.end());
        keys_left.erase(keys_left.end() - num, keys_left.end());
        #pragma omp parallel for
        for (auto key: keys) {
            _process_key(key);
        }
        _finalize();
    }
    void _process_key(uint64_t key) {
        vector<DenseSet> products(m, DenseSet(n));

        // compute single bit products
        // could compute all products in linear time
        // but increases memory usage
        // NOTE: reverse order (LSB to MSB)
        fori (i, m) {
            fori (x, 1ull << n) {
                uint64_t y = tab2[tab1[x] ^ key];
                int bit = (y >> i) & 1;
                products[i].set(x, bit);
            }
        }

        // alternative idea to improve cache usage:
        // precompute products say for current bunch of keys
        // iterate over v
        // inside each v run omp-for over keys
        // every thread works with one local func and one global func same for all threads

        DenseSet cur(n);
        fori (v, 1ull << m) {
            cur = _ones;
            auto tmp = v;
            fori (i, m) {
                if (tmp & 1) {
                    cur &= products[i];
                }
                tmp >>= 1;
            }

            cur.do_Mobius();

            // TBD: maybe make maxset here and iterate over support?

            #pragma omp critical(orthings)
            current[v] |= cur;
        }
    }
    void _finalize() {
        uint64_t umask = (1ull << n) - 1;
        fori (v, 1ull << m) {
            // since we have to iterate over bits anyway
            // better to reduce the size
            current[v].do_MaxSet();
            for (auto u: current[v].get_support()) {
                u ^= umask;
                divcore.set((u << m) | v);
            }
        }
        divcore.do_MinSet();
    }
};