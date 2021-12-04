#pragma once

#include <functional>

#include "hackycpp.h"

#include "BitSet.hpp"
#include "DenseSet.hpp"


struct DenseBox {
    int n;
    uint64_t fullsize;
    std::vector<uint64_t> dimensions;
    BitSet data;

    static constexpr uint64_t VERSION = 0x9f5468a1d5ab66caull;
    static constexpr uint64_t MARKER_END = 0x19b780ddaffa5189ull;

    DenseBox() : n(0) {};
    #ifndef SWIG
    DenseBox(const std::vector<int> & dimensions);
    #endif
    DenseBox(const std::vector<uint64_t> & dimensions);

    DenseBox copy() const;

    void clear();
    void empty();
    void fill();

    bool is_empty() const;
    bool is_full() const;

    // ========================================
    // Read/Write & info
    // ========================================
    void save_to_file(const char *filename) const;
    void save_to_file(FILE *fd) const;
    static DenseBox load_from_file(const char *filename);
    static DenseBox load_from_file(FILE *fd);

    std::string info() const;
    void print() const;
    uint64_t get_hash() const;

    // ========================================
    // Single bit get/set
    // ========================================
    std::vector<uint64_t> unpack(uint64_t x) const;
    uint64_t pack(const std::vector<uint64_t> & xs) const;
    uint64_t project(const uint64_t x) const;

    static std::vector<uint64_t> _unpack(uint64_t x, const std::vector<uint64_t> & dimensions);
    static uint64_t _pack(const std::vector<uint64_t> & xs, const std::vector<uint64_t> & dimensions);
    static uint64_t _project(const uint64_t x, const std::vector<uint64_t> & dimensions);

    int get(uint64_t x) const;
    int get(const std::vector<uint64_t> & xs) const;
    void set(uint64_t x);
    void set(const std::vector<uint64_t> & xs);
    void unset(uint64_t x);
    void unset(const std::vector<uint64_t> & xs);
    void set(uint64_t x, uint64_t value);
    void set(const std::vector<uint64_t> & xs, uint64_t value);

    void add(uint64_t x);
    void remove(uint64_t x);
    void discard(uint64_t x);
    void add(const std::vector<uint64_t> & xs);
    void remove(const std::vector<uint64_t> & xs);
    void discard(const std::vector<uint64_t> & xs);

    // ========================================
    // Support
    // ========================================
    void iter_support(std::function<void(uint64_t x)> const & func) const;
    std::vector<uint64_t> get_support() const;
    std::vector<std::vector<uint64_t>> get_unpacked() const;
    uint64_t get_weight() const;
    std::vector<uint64_t> get_counts_by_weights() const;
    std::string str_stat_by_weights() const;

    // ========================================
    // Bitwise ops
    // ========================================
    bool is_compatible_set(const DenseBox & b) const;
    bool operator==(const DenseBox & b) const;
    bool operator!=(const DenseBox & b) const;
    bool operator<(const DenseBox & b) const;
    bool operator>(const DenseBox & b) const;
    bool operator<=(const DenseBox & b) const;
    bool operator>=(const DenseBox & b) const;

    // ========================================
    // Bitwise ops
    // ========================================
    DenseBox & operator|=(const DenseBox & b);
    DenseBox & operator^=(const DenseBox & b);
    DenseBox & operator&=(const DenseBox & b);
    DenseBox & operator-=(const DenseBox & b);
    DenseBox operator|(const DenseBox & b) const;
    DenseBox operator^(const DenseBox & b) const;
    DenseBox operator&(const DenseBox & b) const;
    DenseBox operator-(const DenseBox & b) const;
    DenseBox operator~() const;

    // ========================================
    // Sweeps
    // ========================================
    #ifndef SWIG
    template<auto func>
    void do_Sweep(uint64_t mask) {
        uint64_t div = 1;
        fori(ni, n) {
            if ((mask & (1ull << ni)) == 0)
                continue;

            int i = n - 1 - ni;
            uint64_t dim = (dimensions[i] + 1);
            fori(x, fullsize) {
                uint64_t val = (x / div) % dim;
                if (val == 0) {
                    std::vector<u8> bits(dim);
                    fori(j, dim) {
                        bits[j] = data.get(x + j * div);
                    }
                    func(bits);
                    fori(j, dim) {
                        data.set(x + j * div, bits[j]);
                    }
                }
            }
            div *= dim;
        }
    }
    #endif

    static inline void OR_up(vector<u8> &cut) {
        fori(i, 1, cut.size()) {
            cut[i] |= cut[i-1];
        }
    }
    static inline void OR_down(vector<u8> &cut) {
        rfori(i, cut.size()-1) {
            cut[i] |= cut[i+1];
        }
    }
    static inline void MAX(vector<u8> &cut) {
        rfori(i, cut.size()) {
            if (cut[i]) {
                fori(j, i) {
                    cut[j] = 0;
                }
                break;
            }
        }
    }
    static inline void MIN(vector<u8> &cut) {
        fori(i, cut.size()) {
            if (cut[i]) {
                fori(j, i + 1, cut.size()) {
                    cut[j] = 0;
                }
                break;
            }
        }
    }
    static inline void REV(vector<u8> &cut) {
        reverse(cut.begin(), cut.end());
    }

    // for dense Quine-McCluskey
    static inline void AND_up_OR(vector<u8> &cut) {
        assert(cut.size() == 3);
        cut[2] |= cut[0] & cut[1];
    }
    static inline void NOTAND_down(vector<u8> &cut) {
        assert(cut.size() == 3);
        cut[0] &= ~cut[2];
        cut[1] &= ~cut[2];
    }

    // for python low-level API
    void do_Sweep_OR_up(uint64_t mask = -1ull);
    void do_Sweep_OR_down(uint64_t mask = -1ull);
    void do_Sweep_MAX(uint64_t mask = -1ull);
    void do_Sweep_MIN(uint64_t mask = -1ull);
    void do_Sweep_REV(uint64_t mask = -1ull);
    void do_Sweep_AND_up_OR(uint64_t mask = -1ull);
    void do_Sweep_NOTAND_down(uint64_t mask = -1ull);

    // ========================================
    // Main methods
    // ========================================
    void do_UpperSet(uint64_t mask = -1ull);
    void do_LowerSet(uint64_t mask = -1ull);
    void do_MaxSet(uint64_t mask = -1ull);
    void do_MinSet(uint64_t mask = -1ull);

    void do_Complement();

    void do_ComplementU2L(bool is_upper=false, uint64_t mask = -1ull);
    void do_ComplementL2U(bool is_lower=false, uint64_t mask = -1ull);

    // ========================================
    // Copy aliases
    // ========================================
    DenseBox UpperSet(uint64_t mask = -1ull) const;
    DenseBox LowerSet(uint64_t mask = -1ull) const;
    DenseBox MaxSet(uint64_t mask = -1ull) const;
    DenseBox MinSet(uint64_t mask = -1ull) const;

    DenseBox Complement() const;

    DenseBox ComplementU2L(bool is_upper=false, uint64_t mask = -1ull) const;
    DenseBox ComplementL2U(bool is_lower=false, uint64_t mask = -1ull) const;

    DenseSet to_DenseSet() const;

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

    def __getstate__(self):
        return self.VERSION, list(self.dimensions), self.data.__getstate__()

    def __setstate__(self, st):
        version, dimensions, data = st
        assert version == self.VERSION
        self.__init__(dimensions)
        self.data.__setstate__(data)
        return self
    %}
    #endif

private:
    void __enumerate(DenseSet &d, const vector<uint64_t> &xs, uint64_t cur, int pos) const;
};