#include <iostream>
#include <functional>

#include "common.hpp"

#include "DenseBox.hpp"

TTi
static T vector_sum(const vector<T> & vec) {
    T s = 0;
    for (auto &v: vec) {
        s += v;
    }
    return s;
}

DenseBox::DenseBox(const std::vector<int> & dimensions) {
    this->dimensions = std::vector<uint64_t>(dimensions.begin(), dimensions.end());
    n = dimensions.size();
    fullsize = 1;
    for(auto i: dimensions) {
        ensure(i >= 1);
        fullsize *= i + 1;
    }
    data = BitSet(fullsize);
}
DenseBox::DenseBox(const std::vector<uint64_t> & dimensions) {
    this->dimensions = std::vector<uint64_t>(dimensions.begin(), dimensions.end());
    n = dimensions.size();
    fullsize = 1;
    for(auto i: dimensions) {
        ensure(i >= 1);
        fullsize *= i + 1;
    }
    data = BitSet(fullsize);
}

DenseBox DenseBox::copy() const {
    return *this;
}

void DenseBox::clear() {
    n = 0;
    dimensions.clear();
    data.clear();
}
void DenseBox::empty() {
    data.empty();
}
void DenseBox::fill() {
    data.fill();
}
bool DenseBox::is_empty() const {
    return data.is_empty();
}
bool DenseBox::is_full() const {
    return data.is_full();
}

// ========================================
// Read/Write & info
// ========================================
void DenseBox::save_to_file(const char *filename) const {
    FILE *fd = fopen(filename, "w");
    ensure(fd, "can not open file");

    save_to_file(fd);

    fclose(fd);
}
DenseBox DenseBox::load_from_file(const char *filename) {
    FILE *fd = fopen(filename, "r");
    ensure(fd, "can not open file");

    auto ret = load_from_file(fd);

    fclose(fd);
    return ret;
}
void DenseBox::save_to_file(FILE *fd) const {
    ensure(1 == fwrite(&DenseBox::VERSION, 8, 1, fd));

    uint64_t ndim = dimensions.size();
    ensure(n == (int)ndim);

    ensure(1 == fwrite(&ndim, 8, 1, fd));
    for(auto dim: dimensions) {
        uint64_t dimword = dim;
        ensure(1 == fwrite(&dimword, 8, 1, fd));
    }

    data.save_to_file(fd);

    ensure(1 == fwrite(&DenseBox::MARKER_END, 8, 1, fd));
}
DenseBox DenseBox::load_from_file(FILE *fd) {
    uint64_t header;
    ensure(1 == fread(&header, 8, 1, fd));
    ensure(header == DenseBox::VERSION, "unknown file version");

    uint64_t ndim;
    ensure(1 == fread(&ndim, 8, 1, fd));
    ensure(0 <= ndim && ndim <= 64);
    vector<int> dimensions;
    fori (_, ndim) {
        uint64_t dim;
        ensure(1 == fread(&dim, 8, 1, fd));
        dimensions.push_back((int)dim);
    }

    DenseBox res(dimensions);
    res.data = BitSet::load_from_file(fd);

    uint64_t marker;
    ensure(1 == fread(&marker, 8, 1, fd));
    ensure(marker == DenseBox::MARKER_END, "unknown file version");
    return res;
}

uint64_t DenseBox::get_hash() const {
    uint64_t h = n;
    h *= 0xcaffee1234abcdefull;
    for (int v: dimensions) {
        h ^= v;
        h *= 0xcaffee1234abcdefull;
        h ^= h >> 12;
        h += v;
        h ^= h >> 17;
    }
    for (uint64_t v: data.data) {
        h ^= v;
        h *= 0xcaffee1234abcdefull;
        h ^= h >> 12;
        h += v;
        h ^= h >> 17;
    }
    return h;
}
std::string DenseBox::info() const {
    string dim;
    fori(i, n) {
        dim += to_string(dimensions[i]);
        if (i < n - 1)
            dim += ",";
    }

    char buf[4096] = {};
    snprintf(
        buf, 4000,
        "<DenseBox(%s) hash=%016lx wt=%lu | %s>",
        dim.c_str(), get_hash(), get_weight(), str_stat_by_weights().c_str()
    );
    return string(buf);
}
void DenseBox::print() const {
    fori(x, fullsize) {
        if (data.get(x)) {
            printf("x %016lx (", x);
            for(auto &v: unpack(x)) {
                printf("%lu,", v);
            }
            printf(")\n");
        }
    }
}

// ========================================
// Single bit get/set
// ========================================
std::vector<u64> DenseBox::unpack(u64 x) const {
    vector<u64> xs(n);
    rfori(i, n) {
        xs[i] = x % (dimensions[i] + 1);
        x /= (dimensions[i] + 1);
    }
    return xs;
}
u64 DenseBox::pack(const std::vector<u64> & xs) const {
    ensure(xs.size() == (size_t)n);
    u64 x = 0;
    fori(i, n) {
        x *= (dimensions[i] + 1);
        ensure(xs[i] <= dimensions[i]);
        x += xs[i];
    }
    ensure(x < fullsize);
    return x;
}
uint64_t DenseBox::project(uint64_t x) const {
    return DenseBox::_project(x, dimensions);
}

std::vector<u64> DenseBox::_unpack(u64 x, const std::vector<uint64_t> & dimensions) {
    uint64_t n = dimensions.size();
    vector<u64> xs(n);
    rfori(i, n) {
        xs[i] = x % (dimensions[i] + 1);
        x /= (dimensions[i] + 1);
    }
    return xs;
}
u64 DenseBox::_pack(const std::vector<u64> & xs, const std::vector<uint64_t> & dimensions) {
    uint64_t n = dimensions.size();
    u64 x = 0;
    fori(i, n) {
        x *= (dimensions[i] + 1);
        ensure(xs[i] <= dimensions[i]);
        x += xs[i];
    }
    return x;
}
uint64_t DenseBox::_project(uint64_t x, const std::vector<uint64_t> & dimensions) {
    uint64_t ndim = dimensions.size();
    vector<uint64_t> xs;
    rfori(i, ndim) {
        uint64_t mask = (1ull << dimensions[i]) - 1;
        xs.push_back(hw(x & mask));
        x >>= dimensions[i];
    }
    ensure(!x);
    reverse(xs.begin(), xs.end());
    return DenseBox::_pack(xs, dimensions);
}

int DenseBox::get(u64 x) const {
    return data.get(x);
}
void DenseBox::set(u64 x) {
    data.set(x);
}
void DenseBox::unset(u64 x) {
    data.unset(x);
}
void DenseBox::set(u64 x, u64 value) {
    data.set(x, value);
}
void DenseBox::add(uint64_t x) {
    set(x);
}
void DenseBox::remove(uint64_t x) {
    ensure(get(x));
    unset(x);
}
void DenseBox::discard(uint64_t x) {
    unset(x);
}

int DenseBox::get(const vector<uint64_t> & xs) const {
    return data.get(pack(xs));
}
void DenseBox::set(const vector<uint64_t> & xs) {
    data.set(pack(xs));
}
void DenseBox::unset(const vector<uint64_t> & xs) {
    data.unset(pack(xs));
}
void DenseBox::set(const vector<uint64_t> & xs, u64 value) {
    data.set(pack(xs), value);
}
void DenseBox::add(const vector<uint64_t> & xs) {
    set(pack(xs));
}
void DenseBox::remove(const vector<uint64_t> & xs) {
    auto x = pack(xs);
    ensure(get(x));
    unset(x);
}
void DenseBox::discard(const vector<uint64_t> & xs) {
    unset(pack(xs));
}

// ========================================
// Support
// ========================================
void DenseBox::iter_support(function<void(u64 x)> const & func) const {
    data.iter_support(func);
}

std::vector<uint64_t> DenseBox::get_support() const {
    vector<uint64_t> inds;
    auto func = [&] (uint64_t v) -> void { inds.push_back(v); };
    iter_support(func);
    return inds;
}
std::vector<std::vector<uint64_t>> DenseBox::get_unpacked() const {
    vector<vector<uint64_t>> res;
    auto func = [&] (uint64_t v) -> void { res.push_back(unpack(v)); };
    iter_support(func);
    return res;
}


uint64_t DenseBox::get_weight() const {
    return data.get_weight();
}
std::vector<uint64_t> DenseBox::get_counts_by_weights() const {
    u64 max_wt = vector_sum(dimensions);
    vector<uint64_t> res(max_wt + 1);
    auto func = [&] (uint64_t v) -> void {
        res[vector_sum(unpack(v))] += 1;
    };
    iter_support(func);
    return res;
}

string DenseBox::str_stat_by_weights() const {
    string ret;
    char buf[4096] = "";
    auto by_wt = get_counts_by_weights();
    fori(i, by_wt.size()) {
        if (by_wt[i]) {
            snprintf(buf, 4000, "%lu:%lu ", i, by_wt[i]);
            ret += buf;
        }
    };
    if (ret.size()) {
        ret.erase(ret.end() - 1);
    }
    return ret;
}

// ========================================
// Bitwise ops
// ========================================
bool DenseBox::is_compatible_set(const DenseBox & b) const {
    return b.dimensions == dimensions;
}
bool DenseBox::operator==(const DenseBox & b) const {
    ensure(is_compatible_set(b), "boxes have different dimensions");
    return data == b.data;
}
bool DenseBox::operator!=(const DenseBox & b) const {
    ensure(is_compatible_set(b), "boxes have different dimensions");
    return data != b.data;
}
bool DenseBox::operator<(const DenseBox & b) const {
    ensure(is_compatible_set(b), "boxes have different dimensions");
    return data < b.data;
}
bool DenseBox::operator>(const DenseBox & b) const {
    ensure(is_compatible_set(b), "boxes have different dimensions");
    return data > b.data;
}
bool DenseBox::operator<=(const DenseBox & b) const {
    ensure(is_compatible_set(b), "boxes have different dimensions");
    return data <= b.data;
}
bool DenseBox::operator>=(const DenseBox & b) const {
    ensure(is_compatible_set(b), "boxes have different dimensions");
    return data >= b.data;
}


DenseBox & DenseBox::operator|=(const DenseBox & b) {
    ensure(is_compatible_set(b), "sets have different dimensions");
    data |= b.data;
    return *this;
}
DenseBox & DenseBox::operator^=(const DenseBox & b) {
    ensure(is_compatible_set(b), "sets have different dimensions");
    data ^= b.data;
    return *this;
}
DenseBox & DenseBox::operator&=(const DenseBox & b) {
    ensure(is_compatible_set(b), "sets have different dimensions");
    data &= b.data;
    return *this;
}
DenseBox & DenseBox::operator-=(const DenseBox & b) {
    ensure(is_compatible_set(b), "sets have different dimensions");
    data -= b.data;
    return *this;
}
DenseBox DenseBox::operator|(const DenseBox & b) const {
    auto res = copy();
    res |= b;
    return res;
}
DenseBox DenseBox::operator^(const DenseBox & b) const {
    auto res = copy();
    res ^= b;
    return res;
}
DenseBox DenseBox::operator&(const DenseBox & b) const {
    auto res = copy();
    res &= b;
    return res;
}
DenseBox DenseBox::operator-(const DenseBox & b) const {
    auto res = copy();
    res -= b;
    return res;
}
DenseBox DenseBox::operator~() const {
    return Complement();
}

// ========================================
// Sweeps
// ========================================
// template<auto func>
// void do_Sweep(uint64_t mask) {
//     u64 div = 1;
//     fori(ni, n) {
//         if ((mask & (1ull << ni)) == 0)
//             continue;

//         int i = n - 1 - ni;
//         u64 dim = dimensions[i];
//         fori(x, fullsize) {
//             u64 val = (x / div) % dim;
//             if (val == 0) {
//                 vector<u8> bits(dim);
//                 fori(j, dim) {
//                     bits[j] = data.get(x + j * div);
//                 }
//                 func(bits);
//                 fori(j, dim) {
//                     data.set(x + j * div, bits[j]);
//                 }
//             }
//         }
//         div *= dimensions[i];
//     }
// }
// for python low-level API
void DenseBox::do_Sweep_OR_up(uint64_t mask) {
    do_Sweep<OR_up>(mask);
}
void DenseBox::do_Sweep_OR_down(uint64_t mask) {
    do_Sweep<OR_down>(mask);
}
void DenseBox::do_Sweep_MAX(uint64_t mask) {
    do_Sweep<MAX>(mask);
}
void DenseBox::do_Sweep_MIN(uint64_t mask) {
    do_Sweep<MIN>(mask);
}
void DenseBox::do_Sweep_REV(uint64_t mask) {
    do_Sweep<REV>(mask);
}
void DenseBox::do_Sweep_AND_up_OR(uint64_t mask) {
    do_Sweep<AND_up_OR>(mask);
}
void DenseBox::do_Sweep_NOTAND_down(uint64_t mask) {
    do_Sweep<NOTAND_down>(mask);
}

void DenseBox::do_UpperSet(uint64_t mask) {
    do_Sweep<OR_up>(mask);
}
void DenseBox::do_LowerSet(uint64_t mask) {
    do_Sweep<OR_down>(mask);
}
void DenseBox::do_MaxSet(uint64_t mask) {
    do_LowerSet(mask);
    do_Sweep<MAX>(mask);
}
void DenseBox::do_MinSet(uint64_t mask) {
    do_UpperSet(mask);
    do_Sweep<MIN>(mask);
}

void DenseBox::do_Complement() {
    data.do_Complement();
}

void DenseBox::do_ComplementU2L(bool is_upper, uint64_t mask) {
    if (!is_upper)
        do_UpperSet();
    do_Complement();
    do_MaxSet(mask);
}
void DenseBox::do_ComplementL2U(bool is_lower, uint64_t mask) {
    if (!is_lower)
        do_LowerSet();
    do_Complement();
    do_MinSet(mask);
}

// ========================================
// Copy aliases
// ========================================

DenseBox DenseBox::UpperSet(uint64_t mask) const {
    auto ret = copy();
    ret.do_UpperSet(mask);
    return ret;
}
DenseBox DenseBox::LowerSet(uint64_t mask) const {
    auto ret = copy();
    ret.do_LowerSet();
    return ret;
}
DenseBox DenseBox::MaxSet(uint64_t mask) const {
    auto ret = copy();
    ret.do_MaxSet();
    return ret;
}
DenseBox DenseBox::MinSet(uint64_t mask) const {
    auto ret = copy();
    ret.do_MinSet();
    return ret;
}
DenseBox DenseBox::Complement() const {
    auto ret = copy();
    ret.do_Complement();
    return ret;
}
DenseBox DenseBox::ComplementU2L(bool is_upper, uint64_t mask) const {
    auto ret = copy();
    ret.do_ComplementU2L();
    return ret;
}
DenseBox DenseBox::ComplementL2U(bool is_lower, uint64_t mask) const {
    auto ret = copy();
    ret.do_ComplementL2U();
    return ret;
}


vector<uint64_t> all_of_weight(int wt, uint64_t len) {
    vector<uint64_t> res;
    fori(i, 1ll << len) {
        if (hw(i) == wt) {
            res.push_back(i);
        }
    }
    return res;
}

void DenseBox::__enumerate(DenseSet &d, const vector<uint64_t> &xs, uint64_t cur, int pos) const {
    ensure(pos <= n);
    if (pos == n) {
        d.set(cur);
        return;
    }
    for(uint64_t chunk: all_of_weight(xs[pos], dimensions[pos])) {
        __enumerate(d, xs, (cur << dimensions[pos]) | chunk, pos + 1);
    }
}


DenseSet DenseBox::to_DenseSet() const {
    uint64_t len = vector_sum(dimensions);
    ensure(len < 63, "too large box?");

    DenseSet res(len);
    auto func = [&] (uint64_t x) -> void {
        auto xs = unpack(x);
        __enumerate(res, xs, 0, 0);
    };
    iter_support(func);
    return res;
}