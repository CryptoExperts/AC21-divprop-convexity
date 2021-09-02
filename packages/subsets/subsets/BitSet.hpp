#pragma once

#ifdef SWIG
%pythoncode %{
    import ctypes
%}
#endif

#include "hackycpp.h" // for types

#include <functional>

namespace Pack64 {
    inline uint64_t HI(uint64_t x) {
        return x >> 6;
    }

    inline uint64_t LO(uint64_t x) {
        return x & 0x3f;
    }

    inline uint64_t HICEIL(uint64_t x) {
        return (x >> 6) + ((x & 0x3f) != 0);
    }
}

struct BitSet {
    uint64_t n;
    std::vector<uint64_t> data;

    static const uint64_t VERSION_SPARSE = 0x1c674e0bf03fea6full;
    static const uint64_t VERSION_DENSE = 0x556483ae0da9468full;
    static const uint64_t MARKER_END = 0x6891a2b5f8bb0b7cull;
    static bool QUIET;  // set to true to disable stderr printing

    static void set_quiet(bool value=true);

    BitSet() : n(0) {};
    BitSet(uint64_t _n) : n (_n), data(Pack64::HICEIL(_n)) {};

    BitSet(const std::vector<uint64_t> &_data);
    BitSet(const std::string &_bits);
    BitSet(const std::vector<char> &_bits);

    BitSet copy() const;
    void resize(uint64_t n);

    uint64_t nwords() const;
    void _trim();

    void clear();
    void empty();
    void fill();

    bool is_empty() const;
    bool is_full() const;

    // ========================================
    // Read/Write & info
    // ========================================
    void save_to_file(FILE *fd) const;
    void save_to_file(const char *filename) const;
    static BitSet load_from_file(const char *filename);
    static BitSet load_from_file(FILE *fd);
    std::string str() const;
    std::string info() const;
    uint64_t get_hash() const;

    // ========================================
    // Single bit get/set
    // ========================================
    int get(uint64_t i) const;
    void set(uint64_t i);
    void unset(uint64_t i);
    void set(uint64_t i, uint64_t value);

    void add(uint64_t x);
    void remove(uint64_t x);
    void discard(uint64_t x);

    // ========================================
    // Comparison
    // ========================================
    bool operator==(const BitSet &bs) const;
    bool operator!=(const BitSet &bs) const;
    bool operator<(const BitSet &bs) const;
    bool operator>(const BitSet &bs) const;
    bool operator<=(const BitSet &bs) const;
    bool operator>=(const BitSet &bs) const;

    // ========================================
    // Bitwise ops
    // ========================================
    BitSet& operator|=(const BitSet &bs);
    BitSet& operator^=(const BitSet &bs);
    BitSet& operator&=(const BitSet &bs);
    BitSet& operator-=(const BitSet &bs);
    BitSet operator^(const BitSet &bs) const;
    BitSet operator|(const BitSet &bs) const;
    BitSet operator&(const BitSet &bs) const;
    BitSet operator-(const BitSet &bs) const;
    // BitSet operator~() const;

    // ========================================
    // Support
    // ========================================
    void iter_support(function<void(uint64_t)> const & func) const;
    std::vector<uint64_t> get_support() const;
    uint64_t get_weight() const;

    // ========================================
    // Main methods
    // ========================================
    void do_Complement();

    // ========================================
    // Copy aliases
    // ========================================
    BitSet Complement() const;

    uint64_t _get_data_ptr() const;

    #ifdef SWIG
    %pythoncode %{
    def __bool__(self):
        return not self.is_empty()

    def __str__(self):
        return self.str()

    def __repr__(self):
        return self.info()

    def __contains__(self, x):
        return bool(self.get(x))

    def __iter__(self):
        return iter(self.get_support())

    def __len__(self):
        return self.get_weight()

    def __getstate__(self):
        data = ctypes.string_at(self._get_data_ptr(), self.data.size() * 8)
        return self.n, self.data.size(), data

    def __setstate__(self, st):
        n, l, data = st
        self.__init__(n)
        assert self.data.size() == l
        dst = self._get_data_ptr()
        src = self._bytes_to_ctypes(data)
        ctypes.memmove(dst, src, len(data))
        return self

    __swig_destroy__ = _subsets.delete_BitSet

    @staticmethod
    def _bytes_to_ctypes(data):
        try:
            # version for pypy, fails on python (non writeable)
            return (ctypes.c_char * len(data)).from_buffer(data)
        except:
            # version for python, fails on pypy (makes extra copies)
            return ctypes.cast(data, ctypes.c_void_p)
    %}
    #endif
};