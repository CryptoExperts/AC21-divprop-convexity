#include "common.hpp"

#include "BitSet.hpp"
#include "DenseSet.hpp"
#include "DenseBox.hpp"
#include "Sweep.hpp"

TTi
static T vector_sum(const vector<T> & vec) {
    T s = 0;
    for (auto &v: vec) {
        s += v;
    }
    return s;
}

void DenseSet::set_quiet(bool value) {
    BitSet::set_quiet(value);
}

DenseSet::DenseSet(int n, const std::vector<uint64_t> &ints) : DenseSet::DenseSet(n) {
    for (auto v: ints) {
        set(v);
    }
}
// void DenseSet::resize(int _n) {
//     // WARNING: keeps only "small" values if n decreases
//     ensure(_n >= 0 and _n <= 64, "supported set dimension is between 0 and 64");
//     n = _n;
//     data.resize(HICEIL(1ull << n));
// }
DenseSet DenseSet::copy() const {
    return *this;
}
void DenseSet::resize(uint64_t n) {
    this->n = n;
    this->data.resize(1ull << n);
}
void DenseSet::clear() {
    data.clear();
    n = 0;
}
void DenseSet::empty() {
    data.empty();
}
void DenseSet::fill() {
    data.fill();
}


bool DenseSet::is_empty() const {
    return data.is_empty();
}
bool DenseSet::is_full() const {
    return data.is_full();
}

// ========================================
// Single bit get/set
// ========================================
int DenseSet::get(uint64_t x) const {
    return data.get(x);
}
void DenseSet::set(uint64_t x) {
    data.set(x);
}
void DenseSet::unset(uint64_t x) {
    data.unset(x);
}
void DenseSet::flip(uint64_t x) {
    data.get(x) ? data.unset(x) : data.set(x);
}
void DenseSet::set(uint64_t x, uint64_t value) {
    data.set(x, value);
}
void DenseSet::add(uint64_t x) {
    data.add(x);
}
void DenseSet::remove(uint64_t x) {
    // ensure is inside
    data.remove(x);
}
void DenseSet::discard(uint64_t x) {
    // ignore if is inside
    data.discard(x);
}


// ========================================
// Tools
// ========================================
// for python low-level API
void DenseSet::do_Sweep_OR_up(uint64_t mask) {
    do_Sweep<OR_up<uint64_t>>(mask);
}
void DenseSet::do_Sweep_OR_down(uint64_t mask) {
    do_Sweep<OR_down<uint64_t>>(mask);
}
void DenseSet::do_Sweep_XOR_up(uint64_t mask) {
    do_Sweep<XOR_up<uint64_t>>(mask);
}
void DenseSet::do_Sweep_XOR_down(uint64_t mask) {
    do_Sweep<XOR_down<uint64_t>>(mask);
}
void DenseSet::do_Sweep_AND_up(uint64_t mask) {
    do_Sweep<AND_up<uint64_t>>(mask);
}
void DenseSet::do_Sweep_AND_down(uint64_t mask) {
    do_Sweep<AND_down<uint64_t>>(mask);
}
void DenseSet::do_Sweep_SWAP(uint64_t mask) {
    do_Sweep<SWAP<uint64_t>>(mask);
}
void DenseSet::do_Sweep_LESS_up(uint64_t mask) {
    do_Sweep<LESS_up<uint64_t>>(mask);
}
void DenseSet::do_Sweep_MORE_down(uint64_t mask) {
    do_Sweep<MORE_down<uint64_t>>(mask);
}

// ========================================
// Bitwise
// ========================================
bool DenseSet::is_compatible_set(const DenseSet & b) const {
    return n == b.n;
}
bool DenseSet::operator==(const DenseSet & b) const {
    ensure(is_compatible_set(b), "boxes have different dimensions");
    return data == b.data;
}
bool DenseSet::operator!=(const DenseSet & b) const {
    ensure(is_compatible_set(b), "boxes have different dimensions");
    return data != b.data;
}
bool DenseSet::operator<(const DenseSet & b) const {
    ensure(is_compatible_set(b), "boxes have different dimensions");
    return data < b.data;
}
bool DenseSet::operator>(const DenseSet & b) const {
    ensure(is_compatible_set(b), "boxes have different dimensions");
    return data > b.data;
}
bool DenseSet::operator<=(const DenseSet & b) const {
    ensure(is_compatible_set(b), "boxes have different dimensions");
    return data <= b.data;
}
bool DenseSet::operator>=(const DenseSet & b) const {
    ensure(is_compatible_set(b), "boxes have different dimensions");
    return data >= b.data;
}

DenseSet & DenseSet::operator|=(const DenseSet & b) {
    ensure(is_compatible_set(b), "sets have different dimensions");
    data |= b.data;
    return *this;
}
DenseSet & DenseSet::operator^=(const DenseSet & b) {
    ensure(is_compatible_set(b), "sets have different dimensions");
    data ^= b.data;
    return *this;
}
DenseSet & DenseSet::operator&=(const DenseSet & b) {
    ensure(is_compatible_set(b), "sets have different dimensions");
    data &= b.data;
    return *this;
}
DenseSet & DenseSet::operator-=(const DenseSet & b) {
    ensure(is_compatible_set(b), "sets have different dimensions");
    data -= b.data;
    return *this;
}
DenseSet DenseSet::operator|(const DenseSet & b) const {
    auto res = copy();
    res |= b;
    return res;
}
DenseSet DenseSet::operator^(const DenseSet & b) const {
    auto res = copy();
    res ^= b;
    return res;
}
DenseSet DenseSet::operator&(const DenseSet & b) const {
    auto res = copy();
    res &= b;
    return res;
}
DenseSet DenseSet::operator-(const DenseSet & b) const {
    auto res = copy();
    res -= b;
    return res;
}
// DenseSet DenseSet::operator~() const {
//     return Complement();
// }

DenseSet DenseSet::get_head_fixed(int h, uint64_t value) {
    ensure(value < (1ull << h));
    ensure(h >=0 && h <= n);
    ensure(n - h >= 6);
    DenseSet result(n - h);
    uint64_t start = value << (n - h - 6);
    uint64_t end = (value + 1) << (n - h - 6);
    result.data = vector<uint64_t>(data.data.begin() + start, data.data.begin() + end);
    return result;
}

// ========================================
// Support
// ========================================

void DenseSet::iter_support(function<void(uint64_t)> const & func) const {
    data.iter_support(func);
}

// returns support of the function
// 32-bit version useful? if support is small then 2x RAM does not matter
// if it's large then working with DenseSet is better anyway...
vector<uint64_t> DenseSet::get_support() const {
    vector<uint64_t> inds;
    auto func = [&] (uint64_t v) -> void { inds.push_back(v); };
    iter_support(func);
    return inds;
}

uint64_t DenseSet::get_weight() const {
    return data.get_weight();
}

vector<uint64_t> DenseSet::get_counts_by_weights() const {
    vector<uint64_t> res(n+1);
    auto func = [&] (uint64_t v) -> void { res[hw(v)] += 1; };
    iter_support(func);
    return res;
}
map<pair<int,int>,uint64_t> DenseSet::get_counts_by_weight_pairs(int n1, int n2) const {
    ensure(n == n1 + n2);

    map<pair<int,int>, uint64_t> res;
    uint64_t mask2 = (1ull << n2)-1;
    auto func = [&] (uint64_t v) -> void {
        uint64_t l = v >> n2;
        uint64_t r = v &mask2;
        res[make_pair(hw(l),hw(r))] += 1;
    };
    iter_support(func);
    return res;
}
string DenseSet::str_stat_by_weights() const {
    string ret;
    char buf[4096] = "";
    auto by_wt = get_counts_by_weights();
    fori(i, n+1) {
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
string DenseSet::str_stat_by_weight_pairs(int n1, int n2) const {
    string ret;
    char buf[4096] = "";
    auto by_wt = get_counts_by_weight_pairs(n1, n2);
    for (auto &p: by_wt) {
        if (p.second) {
            snprintf(
                buf, 4000, "%d,%d:%lu ",
                p.first.first, p.first.second, p.second
            );
            ret += buf;
        }
    };
    if (ret.size()) {
        ret.erase(ret.end() - 1);
    }
    return ret;
}

// ========================================
// Main methods
// ========================================

void DenseSet::do_UnsetUp(uint64_t mask) {
    do_Sweep<ZERO_up<uint64_t>>(mask);
}
void DenseSet::do_UnsetDown(uint64_t mask) {
    do_Sweep<ZERO_down<uint64_t>>(mask);
}
void DenseSet::do_SetUp(uint64_t mask) {
    do_Sweep<ONE_up<uint64_t>>(mask);
}
void DenseSet::do_SetDown(uint64_t mask) {
    do_Sweep<ONE_down<uint64_t>>(mask);
}
void DenseSet::do_Mobius(uint64_t mask) {
    do_Sweep<XOR_up<uint64_t>>(mask);
}
void DenseSet::do_ParitySet(uint64_t mask) {
    do_Sweep<XOR_down<uint64_t>>(mask);
}
void DenseSet::do_Complement() {
    data.do_Complement();
}
void DenseSet::do_Not(uint64_t mask) {
    mask &= (1ull << n)-1;
    auto &raw = data.data;
    uint64_t lo = LO(mask);
    uint64_t hi = HI(mask);
    if (lo) {
        for(uint64_t &word: raw) {
            GenericSweepWord<SWAP<uint64_t>>(word, lo);
        }
    }
    if (hi) {
        fori(i, raw.size()) {
            uint64_t j = i ^ hi;
            ensure(j < raw.size());
            if (j < uint64_t(i))
                continue;
            swap(raw[i], raw[j]);
        }
    }
}
void DenseSet::do_UpperSet(uint64_t mask) {
    do_Sweep<OR_up<uint64_t>>(mask);
}
void DenseSet::do_LowerSet(uint64_t mask) {
    do_Sweep<OR_down<uint64_t>>(mask);
}
void DenseSet::do_MinSet(uint64_t mask) {
    do_UpperSet(mask);
    do_Sweep<LESS_up<uint64_t>>(mask);
}
void DenseSet::do_MaxSet(uint64_t mask) {
    do_LowerSet(mask);
    do_Sweep<MORE_down<uint64_t>>(mask);
}
void DenseSet::do_DivCore(uint64_t mask) {
    do_Sweep<XOR_up<uint64_t>>(mask);
    do_MaxSet(mask);
    do_Not(mask);
}
void DenseSet::do_ComplementU2L(bool is_upper, uint64_t mask) {
    if (!is_upper)
        do_Sweep<OR_up<uint64_t>>(mask);
    do_Complement();
    do_MaxSet(mask);
}
void DenseSet::do_ComplementL2U(bool is_lower, uint64_t mask) {
    if (!is_lower)
        do_Sweep<OR_down<uint64_t>>(mask);
    do_Complement();
    do_MinSet(mask);
}
void DenseSet::do_UpperSet_Up1(bool is_minset, uint64_t mask) {
    if (!is_minset)
        do_MinSet(-1ull);

    // not in-place :( but min set should not be large
    auto minset = get_support();
    auto &raw = data.data;
    // quicker empty
    for (auto uv: minset) {
        raw[HI(uv)] = 0;
    }
    for (auto uv: minset) {
         fori(i, n) {
            if ((mask & (1ull << i)) == 0)
                continue;
            uint64_t uv2 = uv | (1ull << i);
            if (uv2 != uv) {
                raw[HI(uv2)] |= 1ull << LO(uv2);
            }
        }
    }
}

vector<int64_t> DenseSet::WalshHadamard(uint64_t mask) const {
    // 0 -> 1,  1 -> -1
    vector<int64_t> ret(1ull << n, 1);
    auto func = [&] (uint64_t v) -> void { ret[v] = -1; };
    iter_support(func);
    GenericSweep<WALSH_HADAMARD<int64_t>>(ret, mask);
    return ret;
}

DenseSet DenseSet::Mobius(uint64_t mask) const {
    auto ret = copy();
    ret.do_Mobius(mask);
    return ret;
}
DenseSet DenseSet::ParitySet(uint64_t mask) const {
    auto ret = copy();
    ret.do_ParitySet(mask);
    return ret;
}
DenseSet DenseSet::Complement() const {
    auto ret = copy();
    ret.do_Complement();
    return ret;
}
DenseSet DenseSet::Not(uint64_t mask) const {
    auto ret = copy();
    ret.do_Not(mask);
    return ret;
}
DenseSet DenseSet::UpperSet(uint64_t mask) const {
    auto ret = copy();
    ret.do_UpperSet(mask);
    return ret;
}
DenseSet DenseSet::LowerSet(uint64_t mask) const {
    auto ret = copy();
    ret.do_LowerSet(mask);
    return ret;
}
DenseSet DenseSet::MinSet(uint64_t mask) const {
    auto ret = copy();
    ret.do_MinSet(mask);
    return ret;
}
DenseSet DenseSet::MaxSet(uint64_t mask) const {
    auto ret = copy();
    ret.do_MaxSet(mask);
    return ret;
}
DenseSet DenseSet::DivCore(uint64_t mask) const {
    auto ret = copy();
    ret.do_DivCore(mask);
    return ret;
}
DenseSet DenseSet::ComplementU2L(bool is_upper, uint64_t mask) const {
    auto ret = copy();
    ret.do_ComplementU2L(is_upper, mask);
    return ret;
}
DenseSet DenseSet::ComplementL2U(bool is_lower, uint64_t mask) const {
    auto ret = copy();
    ret.do_ComplementL2U(is_lower, mask);
    return ret;
}
DenseSet DenseSet::UpperSet_Up1(bool is_minset, uint64_t mask) const {
    auto ret = copy();
    ret.do_UpperSet_Up1(is_minset, mask);
    return ret;
}

// ========================================
// Stuff
// ========================================
void DenseSet::save_to_file(const char *filename) const {
    data.save_to_file(filename);
}
DenseSet DenseSet::load_from_file(const char *filename) {
    DenseSet res;
    res.data = BitSet::load_from_file(filename);
    res.n = log2(res.data.n);
    ensure(1ull << res.n == res.data.n);
    return res;
}

uint64_t DenseSet::get_hash() const {
    return data.get_hash();
}
std::string DenseSet::info() const {
    char buf[4096] = {};
    snprintf(
        buf, 4000,
        "<DenseSet hash=%016lx n=%d wt=%lu | ",
        get_hash(), n, get_weight()
    );
    return string(buf) + str_stat_by_weights() + ">";
}

// uint64_t DenseSet::project_to_Box(uint64_t v, const std::vector<uint64_t> & dimensions) const {
//     int ndim = (int)dimensions.size();
//     vector<uint64_t> xs;
//     rfori(i, ndim) {
//         uint64_t mask = (1ull << (dimensions[i] - 1)) - 1;
//         xs.push_back(hw(v & mask));
//         v >>= dimensions[i] - 1;
//     }
//     reverse(xs.begin(), xs.end());
//     return DenseBox::_pack(xs, dimensions);
// }

DenseBox DenseSet::to_DenseBox(const std::vector<uint64_t> & dimensions) const {
    int ndim = (int)dimensions.size();
    ensure(vector_sum(dimensions) == (uint64_t)n);
    DenseBox d(dimensions);
    auto func = [&] (uint64_t v) -> void {
        vector<uint64_t> xs;
        rfori(i, ndim) {
            uint64_t mask = (1ull << dimensions[i]) - 1;
            xs.push_back(hw(v & mask));
            v >>= dimensions[i];
        }
        reverse(xs.begin(), xs.end());
        d.add(xs);
    };
    iter_support(func);
    return d;
}