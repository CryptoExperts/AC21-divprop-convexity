#pragma once

#include <functional>

#include "common.hpp"

#include "BitSet.hpp"

#ifdef SWIG
%pythoncode %{
from binteger import Bin
%}
#endif

using namespace Pack64;

struct DenseBox;

/*
Working with single bit vector, represented as vector<uint64_t>.
*/
struct DenseSet {
    int n; // n input bits
    BitSet data;

    static void set_quiet(bool value=true);

    DenseSet() : n(0) {};
    DenseSet(int _n) : n(_n), data(1ull << _n) {
        ensure(n >= 0 and n <= 64, "supported set dimension is between 0 and 64");
    };
    DenseSet(int n, const std::vector<uint64_t> &ints);

    DenseSet copy() const;
    void resize(uint64_t n);
    void clear(); // set to empty set with n=0

    void empty(); // set to empty set, keep n
    void fill(); // set to full set, keep n

    bool is_empty() const;
    bool is_full() const;

    // ========================================
    // Read/Write & info
    // ========================================
    void save_to_file(const char *filename) const;
    static DenseSet load_from_file(const char *filename);
    uint64_t get_hash() const;
    std::string info() const;

    // ========================================
    // Single bit get/set
    // ========================================
    int get(uint64_t x) const;
    void set(uint64_t x);
    void flip(uint64_t x);
    void unset(uint64_t x);
    void set(uint64_t x, uint64_t value);

    void add(uint64_t x);
    void remove(uint64_t x);
    void discard(uint64_t x);

    bool is_compatible_set(const DenseSet & b) const;

    // ========================================
    // Comparison
    // ========================================
    bool operator==(const DenseSet & b) const;
    bool operator!=(const DenseSet & b) const;
    bool operator<(const DenseSet & b) const;
    bool operator<=(const DenseSet & b) const;
    bool operator>(const DenseSet & b) const;
    bool operator>=(const DenseSet & b) const;

    // ========================================
    // Bitwise ops
    // ========================================
    DenseSet & operator|=(const DenseSet & b);
    DenseSet & operator^=(const DenseSet & b);
    DenseSet & operator&=(const DenseSet & b);
    DenseSet & operator-=(const DenseSet & b);
    DenseSet operator|(const DenseSet & b) const;
    DenseSet operator^(const DenseSet & b) const;
    DenseSet operator&(const DenseSet & b) const;
    DenseSet operator-(const DenseSet & b) const;
    // DenseSet operator~() const; // ambigouos

    DenseSet get_head_fixed(int h, uint64_t value);

    // ========================================
    // Support
    // ========================================
    void iter_support(function<void(uint64_t)> const & func) const;
    std::vector<uint64_t> get_support() const;
    uint64_t get_weight() const;

    std::vector<uint64_t> get_counts_by_weights() const;
    std::map<std::pair<int,int>,uint64_t> get_counts_by_weight_pairs(int n1, int n2) const;
    std::string str_stat_by_weights() const;
    std::string str_stat_by_weight_pairs(int n1, int n2) const;

    // ========================================
    // Tools
    // ========================================
    #ifndef SWIG
    template<auto func>
    void do_Sweep(uint64_t mask = -1ull) {
        mask &= (1ull << n)-1;
        // we can use GenericSweep
        // pretending we have bit-slice 64 parallel sets in our array
        if (HI(mask)) {
            GenericSweep<func>(data.data, HI(mask));
        }
        // and then it's only left to Sweep each word
        if (LO(mask)) {
            for(uint64_t &word: data.data) {
                GenericSweepWord<func>(word, LO(mask));
            }
        }
    }
    #endif
    // for python low-level API
    void do_Sweep_OR_up(uint64_t mask = -1ull);
    void do_Sweep_OR_down(uint64_t mask = -1ull);
    void do_Sweep_XOR_up(uint64_t mask = -1ull);
    void do_Sweep_XOR_down(uint64_t mask = -1ull);
    void do_Sweep_AND_up(uint64_t mask = -1ull);
    void do_Sweep_AND_down(uint64_t mask = -1ull);
    void do_Sweep_SWAP(uint64_t mask = -1ull);
    void do_Sweep_LESS_up(uint64_t mask = -1ull);
    void do_Sweep_MORE_down(uint64_t mask = -1ull);

    // ========================================
    // Main methods
    // ========================================
    void do_UnsetUp(uint64_t mask = -1ull);
    void do_UnsetDown(uint64_t mask = -1ull);
    void do_SetUp(uint64_t mask = -1ull);
    void do_SetDown(uint64_t mask = -1ull);

    void do_Mobius(uint64_t mask = -1ull);
    void do_ParitySet(uint64_t mask = -1ull);
    void do_Complement();
    void do_Not(uint64_t mask = -1ull);
    void do_UpperSet(uint64_t mask = -1ull);
    void do_LowerSet(uint64_t mask = -1ull);
    void do_MinSet(uint64_t mask = -1ull);
    void do_MaxSet(uint64_t mask = -1ull);
    void do_DivCore(uint64_t mask = -1ull);
    void do_ComplementU2L(bool is_upper=false, uint64_t mask = -1ull);
    void do_ComplementL2U(bool is_lower=false, uint64_t mask = -1ull);
    void do_UpperSet_Up1(bool is_minset=false, uint64_t mask = -1ull);

    std::vector<int64_t> WalshHadamard(uint64_t mask = -1ull) const;
    DenseSet Mobius(uint64_t mask = -1ull) const;
    DenseSet ParitySet(uint64_t mask = -1ull) const;
    DenseSet Complement() const;
    DenseSet Not(uint64_t mask = -1ull) const;
    DenseSet UpperSet(uint64_t mask = -1ull) const;
    DenseSet LowerSet(uint64_t mask = -1ull) const;
    DenseSet MinSet(uint64_t mask = -1ull) const;
    DenseSet MaxSet(uint64_t mask = -1ull) const;
    DenseSet DivCore(uint64_t mask = -1ull) const;
    DenseSet ComplementU2L(bool is_upper=false, uint64_t mask = -1ull) const;
    DenseSet ComplementL2U(bool is_lower=false, uint64_t mask = -1ull) const;
    DenseSet UpperSet_Up1(bool is_minset=false, uint64_t mask = -1ull) const;

    // static uint64_t project_to_Box(uint64_t v, const std::vector<uint64_t> & dimensions);
    DenseBox to_DenseBox(const std::vector<uint64_t> & dimensions) const;

    #ifdef SWIG
    %pythoncode %{
    def __bool__(self):
        return not self.is_empty()

    def __str__(self):
        return self.info()

    def __repr__(self):
        return self.info()

    def __contains__(self, x):
        return bool(self.get(x))

    def __iter__(self):
        return iter(self.get_support())

    def __len__(self):
        return self.get_weight()

    def __getitem__(self, x):
        return self.get(int(x))

    def __setitem__(self, x, v):
        assert int(v) in (0, 1)
        return self.set(int(x), int(v))

    def to_Bins(self):
        n = int(self.n)
        return [Bin(v, n) for v in self]

    def __getstate__(self):
        return self.n, self.data.__getstate__()

    def __setstate__(self, st):
        n, data = st
        self.__init__(n)
        self.data.__setstate__(data)
        return self
    %}
    #endif
};