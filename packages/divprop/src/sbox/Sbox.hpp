#pragma once

#include <random>
#include <chrono>

#include "common.hpp"
#include "DenseSet.hpp"

template<typename T>
struct T_Sbox {
    int n, m;
    std::vector<T> data;
    uint64_t xmask;
    uint64_t ymask;

    static const uint64_t VERSION1 = 0xcbd6c2fe63066fffull;
    static const uint64_t MARKER_END = 0x143d15e3d6f4f9baull;

    constexpr static uint64_t ENTRY_SIZE = sizeof(T);

    constexpr static bool is_Sbox_class = true;

#ifdef SWIG
    %pythoncode %{
    @classmethod
    def __instancecheck__(cls, inst):
        return getattr(inst, "is_Sbox_class", False)
    %}
#endif

    T_Sbox(int n, int m) {
        this->data.resize(1ull << n);
        this->n = n;
        this->m = m;
        init();
    }
    T_Sbox(const std::vector<T> &data, int n, int m) {
        this->data = data;
        this->n = n;
        this->m = m;
        init();
    }
    void init() {
        ensure(0 <= n && n <= 62);
        ensure(0 <= m && uint64_t(m) <= sizeof(T) * 8);
        ensure(data.size() == (1ull << n));
        xmask = (1ull << n) - 1;
        ymask = (m == 64) ? -1ull : ((1ull << m) - 1);
        fori (x, 1ll << n) {
            ensure(0 <= data[x] && data[x] <= ymask);
        }
    }
    uint64_t get_hash() const {
        uint64_t h = 0xcd35ac633ca730f7ull;
        for (auto v: data) {
            h ^= v;
            h *= 0x579012b977f2665bull;
            h ^= h >> 23;
            h += v;
            h ^= h >> 10;
        }
        return h;
    }
    std::string info() const {
        char buf[4096];
        snprintf(
            buf, 4000,
            "<Sbox hash=%016lx n=%d m=%d>",
            get_hash(), n, m
        );
        return string(buf);
    }

    void invert_in_place() {
        ensure(n == m);
        T_Sbox<T> ret = *this;
        fori (x, xmask + 1) {
            set(ret.data[x], x);
        }
        return;
    }
    T_Sbox<T> inverse() const {
        ensure(n == m);
        T_Sbox<T> ret(n, m);
        fori (x, xmask + 1) {
            ret.set(data[x], x);
        }
        return ret;
    }

    T get(uint64_t x) const {
        ensure(x <= xmask);
        return data[x];
    }
    T set(uint64_t x, const T y) {
        ensure(x <= xmask);
        ensure(y <= ymask);
        data[x] = y;
        return y;
    }

    DenseSet coordinate_product(T mask) const {
        DenseSet f(n);
        fori (x, 1ull << n) {
            uint64_t y = (uint64_t)data[x];
            int bit = (y & mask) == mask;
            f.set(x, bit);
        }
        return f;
    }

    DenseSet graph_dense() const {
        DenseSet graph(n + m);
        fori (x, 1ull << n) {
            uint64_t y = (uint64_t)data[x];
            graph.add((u64(x) << m) | y);
        }
        return graph;
    }

    std::vector<DenseSet> coordinates() const {
        std::vector<DenseSet> funcs(m, DenseSet(n));
        fori (x, 1ull << n) {
            uint64_t y = (uint64_t)data[x];
            fori (i, m) {
                funcs[m-1-i].set(x, (y >> i) & 1);
            }
        }
        return funcs;
    }

    DenseSet coordinate(int i) const {
        ensure(0 <= i && i < n);
        DenseSet func(n);
        fori (x, 1ull << n) {
            uint64_t y = (uint64_t)data[x];
            func.set(x, (y >> (m - 1 - i)) & 1);
        }
        return func;
    }

    std::vector<std::vector<uint8_t>> to_matrix() const {
        // m x n matrix
        std::vector<std::vector<uint8_t>> ret(m, std::vector<uint8_t>(n));
        fori (xi, n) {
            uint64_t y = (uint64_t)data[1ull << (n - 1 - xi)];
            rfori(yi, m) {
                ret[yi][xi] = y & 1;
                y >>= 1;
            }
        }
        return ret;
    }

    bool is_invertible() const {
        if (m != n) {
            return false;
        }
        vector<bool> seen(1ull << m);
        fori (x, 1ull << n) {
            seen[data[x]] = 1;
        }
        fori (y, 1ull << m) {
            if (!seen[y]) {
                return false;
            }
        }
        return true;
    }

    static T_Sbox<T> GEN_random_permutation(int n, uint64_t seed=-1ull) {
        ensure(1 <= n && n <= 62);
        if (seed == -1ull) {
            seed = std::chrono::system_clock::now().time_since_epoch().count();
        }

        T_Sbox<T> res(n, n);
        fori (x, 1ull << n) {
            res.set(x, x);
        }
        std::mt19937 engine(seed);
        shuffle(res.data.begin(), res.data.end(), engine);
        return res;
    }

    void save_to_file(const char *filename) const {
        FILE *fd = fopen(filename, "w");
        ensure(fd, "can not open file");

        uint64_t header = VERSION1;
        uint64_t vt = sizeof(T);
        uint64_t vn = n;
        uint64_t vm = m;

        fwrite(&header, 8, 1, fd);
        fwrite(&vt, 8, 1, fd);
        fwrite(&vn, 8, 1, fd);
        fwrite(&vm, 8, 1, fd);

        fwrite(data.data(), vt, 1ull << vn, fd);

        uint64_t marker = MARKER_END;
        fwrite(&marker, 8, 1, fd);
        fclose(fd);
    }
    static T_Sbox<T> load_from_file(const char *filename) {
        FILE *fd = fopen(filename, "r");
        ensure(fd, "can not open file");


        uint64_t header;
        fread(&header, 8, 1, fd);

        if (header == VERSION1) {
            uint64_t vt, vn, vm;
            fread(&vt, 8, 1, fd);
            fread(&vn, 8, 1, fd);
            fread(&vm, 8, 1, fd);

            ensure(sizeof(T) == vt, "can not load sbox of different word size, sorry");

            T_Sbox<T> res(vn, vm);
            fread(res.data.data(), vt, 1ull << vn, fd);

            uint64_t marker;
            fread(&marker, 8, 1, fd);
            ensure(marker == MARKER_END, "file format error");

            fclose(fd);
            return res;
        }
        else {
            ensure(0, "unknown sbox file version");
        }
        return T_Sbox<T>(0, 0);
    }

    #ifdef SWIG
    %pythoncode %{
        def __str__(self):
            return self.info()
        def __repr__(self):
            return self.info()
        def __invert__(self):
            return self.inverse()
        def __getitem__(self, x):
            return self.get(int(x))
        def __setitem__(self, x, v):
            return self.set(int(x), int(v))
        def __len__(self):
            return len(self.data)
        def __iter__(self):
            return iter(self.data)

        def __getstate__(self):
            return self.n, self.m, list(self.data)

        def __setstate__(self, st):
            n, m, data = st
            self.__init__(data, n, m)
            return self
    %}
    #endif
};